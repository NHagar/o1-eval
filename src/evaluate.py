from pathlib import Path

from llms import chain_of_thought, multi_turn, reasoning_chain, single_turn


def evaluate_model(model, prompt_single, prompts_multi, system_prompt=None):
    single = single_turn(prompt_single, model, system_prompt=system_prompt)[-1][
        "content"
    ]

    if model not in ["o1-preview", "o1-mini"]:
        multi = multi_turn(prompts_multi, model, system_prompt=system_prompt)[-1][
            "content"
        ]
        cot = chain_of_thought(prompt_single, model)[-1]["content"]
        reasoning = reasoning_chain(prompt_single, model)[-1]["content"]
    else:
        multi = None
        cot = None
        reasoning = None

    return single, multi, cot, reasoning


if __name__ == "__main__":
    model = "gpt-4o-mini"
    prompts = Path("./src/prompts/evs")

    with open(prompts / "single.txt", "r") as f:
        prompt_single = f.read()

    with open(prompts / "multi.txt", "r") as f:
        prompts_multi = f.read().split("=====")

    with open(prompts / "system.txt", "r") as f:
        prompt_system = f.read()

    single, multi, cot, reasoning = evaluate_model(
        model, prompt_single, prompts_multi, prompt_system
    )

    with open(prompts / "single_results.txt", "w") as f:
        f.write(single)

    with open(prompts / "multi_results.txt", "w") as f:
        f.write(multi)

    with open(prompts / "cot_results.txt", "w") as f:
        f.write(cot)

    with open(prompts / "reasoning_results.txt", "w") as f:
        f.write(reasoning)
