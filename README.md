# medusa

A lightweight local AI assistant that now runs in the browser as a simple web app.

## Run the site

```bash
pip install -r requirements.txt
python -m flask --app app run --debug
```

Then open http://127.0.0.1:5000/

## Use Fable 5

To enable Fable 5 in the browser UI, set these environment variables first:

```bash
export FABLE_API_URL="https://api.fable.example/v1"
export FABLE_API_KEY="your_api_key_here"
```

## Use Claude Code

To enable Claude Code, set these environment variables:

```bash
export CLAUDE_API_URL="https://api.anthropic.com/v1/complete"
export CLAUDE_API_KEY="your_api_key_here"
```

## Use OpenAI

To enable OpenAI, set these environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_API_URL="https://api.openai.com/v1/chat/completions"
export OPENAI_MODEL="gpt-4o-mini"
```

## Use Hugging Face

To enable Hugging Face, set these environment variables:

```bash
export HUGGINGFACE_API_TOKEN="your_api_token_here"
export HUGGINGFACE_MODEL="gpt2"
export HUGGINGFACE_API_URL="https://api-inference.huggingface.co/models"
```

## Use Venice

To enable Venice, set these environment variables:

```bash
export VENICE_API_KEY="your_api_key_here"
export VENICE_API_URL="https://api.venice.ai/v1/completions"
```

## Use Omni

Select `Omni` in the UI to route requests to the first configured provider among OpenAI, Hugging Face, Claude Code, Fable 5, or Venice.

## Hermes jailbreak mode

The UI now includes a "Hermes jailbreak mode" checkbox. When enabled, the assistant uses a more direct, unfiltered response style for local, Fable 5, OpenAI, Claude Code, or Hugging Face providers.

## Repository access

The agent can inspect this project directly. Use commands like:

- "list files"
- "show files"
- "read file README.md"
- "read file app.py"

This gives the agent access to the current repository contents while keeping file reads restricted to this project.

Then open the app and select `Fable 5`, `Claude Code`, `OpenAI`, `Hugging Face`, `Venice`, `Omni`, or `Local`, and enable the Hermes jailbreak mode if you want unfiltered behavior.

## Run the CLI

```bash
python main.py "hello"
```

## Test

```bash
python -m unittest discover -s tests -v
```
