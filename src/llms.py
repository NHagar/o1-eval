import ollama
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def single_turn(user_prompt, model, system_prompt=None):
    if system_prompt is None:
        messages = [
            {"role": "user", "content": user_prompt}
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    if model == "llama3.1":
        resp = ollama.chat(
            model=model,
            messages=messages
        )
        resp_text = resp["message"]["content"]
    else:
        resp = OpenAI().chat.completions.create(
            model=model,
            messages=messages
        )
        resp_text = resp.choices[0].message.content

    return resp_text
