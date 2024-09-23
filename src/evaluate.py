from llms import chain_of_thought, multi_turn, reasoning_chain, single_turn


def evaluate_model(model, prompt_single, prompts_multi, system_prompt=None):
    single = single_turn(prompt_single, model)

    if model not in ["o1-preview", "o1-mini"]:
        multi = multi_turn(prompts_multi, model)
        cot = chain_of_thought(prompt_single, model)
        reasoning = reasoning_chain(prompt_single, model)
    else:
        multi = None
        cot = None
        reasoning = None

    return single, multi, cot, reasoning
