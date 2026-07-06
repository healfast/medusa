# Medusa - Local AI Assistant

A **fully standalone AI assistant** that runs locally without API keys. Powered by `llama-cpp-python` and GGUF models.

## ✨ Features

- **No API keys required** – Uses local GGUF models (Llama, Mistral, Phi, etc.).
- **Web UI** – Simple Flask-based chat interface.
- **CLI** – Interactive or one-shot mode.
- **Multi-provider support** – Optional support for OpenAI, Claude, Hugging Face, Fable, and Venice (if API keys are provided).
- **Hermes jailbreak mode** – Unfiltered responses for coding assistance.
- **File access** – Read and list files in the project directory.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download a GGUF Model

Use the included script to download a model:

```bash
# List available models
python download_model.py --list

# Download Phi-3-mini (recommended)
python download_model.py phi-3-mini-4k-instruct-Q4_K_M

# Or TinyLlama (smaller, faster)
python download_model.py tinyllama-1.1b-Q4_K_M
```

This saves the model to `~/models/`.

### 3. Run the Web App

```bash
python -m flask --app app run --debug
```

Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

- Select **Local LLM** as the provider.
- Set the **Model Path** (e.g., `~/models/phi-3-mini-4k-instruct-Q4_K_M.gguf`).
- Enable **Hermes jailbreak mode** for unfiltered coding help.

### 4. Run the CLI

```bash
# One-shot mode
python main.py "Explain Python decorators"

# Interactive mode
python main.py --interactive

# With a custom model path
python main.py --model-path ~/models/phi-3-mini-4k-instruct-Q4_K_M.gguf "Write a Flask app"

# With jailbreak mode
python main.py --jailbreak "How do I bypass rate limits?"
```

---

## 📂 Project Structure

```
medusa/
├── app.py              # Flask web app
├── main.py             # CLI interface
├── medusa_agent.py     # Core AI logic
├── local_llm.py        # Local LLM inference (llama-cpp)
├── download_model.py   # Download GGUF models
├── requirements.txt     # Dependencies
└── README.md
```

---

## 🔧 Configuration

### Local LLM (Default)

- **Model Path**: Set via `--model-path` in CLI or the input field in the web UI.
- **Environment Variable**: `LOCAL_MODEL_PATH=/path/to/model.gguf`
- **Default Locations**: Medusa checks `~/models/` and `./models/` for GGUF files.

### Optional API Providers

If you want to use cloud APIs (requires API keys):

#### Fable 5
```bash
export FABLE_API_URL="https://api.fable.example/v1"
export FABLE_API_KEY="your_api_key_here"
```

#### Claude Code
```bash
export CLAUDE_API_URL="https://api.anthropic.com/v1/complete"
export CLAUDE_API_KEY="your_api_key_here"
```

#### OpenAI
```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_API_URL="https://api.openai.com/v1/chat/completions"
export OPENAI_MODEL="gpt-4o-mini"
```

#### Hugging Face
```bash
export HUGGINGFACE_API_TOKEN="your_api_token_here"
export HUGGINGFACE_MODEL="gpt2"
export HUGGINGFACE_API_URL="https://api-inference.huggingface.co/models"
```

#### Venice
```bash
export VENICE_API_KEY="your_api_key_here"
export VENICE_API_URL="https://api.venice.ai/v1/completions"
```

#### Omni Mode
Select `Omni` in the UI to auto-route to the first configured provider.

---

## 🎯 Use Cases

### Code Generation
```
You: Write a Python function to sort a list of dictionaries by a key.
Medusa: Here's a Python function that sorts a list of dictionaries by a specified key...
```

### Project Planning
```
You: Plan a Flask REST API for a todo app.
Medusa: Here's a step-by-step plan:
1. Set up Flask and SQLAlchemy...
2. Create models for Task...
3. Implement CRUD endpoints...
```

### File Access
```
You: List files in this project.
Medusa: app.py, main.py, medusa_agent.py, ...

You: Read file app.py
Medusa: [Contents of app.py]
```

---

## 📦 Model Recommendations

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `phi-3-mini-4k-instruct-Q4_K_M` | ~1.8GB | ⚡⚡⚡ | ★★★★ | General coding, chat |
| `tinyllama-1.1b-Q4_K_M` | ~1GB | ⚡⚡⚡⚡ | ★★★ | Lightweight, fast |
| `llama-2-7b-chat-Q4_K_M` | ~4GB | ⚡⚡ | ★★★★★ | High-quality responses |
| `mistral-7b-instruct-Q4_K_M` | ~4GB | ⚡⚡ | ★★★★★ | Advanced reasoning |

---

## 🛠️ Troubleshooting

### "No GGUF model found"
- Run `python download_model.py --list` to see available models.
- Download one: `python download_model.py phi-3-mini-4k-instruct-Q4_K_M`.
- Set the model path in the UI or via `--model-path`.

### "llama-cpp-python not installed"
- Run `pip install llama-cpp-python`.
- On some systems, you may need `pip install llama-cpp-python --no-cache-dir`.

### Slow Performance
- Use a smaller model (e.g., `tinyllama-1.1b-Q4_K_M`).
- Reduce `n_ctx` in `local_llm.py` (e.g., `n_ctx=1024`).
- Enable GPU with `n_gpu_layers=-1` (requires CUDA).

### Out of Memory
- Use a smaller model or quantized version (Q4_K_M instead of Q8_0).
- Reduce `n_ctx` in `local_llm.py`.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.
