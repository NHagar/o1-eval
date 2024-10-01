from pathlib import Path

import pandas as pd

ab_results = Path("./src/prompts/ab").rglob("*.csv")

for ab_result in ab_results:
    df = pd.read_csv(ab_result, names=["test_id", "is_correct", "response", "winner"])

    print(str(ab_result))

    print(df.is_correct.sum() / len(df) * 100)
