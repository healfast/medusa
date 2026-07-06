from flask import Flask, jsonify, render_template_string, request

from medusa_agent import generate_reply
from local_llm import list_available_models


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        available_models = list_available_models()
        model_options = "\n".join(f"<option value='{m}'>{m}</option>" for m in available_models)
        return render_template_string("""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Medusa Agent - Local AI</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #f8fafc; }
              .shell { max-width: 860px; margin: 0 auto; padding: 32px 20px 60px; }
              .card { background: #111827; border: 1px solid #334155; border-radius: 16px; padding: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.25); }
              h1 { margin-top: 0; }
              #chat { min-height: 320px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 10px; }
              .bubble { padding: 12px 14px; border-radius: 12px; max-width: 80%; }
              .user { align-self: flex-end; background: #2563eb; }
              .assistant { align-self: flex-start; background: #1f2937; }
              form { display: flex; flex-direction: column; gap: 10px; }
              input, select { padding: 12px; border-radius: 10px; border: 1px solid #475569; background: #020617; color: white; }
              button { padding: 12px 16px; border: none; border-radius: 10px; background: #10b981; color: white; cursor: pointer; }
              .settings { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; }
              .settings label { color: #cbd5e1; display: flex; align-items: center; gap: 8px; }
              .info { color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px; }
              .model-info { font-size: 0.85rem; color: #64748b; }
            </style>
          </head>
          <body>
            <div class="shell">
              <div class="card">
                <h1>Medusa Agent</h1>
                <p><strong>Local AI Assistant - No API Keys Required!</strong></p>
                <p>Powered by <code>llama-cpp-python</code>. Download a GGUF model (e.g., Phi-3-mini, TinyLlama) and set the path below.</p>
                <div id="chat"></div>
                <form id="chat-form">
                  <div class="settings">
                    <label>
                      Provider:
                      <select id="provider" name="provider">
                        <option value="local">Local LLM</option>
                        <option value="fable">Fable 5</option>
                        <option value="claude_code">Claude Code</option>
                        <option value="openai">OpenAI</option>
                        <option value="huggingface">Hugging Face</option>
                        <option value="venice">Venice</option>
                        <option value="omni">Omni (Auto)</option>
                      </select>
                    </label>
                    <label>
                      Model Path:
                      <input type="text" id="model_path" name="model_path" placeholder="path/to/model.gguf" value="" />
                    </label>
                  </div>
                  <div class="settings">
                    <label style="color: #cbd5e1; display:flex; align-items:center; gap: 8px;">
                      <input type="checkbox" id="jailbreak" /> Hermes jailbreak mode
                    </label>
                  </div>
                  <div class="info">
                    <p><strong>Local LLM:</strong> Uses <code>llama-cpp-python</code>. Set the model path above (e.g., <code>~/models/phi-3-mini-4k-instruct-Q4_K_M.gguf</code>).</p>
                    <p><strong>API Providers:</strong> Fable, Claude, OpenAI, Hugging Face, and Venice require API keys. Omni auto-selects the first configured provider.</p>
                    <div class="model-info">
                      <strong>Available Models:</strong> {{ model_options if model_options else "None found" }}
                    </div>
                  </div>
                  <div style="display: flex; gap: 10px;">
                    <input id="message" name="message" placeholder="Type a message..." autocomplete="off" required style="flex: 1;">
                    <button type="submit">Send</button>
                  </div>
                </form>
              </div>
            </div>
            <script>
              const chat = document.getElementById('chat');
              const form = document.getElementById('chat-form');
              const input = document.getElementById('message');
              const jailCheckbox = document.getElementById('jailbreak');
              const providerSelect = document.getElementById('provider');
              const modelPathInput = document.getElementById('model_path');

              function addBubble(text, who) {
                const div = document.createElement('div');
                div.className = `bubble ${who}`;
                div.textContent = text;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
              }

              form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const message = input.value.trim();
                if (!message) return;
                addBubble(message, 'user');
                input.value = '';
                const provider = providerSelect.value;
                const modelPath = modelPathInput.value;
                const response = await fetch('/api/chat', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ 
                    message, 
                    provider, 
                    model_path: modelPath,
                    jailbreak: jailCheckbox.checked 
                  })
                });
                const data = await response.json();
                addBubble(data.reply, 'assistant');
              });
            </script>
          </body>
        </html>
        """, model_options=model_options)

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = payload.get("message", "")
        provider = payload.get("provider", "local")
        model_path = payload.get("model_path", None)
        jailbreak = bool(payload.get("jailbreak", False))
        reply = generate_reply(
            message, 
            provider=provider, 
            jailbreak=jailbreak,
            model_path=model_path
        )
        return jsonify({"reply": reply})

    @app.get("/api/models")
    def list_models():
        models = list_available_models()
        return jsonify({"models": models})

    return app


app = create_app()
