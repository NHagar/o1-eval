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
# load sample of upworthy data
df = con.execute("""WITH sampled_tests AS (
    SELECT DISTINCT clickability_test_id FROM 'data/upworthy_processed.csv' USING SAMPLE 2
    )
    SELECT * FROM 'data/upworthy_processed.csv' WHERE clickability_test_id IN (SELECT clickability_test_id FROM sampled_tests)
    """).fetchdf()
# for each test
test_ids = df["clickability_test_id"].unique()

results_single = []
results_multi = []
results_cot = []
results_reasoning = []


def process_model_response(response, winning_idx):
    if isinstance(response, dict):
        if "Headline ID" in response:
            resp_id = int(response["Headline ID"])
        elif "content" in response:
            try:
                resp_id = int(response["content"].split("ID: ")[1].split("\n")[0])
            except (IndexError, ValueError):
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


model = "llama3.1"

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

    # # run prediction
    single, multi, cot, reasoning = evaluate_model(
        model, prompt_single, prompt_multi_copy, prompt_system
    )

    results_single.append(
        {
            "is_correct": process_model_response(single, winning_idx),
            "response": single,
            "winner": winning_idx,
        }
    )
    results_multi.append(
        {
            "is_correct": process_model_response(multi, winning_idx),
            "response": multi,
            "winner": winning_idx,
        }
    )
    results_cot.append(
        {
            "is_correct": process_model_response(cot, winning_idx),
            "response": cot,
            "winner": winning_idx,
        }
    )
    results_reasoning.append(
        {
            "correct": process_model_response(reasoning, winning_idx),
            "response": reasoning,
            "winner": winning_idx,
        }
    )

output_path = prompts_path / "output" / model
output_path.mkdir(exist_ok=True, parents=True)

pd.DataFrame(results_single).to_csv(output_path / "single_results.csv", index=False)
pd.DataFrame(results_multi).to_csv(output_path / "multi_results.csv", index=False)
pd.DataFrame(results_cot).to_csv(output_path / "cot_results.csv", index=False)
pd.DataFrame(results_reasoning).to_csv(
    output_path / "reasoning_results.csv", index=False
)
