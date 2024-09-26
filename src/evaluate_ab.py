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
df = con.execute("""WITH sampled_tests AS (
    SELECT DISTINCT clickability_test_id FROM 'data/upworthy_processed.csv' USING SAMPLE 10
    )
    SELECT * FROM 'data/upworthy_processed.csv' WHERE clickability_test_id IN (SELECT clickability_test_id FROM sampled_tests)
    """).fetchdf()
# for each test
test_ids = df["clickability_test_id"].unique()
for test_id in test_ids:
    variants = df[df["clickability_test_id"] == test_id].reset_index(drop=True)

    append_chunk = ""
    for i, row in variants.iterrows():
        formatted = f"""HEADLINE: {row['text_blob']}
ID: {i}
-----
        """
        append_chunk += formatted
    print(append_chunk)

    # TODO: add to prompts
    # TODO: Update prompts with ID selection


#     format variants and add to prompt
#     run prediction
#     check if prediction is correct
#     persist correctness
