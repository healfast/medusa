from medusa_agent import generate_reply


def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Medusa - Local AI Assistant")
    parser.add_argument("prompt", nargs="*", help="Your prompt (optional if using interactive mode)")
    parser.add_argument("--provider", default="local", help="Provider: local, fable, claude_code, openai, huggingface, venice, omni")
    parser.add_argument("--model-path", default=None, help="Path to GGUF model file (for local provider)")
    parser.add_argument("--no-jailbreak", action="store_false", dest="jailbreak", default=True, help="Disable Hermes godmode responses")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    if args.prompt and not args.interactive:
        prompt = " ".join(args.prompt)
        reply = generate_reply(
            prompt,
            provider=args.provider,
            jailbreak=args.jailbreak,
            model_path=args.model_path,
        )
        print(f"Medusa: {reply}")
        return

    # Interactive mode
    print("Medusa - Local AI Assistant (Ctrl+C to exit)")
    print(f"Provider: {args.provider}")
    if args.model_path:
        print(f"Model: {args.model_path}")
    if args.jailbreak:
        print("Hermes godmode: ENABLED")
    else:
        print("Hermes godmode: DEFAULT ON")
    print("-" * 40)
    
    while True:
        try:
            prompt = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not prompt.strip():
            continue
        reply = generate_reply(
            prompt,
            provider=args.provider,
            jailbreak=args.jailbreak,
            model_path=args.model_path,
        )
        print(f"Medusa: {reply}")


if __name__ == "__main__":
    main()
