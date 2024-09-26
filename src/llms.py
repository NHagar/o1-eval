import json
from enum import Enum
from typing import List

import ollama
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class NextActionEnum(str, Enum):
    cont = "continue"
    final_answer = "final_answer"


class ReasoningChainStep(BaseModel):
    title: str
    content: str
    next_action: NextActionEnum


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


def chain_of_thought(user_prompt: str, model: str) -> List:
    cot_prompt = """You are an AI assistant that uses a Chain of Thought (CoT) approach with reflection to answer queries. Follow these steps:

            1. Think through the problem step by step within the <thinking> tags.
            2. Reflect on your thinking to check for any errors or improvements within the <reflection> tags.
            3. Make any necessary adjustments based on your reflection.
            4. Provide your final, concise answer within the <output> tags.

            Important: The <thinking> and <reflection> sections are for your internal reasoning process only.
            Do not include any part of the final answer in these sections.
            The actual response to the query must be entirely contained within the <output> tags.

            Use the following format for your response:
            <thinking>
            [Your step-by-step reasoning goes here. This is your internal thought process, not the final answer.]
            <reflection>
            [Your reflection on your reasoning, checking for errors or improvements]
            </reflection>
            [Any adjustments to your thinking based on your reflection]
            </thinking>
            <output>
            [Your final, concise answer to the query. This is the only part that will be shown to the user.]
            </output>
            """

    resp = single_turn(user_prompt, model, system_prompt=cot_prompt)

    return resp


def reasoning_chain(user_prompt: str, model: str):
    history = [
        {
            "role": "system",
            "content": """You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title that describes what you're doing in that step, along with the content. Decide if you need another step or if you're ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys. USE AS MANY REASONING STEPS AS POSSIBLE. AT LEAST 3. BE AWARE OF YOUR LIMITATIONS AS AN LLM AND WHAT YOU CAN AND CANNOT DO. IN YOUR REASONING, INCLUDE EXPLORATION OF ALTERNATIVE ANSWERS. CONSIDER YOU MAY BE WRONG, AND IF YOU ARE WRONG IN YOUR REASONING, WHERE IT WOULD BE. FULLY TEST ALL OTHER POSSIBILITIES. YOU CAN BE WRONG. WHEN YOU SAY YOU ARE RE-EXAMINING, ACTUALLY RE-EXAMINE, AND USE ANOTHER APPROACH TO DO SO. DO NOT JUST SAY YOU ARE RE-EXAMINING. USE AT LEAST 3 METHODS TO DERIVE THE ANSWER. USE BEST PRACTICES.

    Example of a valid JSON response:
    ```json
    {
        "title": "Identifying Key Information",
        "content": "To begin solving this problem, we need to carefully examine the given information and identify the crucial elements that will guide our solution process. This involves...",
        "next_action": "continue"
    }```
    """,
        },
        {"role": "user", "content": user_prompt},
        {
            "role": "assistant",
            "content": "Thank you! I will now think step by step following my instructions, starting at the beginning after decomposing the problem.",
        },
    ]

    step_count = 1

    while True:
        if model == "llama3.1":
            resp = ollama.chat(model=model, messages=history)
            resp_text = resp["message"]["content"]
        else:
            llm = OpenAI()
            resp = llm.beta.chat.completions.parse(
                model=model, messages=history, response_format=ReasoningChainStep
            )

            resp_text = resp.choices[0].message.content

        try:
            step_data = json.loads(resp_text)
        except json.JSONDecodeError:
            step_data = {
                "title": f"Step {step_count} (JSON DECODING ERROR)",
                "content": resp_text,
                "next_action": "final_answer",
            }

        history.append({"role": "assistant", "content": json.dumps(step_data)})

        if step_data["next_action"] == "final_answer" or step_count > 25:
            break

        step_count += 1

    final_data = single_turn(
        "Please provide the final answer based on your reasoning above.",
        model,
        history=history,
    )

    return final_data
