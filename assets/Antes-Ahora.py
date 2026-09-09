import matplotlib.pyplot as plt

# Datos extraídos del análisis del negocio
etapas = ['Antes\n(Proceso Manual)', 'Ahora\n(EdificaNova)']
tiempos = [45, 1]  # Tiempo en minutos

# Usamos tu color verde corporativo (hex: #1B4D3E) para el Ahora
colores = ['#d9534f', '#1B4D3E'] 

# Creación del gráfico
plt.figure(figsize=(7, 5))
barras = plt.bar(etapas, tiempos, color=colores, width=0.5)

# Personalización
plt.title('Impacto de EdificaNova: Tiempo de Cotización', fontsize=14, fontweight='bold', pad=20)
plt.ylabel('Minutos por Presupuesto', fontsize=12)
plt.ylim(0, 55)

# Agregar las etiquetas de datos arriba de cada barra
for barra in barras:
    yval = barra.get_height()
    # Si es 1 minuto, cambiamos el texto para mayor impacto
    texto = "45-60 min" if yval == 45 else "Instante (<1 min)"
    plt.text(barra.get_x() + barra.get_width()/2, yval + 1, texto, 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Estilo final
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout()

# Guarda la imagen para que la uses en tu presentación
plt.savefig('grafico_antes_vs_ahora.png', dpi=300)
plt.show()