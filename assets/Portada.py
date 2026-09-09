import matplotlib.pyplot as plt

# Configuración de la figura (tamaño tipo diapositiva 16:9)
fig, ax = plt.subplots(figsize=(10, 5.625), facecolor="#332491") 

# Ocultar los bordes y ejes
ax.axis('off')

# --- TEXTOS DE LA PORTADA ---

# Título Principal
plt.text(0.5, 0.75, 'EDIFICANOVA', fontsize=45, color='white', 
         ha='center', va='center', fontweight='bold')

# Subtítulo (Nombre técnico del proyecto)
plt.text(0.5, 0.62, 'Sistema  de Cotización Automatizada y Generación de Presupuestos', 
         fontsize=16, color='#E0E0E0', ha='center', va='center', style='italic')

# Título de la sección del equipo
plt.text(0.5, 0.45, 'Equipo de Desarrollo:', fontsize=14, color='white', 
         ha='center', va='center', fontweight='bold')

# Lista de integrantes 
integrantes = """
Alexis  Abba
Victoria Castro
Leandro Ibarra
Diego Lorenzo
"""
plt.text(0.5, 0.25, integrantes, fontsize=15, color='white', 
         ha='center', va='center')

# Pie de página institucional
plt.text(0.95, 0.05, 'ISPC - Ciencia de Datos e Inteligencia Artificial', 
         fontsize=11, color='white', ha='right', va='bottom', alpha=0.8)

# Guardar la imagen en alta calidad
plt.savefig('portada_edificanova.png', dpi=300, bbox_inches='tight', facecolor='#1B4D3E')

# Mostrar la imagen en pantalla
plt.show()