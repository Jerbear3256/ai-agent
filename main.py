import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse


def main():


    # Load key from .env file
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")


    # Initialize OpenAI client with the API key
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    prompt = args.user_prompt
    messages = [
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    if response.usage is None:
        raise RuntimeError("Response usage is None. Unable to retrieve token usage information.")

    if args.verbose:
        # Print the prompt and token usage information if verbose tag is set
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    # Otherwise, always print the response content
    print(f"Response:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
