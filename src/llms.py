from typing import List

import ollama
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def single_turn(
    user_prompt: str,
    model: str,
    system_prompt: str | None = None,
    history: List | None = None,
) -> List:
    """
    Generate a single-turn response from a language model.

    Args:
        user_prompt (str): The user's input prompt.
        model (str): The name of the language model to use.
        system_prompt (str | None, optional): An optional system prompt. Defaults to None.
        history (List | None, optional): A list of previous message exchanges. Defaults to None.

    Returns:
        List: The conversation history including the user input and model response.
    """
    if history is not None:
        messages = history + [{"role": "user", "content": user_prompt}]
    elif system_prompt is None:
        messages = [{"role": "user", "content": user_prompt}]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    if model == "llama3.1":
        resp = ollama.chat(model=model, messages=messages)
        resp_text = resp["message"]["content"]
    else:
        resp = OpenAI().chat.completions.create(model=model, messages=messages)
        resp_text = resp.choices[0].message.content

    messages.append({"role": "assistant", "content": resp_text})

    return messages


def multi_turn(
    user_prompts: List[str], model: str, system_prompt: str | None = None
) -> List:
    """
    Generate multi-turn responses from a language model.

    Args:
        user_prompts (List[str]): A list of user input prompts.
        model (str): The name of the language model to use.
        system_prompt (str | None, optional): An optional system prompt. Defaults to None.

    Returns:
        List: The conversation history including both user inputs and model responses.
    """
    history = []
    for user_prompt in user_prompts:
        if len(history) == 0:
            resp = single_turn(user_prompt, model, system_prompt=system_prompt)
        else:
            resp = single_turn(user_prompt, model, history=history)
        history.extend(resp)

    return history
