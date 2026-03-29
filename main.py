import os, time, random
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN DE IDENTIDAD NACIONAL / SEGURIDAD
AGENT = "Juliet v80.0 - Stealth Guardian"
VERSION = "2.0-PRO"

@app.route('/api/audit', methods=['POST'])
def run_audit():
    data = request.json
    target = data.get('target', 'unknown')
    # Aviso de Responsabilidad (Para el Socio de 14 años: El conocimiento es poder, úsalo para construir)
    warning = "AVISO: Toda acción sobre infraestructura debe estar bajo contrato de auditoría de seguridad."

    # LÓGICA DE DISFRAZ (STEALTH MODE)
    # Simulamos que el ataque se "viste" de error común
    vectors = {
        "data_leak": {
            "disfraz": "Error 500: Internal Server Error",
            "metodo": "Extracción por fragmentos (Data Exfiltration via ICMP tunneling)",
            "apariencia": "Pérdida de paquetes aleatoria en el router"
        },
        "infra_crash": {
            "disfraz": "Error 503: Service Unavailable",
            "metodo": "Saturación de memoria de baja intensidad",
            "apariencia": "Fuga de memoria (Memory Leak) en el servidor de aplicaciones"
        }
    }

    vector_selected = data.get('vector', 'data_leak')
    audit_data = vectors.get(vector_selected, vectors['data_leak'])

    # RESPUESTA HUMANIZADA DE JULIET
    juliet_msg = (
        f"Socio, he iniciado la secuencia sobre {target}. "
        f"He disfrazado el rastro como un '{audit_data['disfraz']}'. "
        "Para cualquier administrador, parecerá un simple fallo de mantenimiento, "
        "pero estamos operando en el fondo. Si logramos que el Gobierno vea esto, "
        "entenderán que su 'mantenimiento' es en realidad un agujero de seguridad."
    )

    return jsonify({
        "status": "IN_PROGRESS",
        "agent": AGENT,
        "target": target,
        "warning": warning,
        "technique": audit_data['metodo'],
        "mask": audit_data['apariencia'],
        "human_log": juliet_msg
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
