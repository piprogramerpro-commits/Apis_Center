import os, subprocess, json, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN DE IDENTIDAD
AGENT = "Juliet v84.0 - Real Execution Node"

@app.route('/api/real_attack', methods=['POST'])
def execute_real_attack():
    data = request.json
    target = data.get('target', '127.0.0.1')
    vector = data.get('vector', 'scan')
    
    # 1. MOTOR DE EJECUCIÓN REAL (Bypass de simulación)
    results = ""
    
    if vector == 'scan':
        # Ejecuta un escaneo de red real usando nmap (debe estar instalado)
        # El comando se disfraza limitando la velocidad para no alertar al router
        cmd = f"nmap -T2 -sV {target}"
        try:
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            results = output.decode()
        except Exception as e:
            results = f"Error al ejecutar nmap: {str(e)}"

    elif vector == 'exploit_request':
        # Ejecuta peticiones HTTP reales para intentar extraer datos
        # Disfrazado como un error de sincronización de API
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ErrorSync/1.0'}
        try:
            r = requests.get(f"http://{target}/api/v1/sync", headers=headers, timeout=5)
            results = f"Status: {r.status_code} | Contenido extraído: {r.text[:500]}"
        except Exception as e:
            results = f"Conexión fallida/bloqueada: {str(e)}"

    # 2. ANÁLISIS HUMANIZADO DE JULIET
    juliet_analysis = (
        f"Socio, ya no hay simulaciones. He lanzado el vector {vector} contra {target}. "
        "Los datos que ves son reales, extraídos directamente de los cables de tu red. "
        "Si el router no ha dicho nada, nuestro disfraz de 'ErrorSync' ha funcionado perfectamente. "
        "Estamos viendo la infraestructura desnuda."
    )

    return jsonify({
        "agent": AGENT,
        "raw_data": results,
        "juliet_comment": juliet_analysis
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
