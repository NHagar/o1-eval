from pathlib import Path

import duckdb
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
    SELECT DISTINCT clickability_test_id FROM 'data/upworthy_processed.csv' USING SAMPLE 10
    )
    SELECT * FROM 'data/upworthy_processed.csv' WHERE clickability_test_id IN (SELECT clickability_test_id FROM sampled_tests)
    """).fetchdf()
# for each test
test_ids = df["clickability_test_id"].unique()

results_single = []
results_multi = []
results_cot = []
results_reasoning = []

for test_id in tqdm(test_ids):
    variants = df[df["clickability_test_id"] == test_id].reset_index(drop=True)

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
    model = "gpt-4o-mini"
    single, multi, cot, reasoning = evaluate_model(
        model, prompt_single, prompt_multi_copy, prompt_system
    )

    results_single.append(single)
    results_multi.append(multi)
    results_cot.append(cot)
    results_reasoning.append(reasoning)


print(results_single)
print(results_multi)
print(results_cot)
print(results_reasoning)

#     format variants and add to prompt
#     run prediction
#     check if prediction is correct
#     persist correctness
