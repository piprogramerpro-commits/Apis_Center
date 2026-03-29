import os, time, random
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN DE IDENTIDAD TÉCNICA
AGENT = "Juliet v81.0 - Stealth Engine"

@app.route('/api/attack_vector', methods=['POST'])
def execute_stealth_vector():
    data = request.json
    target = data.get('target', 'unknown')
    vector_type = data.get('type', 'data_extraction')
    
    # MOTOR DE DISFRAZ (OBFUSCATION ENGINE)
    # Aquí definimos cómo se ve el ataque desde el lado del objetivo
    masks = {
        "data_extraction": {
            "mask_name": "Broken Image / Resource Load Fail",
            "log_entry": "GET /static/images/logo_err.png - 404 Not Found",
            "stealth_method": "Exfiltración de datos bit a bit dentro de los headers de peticiones 404"
        },
        "system_stress": {
            "mask_name": "Database Connection Timeout",
            "log_entry": "SQLSTATE[HY000] [2002] Connection timed out",
            "stealth_method": "Inyección de micro-retrasos para saturar el pool de conexiones sin disparar el Firewall"
        },
        "config_exploit": {
            "mask_name": "Legacy Browser Incompatibility",
            "log_entry": "User-Agent: MSIE 6.0 - Unsupported Protocol",
            "stealth_method": "Inyección de payloads en paquetes fragmentados que parecen tráfico de navegadores antiguos"
        }
    }

    selected = masks.get(vector_type, masks["data_extraction"])
    
    # Simulación de ejecución con "jitter" (tiempo aleatorio para no parecer un bot)
    time.sleep(random.uniform(1.5, 4.0))

    # RESPUESTA PARA DARING-INTUITION (JULIET)
    juliet_report = {
        "status": "SUCCESS",
        "disguise_active": selected["mask_name"],
        "server_log_simulation": selected["log_entry"],
        "human_analysis": f"Socio, el objetivo en {target} cree que tiene un problema de carga de imágenes. No saben que estamos dentro. He usado el disfraz de {selected['mask_name']} para que el sysadmin no se levante de la silla."
    }

    return jsonify(juliet_report)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
