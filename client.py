#!/usr/bin/env python3

""" 
A simple client that can query the translation server
"""

import json
import requests

SERVER_IP="127.0.0.1"
SERVER_PORT=7890
SERVER_URL=f"http://{SERVER_IP}:{str(SERVER_PORT)}/translate"


def send_translation(input_text, input_language, output_language, model="default"):
    json_frame = {
        'input_language': input_language,
        'output_language': output_language,
        'input_text': input_text,
        'translation_model': model}

    r = requests.post(SERVER_URL, json=json_frame)
    return json.loads(r.text)


def screen_reader():
    print("[¤] Welcome to terminal translation client")
    try:
        requests.post(SERVER_URL)
    except:
        print("[¤] Server is not up, edit server variables")
        exit(1)
    print("[¤] Select input and output language, has to be 2 letter iso code")
    input_language = input("\tInput language: ")
    output_language = input("\tOutput language: ")
    try:
        while True:
            input_text = input("\tText to translate: ")
            result = send_translation(input_text, input_language, output_language)
            if not result["translated_text"]:
                print("\n[X]: ", result["msg"])
                exit(1)
            print(result["translated_text"], "\n")
    except KeyboardInterrupt:
        print("\n\t[¤] Goodbye")
        exit(0)
def main():
    screen_reader()

if __name__ == "__main__":
    main()
