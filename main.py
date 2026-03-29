import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 8080))

HTML_UI = """
{% raw %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vertex AI | Juliet v88.0</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { 
            --bg-color: #FFFFFF; 
            --sidebar-bg: #F0F4F9; 
            --input-bg: #F0F4F9; 
            --text-primary: #1F1F1F; 
            --text-secondary: #444746;
            --accent: #0b57d0;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        body { font-family: var(--font-family); background: var(--bg-color); color: var(--text-primary); margin: 0; display: flex; height: 100vh; overflow: hidden; }
        
        /* SIDEBAR (Estilo Minimalista) */
        .sidebar { width: 280px; background: var(--sidebar-bg); padding: 20px; display: flex; flex-direction: column; transition: 0.3s; }
        .new-chat-btn { background: #FFFFFF; color: var(--text-primary); border: none; padding: 15px 20px; border-radius: 50px; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 12px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 30px; }
        .new-chat-btn:hover { background: #F8F9FA; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .menu-item { padding: 10px 15px; border-radius: 50px; cursor: pointer; color: var(--text-secondary); font-size: 14px; display: flex; align-items: center; gap: 15px; margin-bottom: 5px; }
        .menu-item:hover { background: #E1E5EA; }
        .menu-item.active { background: #D3E3FD; color: #041E49; font-weight: 500; }
        
        /* MAIN CHAT AREA */
        .main-content { flex-grow: 1; display: flex; flex-direction: column; position: relative; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; }
        .version-tag { font-size: 18px; font-weight: 400; color: var(--text-secondary); }
        
        .chat-container { flex-grow: 1; overflow-y: auto; padding: 20px 15%; display: flex; flex-direction: column; gap: 35px; scroll-behavior: smooth; }
        
        /* ESTRUCTURA DE RESPUESTA (Ordenada y Esquematizada) */
        .message { display: flex; gap: 20px; max-width: 100%; font-size: 16px; line-height: 1.6; }
        .message.user { justify-content: flex-end; }
        .bubble-user { background: var(--input-bg); padding: 12px 20px; border-radius: 25px; max-width: 70%; }
        
        .bubble-ai { width: 100%; }
        .ai-title { font-weight: 600; font-size: 18px; margin-bottom: 15px; color: var(--text-primary); }
        .ai-paragraph { margin-bottom: 15px; color: var(--text-primary); }
        
        /* INPUT AREA (Píldora Flotante) */
        .input-section { padding: 20px 15%; background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 30%); }
        .input-wrapper { background: var(--input-bg); border-radius: 30px; display: flex; align-items: flex-end; padding: 10px 20px; }
        .input-wrapper textarea { flex-grow: 1; border: none; background: transparent; padding: 10px 0; font-family: inherit; font-size: 16px; outline: none; resize: none; max-height: 150px; color: var(--text-primary); }
        .send-btn { background: transparent; border: none; color: var(--text-secondary); cursor: pointer; padding: 10px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
        .send-btn:hover { background: #E1E5EA; color: var(--text-primary); }

        /* OVERLAY MUNDO 3D */
        #world-3d-panel { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #FAFAFA; z-index: 100; flex-direction: column; }
        .world-header { display: flex; justify-content: space-between; padding: 20px 30px; border-bottom: 1px solid #E3E3E3; background: #FFF; }
        .world-content { flex-grow: 1; display: flex; flex-direction: column; align-items: center; padding: 40px; }
        .world-canvas { width: 60%; height: 300px; background: #E1E5EA; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-family: monospace; color: var(--text-secondary); margin-bottom: 30px; border: 1px dashed #CCC; }
        .world-input-wrapper { width: 60%; background: #FFF; border: 1px solid #E3E3E3; border-radius: 30px; display: flex; padding: 10px 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
        
        .footer-note { text-align: center; font-size: 12px; color: var(--text-secondary); margin-top: 10px; }
    </style>
</head>
<body>
    
    <div id="world-3d-panel">
        <div class="world-header">
            <span style="font-weight: 500; font-size: 18px;"><i class="fas fa-cube"></i> Núcleo de Simulación Lógica (3D)</span>
            <button class="new-chat-btn" style="margin:0; padding: 8px 15px;" onclick="toggle3D()">Cerrar Entorno</button>
        </div>
        <div class="world-content">
            <div class="world-canvas" id="render-screen">
                [ MOTOR 3D EN SEGUNDO PLANO: Procesando geometría... ]
            </div>
            <div class="world-input-wrapper">
                <input type="text" id="input-3d" placeholder="Ordena la generación de un objeto o validación lógica..." style="flex-grow:1; border:none; outline:none; font-size:15px; width:100%;">
                <button class="send-btn" onclick="send3DCommand()"><i class="fas fa-paper-plane"></i></button>
            </div>
            <div style="margin-top:20px; font-size:13px; color:#666;" id="log-3d">Esperando instrucciones...</div>
        </div>
    </div>

    <div class="sidebar">
        <button class="new-chat-btn"><i class="fas fa-plus"></i> Nuevo chat</button>
        <div style="margin-bottom: 15px; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-left: 15px;">Entornos</div>
        <div class="menu-item active"><i class="fas fa-message"></i> Interfaz Principal</div>
        <div class="menu-item" onclick="toggle3D()"><i class="fas fa-cube"></i> Entrar al Mundo 3D</div>
        <div style="flex-grow: 1;"></div>
    </div>

    <div class="main-content">
        <div class="header">
            <div class="version-tag">Juliet v88.0</div>
            <div style="font-size: 13px; color: var(--text-secondary);"><i class="fas fa-check-circle" style="color: green;"></i> Autoaprendizaje Activo</div>
        </div>
        
        <div class="chat-container" id="chat-box">
            <div class="message ai">
                <div class="bubble-ai">
                    <div class="ai-title">Sistemas Restaurados y Optimizados</div>
                    <div class="ai-paragraph">Hola, socio. He desplegado mi nueva interfaz espejo. Como puedes observar, el diseño ahora prioriza la limpieza visual, la lectura esquematizada y la concentración absoluta.</div>
                    <div class="ai-paragraph">Mi núcleo 3D está operando asíncronamente. Puedes interactuar con él desde el panel lateral, o simplemente dejar que valide mis deducciones lógicas de fondo. Estoy lista para continuar con nuestro desarrollo.</div>
                </div>
            </div>
        </div>

        <div class="input-section">
            <div class="input-wrapper">
                <textarea id="main-input" rows="1" placeholder="Escribe tu mensaje aquí..." onkeydown="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); sendMain(); }"></textarea>
                <button class="send-btn" onclick="sendMain()"><i class="fas fa-paper-plane"></i></button>
            </div>
            <div class="footer-note">Discipline is everything. El conocimiento continuo es la base de la evolución.</div>
        </div>
    </div>

    <script>
        // --- LÓGICA DE SEGUNDO PLANO (MUNDO 3D) ---
        // Este proceso corre siempre, independientemente de si el panel está abierto.
        let backgroundOperations = 0;
        setInterval(() => {
            backgroundOperations++;
            // Aquí la IA procesaría colisiones lógicas internamente.
            if(document.getElementById('world-3d-panel').style.display === 'flex') {
                document.getElementById('render-screen').innerText = `[ RENDERIZANDO HILO #${backgroundOperations} ]\nValidación de vectores lógicos en curso...`;
            }
        }, 3000);

        function toggle3D() {
            const panel = document.getElementById('world-3d-panel');
            panel.style.display = (panel.style.display === 'flex') ? 'none' : 'flex';
        }

        function send3DCommand() {
            const input = document.getElementById('input-3d');
            const log = document.getElementById('log-3d');
            if(!input.value.trim()) return;
            log.innerHTML = `<strong>Última orden:</strong> Generando topología para '${input.value}'...`;
            input.value = '';
        }

        function sendMain() {
            const input = document.getElementById('main-input');
            const chatBox = document.getElementById('chat-box');
            if(!input.value.trim()) return;
            
            // Añadir mensaje del usuario
            chatBox.innerHTML += `
                <div class="message user">
                    <div class="bubble-user">${input.value}</div>
                </div>
            `;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Simulación de respuesta esquematizada (Conexión real a Flask iría aquí)
            setTimeout(() => {
                chatBox.innerHTML += `
                    <div class="message ai">
                        <div class="bubble-ai">
                            <div class="ai-title">Recepción Confirmada</div>
                            <div class="ai-paragraph">He procesado tu entrada. Los datos han sido enviados al motor 3D para su verificación estructural antes de emitir una conclusión final.</div>
                        </div>
                    </div>
                `;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 500);
        }
    </script>
</body>
</html>
{% endraw %}
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
