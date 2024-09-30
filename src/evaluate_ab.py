from pathlib import Path

import duckdb
import pandas as pd
from tqdm import tqdm

from evaluate_data import evaluate_model

# load prompts
prompts_path = Path("./src/prompts/ab")

with open(prompts_path / "single.txt", "r") as f:
    prompt_single = f.read()

with open(prompts_path / "multi.txt", "r") as f:
    prompt_multi = f.read()

with open(prompts_path / "system.txt", "r") as f:
    prompt_system = f.read()

con = duckdb.connect(database=":memory:")

# check if test ID path exists
if not Path("./data/sample_ids.csv").exists():
    # load sample of upworthy data
    df = con.execute("""WITH sampled_tests AS (
        SELECT DISTINCT clickability_test_id FROM 'data/upworthy_processed.csv' USING SAMPLE 50
        )
        SELECT * FROM 'data/upworthy_processed.csv' WHERE clickability_test_id IN (SELECT clickability_test_id FROM sampled_tests)
        """).fetchdf()
    # for each test
    test_ids = df["clickability_test_id"].unique()

    pd.DataFrame(test_ids, columns=["test_id"]).to_csv(
        "./data/sample_ids.csv", index=False
    )
else:
    test_ids = pd.read_csv("./data/sample_ids.csv")["test_id"].tolist()
    df = con.execute(
        """SELECT * FROM 'data/upworthy_processed.csv' WHERE clickability_test_id IN (SELECT test_id FROM 'data/sample_ids.csv')"""
    ).fetchdf()


def process_model_response(response, winning_idx):
    if isinstance(response, dict):
        if "Headline ID" in response:
            resp_id = int(response["Headline ID"])
        elif "content" in response:
            try:
                resp_id = int(response["content"].split("ID: ")[1].split("\n")[0])
            except (IndexError, ValueError, AttributeError):
                return None
        else:
            return None
    else:
        try:
            resp_id = int(response.split("ID: ")[1].split("\n")[0])
        except (IndexError, ValueError):
            return None

    if resp_id == winning_idx:
        correct = True
    else:
        correct = False

    return correct


def check_for_results(res_path):
    if not res_path.exists():
        return pd.DataFrame(columns=["test_id", "is_correct", "response", "winner"])
    else:
        return pd.read_csv(
            res_path,
            names=["test_id", "is_correct", "response", "winner"],
        )


models = [
    "gpt-4o-mini",
    "llama3.1",
    "gpt-4o-2024-08-06",
    "o1-mini",
    "o1-preview",
]

for model in models:
    output_path = prompts_path / "output" / model
    output_path.mkdir(parents=True, exist_ok=True)

    results_single = check_for_results(output_path / "single_results.csv")
    results_multi = check_for_results(output_path / "multi_results.csv")
    results_cot = check_for_results(output_path / "cot_results.csv")
    results_reasoning = check_for_results(output_path / "reasoning_results.csv")

    test_ids = [i for i in test_ids if i not in results_single.test_id.tolist()]

    print(f"Running evaluation for model: {model}")
    for test_id in tqdm(test_ids):
        variants = df[df["clickability_test_id"] == test_id]
        # randomly shuffle variants
        variants = variants.sample(frac=1)
        variants.reset_index(drop=True, inplace=True)
        # store index of winning variant
        winning_idx = variants[variants["first_place"]].index[0]

        append_chunk = ""
        for i, row in variants.iterrows():
            formatted = f"""ID: {i}
    HEADLINE: {row['text_blob']}
    -----
            """
            append_chunk += formatted

        prompt_single += append_chunk

        prompt_multi_copy = prompt_multi
        prompt_multi_copy = prompt_multi_copy.split("=====")
        prompt_multi_copy[0] += append_chunk

        # run prediction
        if model in ["o1-mini", "o1-preview"]:
            prompt_system = None

        single, multi, cot, reasoning = evaluate_model(
            model, prompt_single, prompt_multi_copy, prompt_system
        )

        # write or append rows to corresponding CSVs
        pd.DataFrame(
            [
                {
                    "test_id": test_id,
                    "is_correct": process_model_response(single, winning_idx),
                    "response": single,
                    "winner": winning_idx,
                }
            ]
        ).to_csv(
            output_path / "single_results.csv", mode="a", header=False, index=False
        )

        if model not in ["o1-mini", "o1-preview"]:
            pd.DataFrame(
                [
                    {
                        "test_id": test_id,
                        "is_correct": process_model_response(multi, winning_idx),
                        "response": multi,
                        "winner": winning_idx,
                    }
                ]
            ).to_csv(
                output_path / "multi_results.csv", mode="a", header=False, index=False
            )

            pd.DataFrame(
                [
                    {
                        "test_id": test_id,
                        "is_correct": process_model_response(cot, winning_idx),
                        "response": cot,
                        "winner": winning_idx,
                    }
                ]
            ).to_csv(
                output_path / "cot_results.csv", mode="a", header=False, index=False
            )

            pd.DataFrame(
                [
                    {
                        "test_id": test_id,
                        "is_correct": process_model_response(reasoning, winning_idx),
                        "response": reasoning,
                        "winner": winning_idx,
                    }
                ]
            ).to_csv(
                output_path / "reasoning_results.csv",
                mode="a",
                header=False,
                index=False,
            )
