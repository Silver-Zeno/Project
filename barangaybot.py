from ollama import Client


def main():
    client = Client()
    print("Barangaybot: I'm Barangaybot, your virtual assistant! (Type 'exit' to quit.)\n")

    while True:
        prompt = input("You: ")
        if prompt.lower() in {"exit", "quit"}:
            break

        try:
            response = client.chat(
                model="barangaybot",
                messages=[{"role": "user", "content": prompt}],
            )
            print("\nBarangaybot:", response["message"]["content"], "\n")
        except Exception as exc:  # keep CLI from crashing on model errors
            print("\nError talking to Barangaybot:", exc, "\n")


if __name__ == "__main__":
    main()
