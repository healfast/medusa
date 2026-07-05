from medusa_agent import generate_reply


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(generate_reply(prompt))
        return

    while True:
        try:
            prompt = input("You: ")
        except EOFError:
            print()
            break
        if not prompt.strip():
            continue
        print(f"Medusa: {generate_reply(prompt)}")


if __name__ == "__main__":
    main()
