from pathlib import Path

from llms import chain_of_thought, multi_turn, reasoning_chain, single_turn


def evaluate_model(model, prompt_single, prompts_multi, system_prompt=None):
    print("Starting single-turn conversation...")
    single = single_turn(prompt_single, model, system_prompt=system_prompt)[-1][
        "content"
    ]

    if model not in ["o1-preview", "o1-mini"]:
        print("Starting multi-turn conversation...")
        multi = multi_turn(prompts_multi, model, system_prompt=system_prompt)[-1][
            "content"
        ]
        print("Starting chain of thought...")
        cot = chain_of_thought(prompt_single, model)[-1]["content"]
        print("Starting reasoning chain...")
        reasoning = reasoning_chain(prompt_single, model)[-1]["content"]
    else:
        multi = None
        cot = None
        reasoning = None

    return single, multi, cot, reasoning


if __name__ == "__main__":
    prompt_paths = [
        # Path("./src/prompts/evs"),
        Path("./src/prompts/crashes"),
        Path("./src/prompts/fruit"),
    ]

    for prompts in prompt_paths:
        with open(prompts / "single.txt", "r") as f:
            prompt_single = f.read()

        with open(prompts / "multi.txt", "r") as f:
            prompts_multi = f.read().split("=====")

        with open(prompts / "system.txt", "r") as f:
            prompt_system = f.read()

        models = [
            "gpt-4o-mini",
            "gpt-4o-2024-08-06",
            "llama3.1",
            # "o1-preview",
            # "o1-mini",
        ]

        for model in models:
            single, multi, cot, reasoning = evaluate_model(
                model, prompt_single, prompts_multi, prompt_system
            )

            output_subdir = prompts / "output" / model
            output_subdir.mkdir(exist_ok=True, parents=True)

            with open(output_subdir / "single_results.txt", "w") as f:
                f.write(single)

            with open(output_subdir / "multi_results.txt", "w") as f:
                f.write(multi)

            with open(output_subdir / "cot_results.txt", "w") as f:
                f.write(cot)

            with open(output_subdir / "reasoning_results.txt", "w") as f:
                f.write(reasoning)
