from flask import Flask, jsonify, render_template_string, request

from local_llm import list_available_models
from medusa_agent import generate_reply


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
            <title>Medusa Agent — Local AI</title>
            <style>
              :root { color-scheme: dark; }
              body {
                margin: 0;
                font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: radial-gradient(circle at top, #0f172a 0%, #020617 45%, #020617 100%);
                color: #e2e8f0;
              }
              .shell { max-width: 900px; margin: 0 auto; padding: 30px 18px 60px; }
              .card {
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 24px;
                padding: 22px;
                box-shadow: 0 18px 60px rgba(2, 6, 23, 0.45);
              }
              h1 { margin-top: 0; font-size: 2rem; }
              .lead { color: #94a3b8; line-height: 1.7; }
              #chat { min-height: 320px; margin: 16px 0; display: flex; flex-direction: column; gap: 10px; }
              .bubble { padding: 12px 14px; border-radius: 14px; max-width: 82%; line-height: 1.6; }
              .user { align-self: flex-end; background: linear-gradient(135deg, #2563eb, #1d4ed8); }
              .assistant { align-self: flex-start; background: #111827; border: 1px solid rgba(148, 163, 184, 0.16); }
              form { display: flex; flex-direction: column; gap: 10px; }
              .controls { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 6px; }
              label { color: #cbd5e1; display: flex; align-items: center; gap: 8px; }
              input, select { padding: 12px; border-radius: 10px; border: 1px solid #334155; background: #020617; color: #f8fafc; }
              button { padding: 12px 16px; border: none; border-radius: 10px; background: linear-gradient(135deg, #10b981, #34d399); color: #052e16; cursor: pointer; font-weight: 700; }
              .hint { color: #94a3b8; font-size: 0.95rem; }
              .models { color: #64748b; font-size: 0.9rem; }
            </style>
          </head>
          <body>
            <div class="shell">
              <div class="card">
                <h1>Medusa Agent</h1>
                <p class="lead">A fully local assistant for planning, coding, and explanations — free to run, with optional Ollama support and no API keys required.</p>
                <div id="chat"></div>
                <form id="chat-form">
                  <div class="controls">
                    <label>
                      Provider
                      <select id="provider" name="provider">
                        <option value="local">Local heuristics</option>
                        <option value="ollama">Ollama — llama2-uncensored</option>
                      </select>
                    </label>
                    <label>
                      Model path
                      <input type="text" id="model_path" name="model_path" placeholder="~/models/phi-3-mini-4k-instruct-Q4_K_M.gguf" value="" />
                    </label>
                  </div>
                  <div class="controls">
                    <label>
                      <input type="checkbox" id="jailbreak" checked /> Hermes godmode (default on)
                    </label>
                  </div>
                  <div class="hint">This experience prefers local models and repository-based answers. If Ollama is installed, it can use the local `llama2-uncensored` model.</div>
                  <div class="models">Available GGUF models: {{ model_options if model_options else "None found" }}</div>
                  <div class="controls">
                    <input id="message" name="message" placeholder="Ask anything..." autocomplete="off" required style="flex: 1;">
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
                const response = await fetch('/api/chat', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    message,
                    provider: providerSelect.value,
                    model_path: modelPathInput.value,
                    jailbreak: jailCheckbox.checked,
                  }),
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
        jailbreak = payload.get("jailbreak")
        if jailbreak is None:
            jailbreak = True
        else:
            jailbreak = bool(jailbreak)
        reply = generate_reply(message, provider=provider, jailbreak=jailbreak, model_path=model_path)
        return jsonify({"reply": reply})

    @app.get("/api/models")
    def list_models():
        return jsonify({"models": list_available_models()})

    return app


app = create_app()
