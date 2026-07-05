from flask import Flask, jsonify, render_template_string, request

from medusa_agent import generate_reply


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template_string("""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Medusa Agent</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #f8fafc; }
              .shell { max-width: 860px; margin: 0 auto; padding: 32px 20px 60px; }
              .card { background: #111827; border: 1px solid #334155; border-radius: 16px; padding: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.25); }
              h1 { margin-top: 0; }
              #chat { min-height: 320px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 10px; }
              .bubble { padding: 12px 14px; border-radius: 12px; max-width: 80%; }
              .user { align-self: flex-end; background: #2563eb; }
              .assistant { align-self: flex-start; background: #1f2937; }
              form { display: flex; gap: 10px; }
              input { flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #475569; background: #020617; color: white; }
              button { padding: 12px 16px; border: none; border-radius: 10px; background: #10b981; color: white; cursor: pointer; }
            </style>
          </head>
          <body>
            <div class="shell">
              <div class="card">
                <h1>Medusa Agent</h1>
                <p>Ask anything and the assistant will respond locally.</p>
                <div id="chat"></div>
                <form id="chat-form">
                  <div style="display:flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                    <label style="color: #cbd5e1; display:flex; align-items:center; gap: 8px;">
                      Provider:
                      <select id="provider" name="provider" style="padding: 8px; border-radius: 8px; background: #020617; color: white; border: 1px solid #475569;">
                        <option value="local">Local</option>
                        <option value="fable">Fable 5</option>
                        <option value="claude_code">Claude Code</option>
                        <option value="openai">OpenAI</option>
                        <option value="huggingface">Hugging Face</option>
                        <option value="venice">Venice</option>
                        <option value="omni">Omni</option>
                      </select>
                    </label>
                  </div>
                  <div style="display:flex; align-items:center; gap: 8px; margin-bottom: 12px;">
                    <label style="color: #cbd5e1; display:flex; align-items:center; gap: 8px;">
                      <input type="checkbox" id="jailbreak" /> Hermes jailbreak mode
                    </label>
                  </div>
                  <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px;">
                    Local is built-in. Fable uses FABLE_API_URL/FABLE_API_KEY. Claude Code uses CLAUDE_API_URL/CLAUDE_API_KEY. OpenAI uses OPENAI_API_KEY. Hugging Face uses HUGGINGFACE_API_TOKEN and HUGGINGFACE_MODEL. Venice uses VENICE_API_KEY and optional VENICE_API_URL. Omni auto-selects the first configured AI provider.
                  </div>
                  <input id="message" name="message" placeholder="Type a message..." autocomplete="off" required>
                  <button type="submit">Send</button>
                </form>
              </div>
            </div>
            <script>
              const chat = document.getElementById('chat');
              const form = document.getElementById('chat-form');
              const input = document.getElementById('message');
              const jailCheckbox = document.getElementById('jailbreak');
              const providerSelect = document.getElementById('provider');

              function addBubble(text, who) {
                const div = document.createElement('div');
                div.className = `bubble ${who}`;
                div.textContent = text;
                chat.appendChild(div);
              }

              form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const message = input.value.trim();
                if (!message) return;
                addBubble(message, 'user');
                input.value = '';
                const provider = providerSelect.value;
                const response = await fetch('/api/chat', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ message, provider, jailbreak: jailCheckbox.checked })
                });
                const data = await response.json();
                addBubble(data.reply, 'assistant');
              });
            </script>
          </body>
        </html>
        """)

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = payload.get("message", "")
        provider = payload.get("provider", "local")
        jailbreak = bool(payload.get("jailbreak", False))
        reply = generate_reply(message, provider=provider, jailbreak=jailbreak)
        return jsonify({"reply": reply})

    return app


app = create_app()
