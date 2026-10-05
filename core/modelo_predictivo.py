"""
Módulo de predicción de probabilidad de cierre — EdificaNova v0.5.0.

Entrena un clasificador Random Forest sobre el histórico comercial de la
constructora y expone una función pura `predecir_probabilidad()` que estima
la chance de que un lead se convierta en venta.

Clases del target (estado_lead):
    - VENDIDO       → venta concretada  (positivo)
    - POTABLE       → interés activo
    - NO LE INTERESA → descartado
"""
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer

# ── Rutas ────────────────────────────────────────────────────────────────────

_MODULE_DIR = Path(__file__).parent
_DATA_DIR = _MODULE_DIR / ".." / "data"
_MODEL_PATH = _DATA_DIR / "modelo_cierre.joblib"
_DATASET_PATH = _DATA_DIR / "dataset_constructora_final.csv"

# ── Features utilizadas ───────────────────────────────────────────────────────

FEATURES_NUMERICAS = ["distancia_km", "m2_referencia", "precio_cotizado"]
FEATURES_CATEGORICAS = [
    "sistema_constructivo",
    "tipo_entrega",
    "tipologia",
    "revestimiento",
    "forma_pago",
]
FEATURES = FEATURES_NUMERICAS + FEATURES_CATEGORICAS

TARGET = "estado_lead"
CLASE_POSITIVA = "VENDIDO"


# ── Pipeline de preprocesamiento + modelo ─────────────────────────────────────

def _construir_pipeline() -> Pipeline:
    preprocesador = ColumnTransformer(
        transformers=[
            (
                "num",
                SimpleImputer(strategy="median"),
                FEATURES_NUMERICAS,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OrdinalEncoder(
                        handle_unknown="use_encoded_value",
                        unknown_value=-1,
                    )),
                ]),
                FEATURES_CATEGORICAS,
            ),
        ]
    )
    return Pipeline([
        ("prep", preprocesador),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        )),
    ])


# ── Entrenamiento ─────────────────────────────────────────────────────────────

def entrenar_modelo(dataset_path: str = None, model_path: str = None) -> dict:
    """
    Entrena el modelo y lo guarda en disco.

    Parameters
    ----------
    dataset_path : str, opcional
        Ruta al CSV de entrenamiento. Por defecto usa data/dataset_constructora_final.csv.
    model_path : str, opcional
        Ruta donde guardar el modelo. Por defecto usa data/modelo_cierre.joblib.

    Returns
    -------
    dict
        Métricas del entrenamiento: accuracy, precision, recall en test set.
    """
    dataset_path = dataset_path or str(_DATASET_PATH)
    model_path = model_path or str(_MODEL_PATH)

    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=[TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = _construir_pipeline()
    pipeline.fit(X_train, y_train)

    # Métricas básicas
    from sklearn.metrics import classification_report
    y_pred = pipeline.predict(X_test)
    reporte = classification_report(y_test, y_pred, output_dict=True)

    joblib.dump(pipeline, model_path)

    return {
        "accuracy": round(reporte["accuracy"], 4),
        "vendido_precision": round(reporte.get(CLASE_POSITIVA, {}).get("precision", 0), 4),
        "vendido_recall": round(reporte.get(CLASE_POSITIVA, {}).get("recall", 0), 4),
        "vendido_f1": round(reporte.get(CLASE_POSITIVA, {}).get("f1-score", 0), 4),
        "model_path": model_path,
    }


# ── Inferencia ────────────────────────────────────────────────────────────────

def _cargar_modelo(model_path: str = None) -> Pipeline:
    model_path = model_path or str(_MODEL_PATH)
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Modelo no encontrado en {model_path}. "
            "Ejecutá entrenar_modelo() primero."
        )
    return joblib.load(model_path)


def predecir_probabilidad(
    m2: float,
    sistema_constructivo: str,
    tipo_entrega: str,
    distancia_km: float,
    tipologia: str = "AMERICANA",
    revestimiento: str = "LADRILLO",
    forma_pago: str = "CONTADO",
    precio_cotizado: float = None,
    model_path: str = None,
) -> dict:
    """
    Predice la probabilidad de cierre (venta) para una cotización nueva.

    Parameters
    ----------
    m2 : float
        Metros cuadrados del proyecto.
    sistema_constructivo : str
        Sistema constructivo (ej: "W.F.", "E.E.", "S.L.M").
    tipo_entrega : str
        Modalidad de entrega (ej: "OBRA GRIS", "LLAVE EN MANO").
    distancia_km : float
        Distancia logística en kilómetros.
    tipologia : str
        Tipología arquitectónica (ej: "AMERICANA", "CABAÑA").
    revestimiento : str
        Revestimiento exterior (ej: "LADRILLO", "MADERA").
    forma_pago : str
        Forma de pago (ej: "CONTADO", "PLAN 36-60").
    precio_cotizado : float, opcional
        Precio total cotizado. Si no se provee, se estima como m2 * 380000.
    model_path : str, opcional
        Ruta al modelo serializado.

    Returns
    -------
    dict
        {
          "probabilidad_vendido": float (0-1),
          "etiqueta": str ("🟢 Alta" | "🟡 Media" | "🔴 Baja"),
          "porcentaje": str ("78%"),
          "clases": dict con probabilidad de cada clase,
        }
    """
    pipeline = _cargar_modelo(model_path)

    if precio_cotizado is None:
        precio_cotizado = m2 * 380_000

    fila = pd.DataFrame([{
        "distancia_km": distancia_km,
        "m2_referencia": m2,
        "precio_cotizado": precio_cotizado,
        "sistema_constructivo": sistema_constructivo.upper(),
        "tipo_entrega": tipo_entrega.upper(),
        "tipologia": tipologia.upper(),
        "revestimiento": revestimiento.upper(),
        "forma_pago": forma_pago.upper(),
    }])

    probas = pipeline.predict_proba(fila)[0]
    clases = pipeline.classes_
    proba_dict = {c: round(float(p), 4) for c, p in zip(clases, probas)}

    prob_vendido = proba_dict.get(CLASE_POSITIVA, 0.0)

    if prob_vendido >= 0.35:
        etiqueta = "🟢 Alta"
    elif prob_vendido >= 0.15:
        etiqueta = "🟡 Media"
    else:
        etiqueta = "🔴 Baja"

    return {
        "probabilidad_vendido": prob_vendido,
        "etiqueta": etiqueta,
        "porcentaje": f"{prob_vendido * 100:.0f}%",
        "clases": proba_dict,
    }
