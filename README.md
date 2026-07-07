# Medusa - Local AI Assistant

Medusa is a fully local assistant that runs without API keys. It can use repository context, a local GGUF model through llama-cpp-python, or the Ollama CLI with the `llama2-uncensored` model when available.

## Features

- No API keys required
- Local web UI with a polished, DeepSeek-inspired experience
- Repository-aware planning, coding, and explanation help
- Optional local GGUF model support via llama-cpp-python
- Optional Ollama support via `ollama run llama2-uncensored ...`
- Hermes-style jailbreak mode for more direct guidance

## Quick start

```bash
pip install -r requirements.txt
python -m flask --app app run --debug
```

Then open http://127.0.0.1:5000/.

### Local LLM options

- GGUF models: place a model in `~/models/` or a local `models/` folder and either set `LOCAL_MODEL_PATH` or use the model path input in the UI.
- Ollama: install Ollama and pull the model from https://ollama.com/library/llama2-uncensored.

## Repository access

Use prompts such as:

- "list files"
- "read file README.md"
- "show files"

The assistant will inspect the current repository and answer based on the available source.

## Testing

```bash
python -m unittest discover -s tests -v
```
