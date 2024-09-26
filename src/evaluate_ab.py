from pathlib import Path

import duckdb

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
df = con.execute(
    "SELECT * FROM 'data/upworthy_processed.csv' USING SAMPLE 10"
).fetchdf()
# for each test
test_ids = df["clickability_test_id"].unique()
for test_id in test_ids:
    variants = df[df["clickability_test_id"] == test_id].reset_index(drop=True)

    append_chunk = ""
    for i, row in variants.iterrows():
        formatted = ""


#     format variants and add to prompt
#     run prediction
#     check if prediction is correct
#     persist correctness
