#!/usr/bin/env python3
"""
CLI arkhe chat para interação local com o modelo ARKHE-OS.

Uso:
  python arkhe_chat.py
"""

import argparse
import urllib.request
import urllib.error
import json
import sys

def chat(prompt: str, server_url: str = "http://localhost:8080/completion"):
    """Envia um prompt para o servidor llama.cpp e retorna a resposta."""
    data = json.dumps({
        "prompt": prompt,
        "n_predict": 128,
        "temperature": 0.7,
        "stop": ["\n", "User:"]
    }).encode('utf-8')

    req = urllib.request.Request(server_url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("content", "")
    except urllib.error.URLError as e:
        print(f"Error connecting to server: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="ARKHE-OS Chat CLI")
    parser.add_argument("--url", default="http://localhost:8080/completion", help="llama.cpp server URL")
    args = parser.parse_args()

    print("==================================================")
    print("              ARKHE-OS Chat CLI                   ")
    print("==================================================")
    print(f"Connecting to: {args.url}")
    print("Type 'exit' or 'quit' to exit.")
    print("--------------------------------------------------")

    while True:
        try:
            prompt = input("User: ")
            if prompt.strip().lower() in ['exit', 'quit']:
                break

            if not prompt.strip():
                continue

            response = chat(prompt, server_url=args.url)
            if response is not None:
                print(f"ARKHE-OS: {response.strip()}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
