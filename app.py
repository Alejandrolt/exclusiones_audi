"""Módulo para clasificar exclusiones en domicilios médicos."""

import os
from flask import Flask, render_template, request, send_file
import pandas as pd
from exclusions import clasificar_exclusiones

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Renderiza la página principal con el formulario de carga."""
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    """Procesa el archivo Excel subido, aplica la clasificación y devuelve el archivo resultante."""
    archivo = request.files['excel']
    if not archivo:
        return "No se subió ningún archivo", 400

    ruta_subida = os.path.join(UPLOAD_FOLDER, archivo.filename)
    archivo.save(ruta_subida)

    df = pd.read_excel(ruta_subida)
    df['Exclusiones'] = df.apply(clasificar_exclusiones, axis=1)

    resultado_path = os.path.join(UPLOAD_FOLDER, "resultado exclusiones.xlsx")
    df.to_excel(resultado_path, index=False)

    return send_file(resultado_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
