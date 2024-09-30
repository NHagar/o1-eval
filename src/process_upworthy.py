import duckdb

con = duckdb.connect(database=":memory:")

# clickability_test_id - more than 1 record
# excerpt + headline + share_text
# text blob - more than 1 unique record
df = con.execute("""
    WITH variants AS (
        SELECT
            clickability_test_id,
            COUNT(*) AS variant_count,
            SUM(CAST(winner AS INTEGER)) AS winner_count
        FROM
            './data/upworthy.csv'
        GROUP BY
            1
    ),
    multi_variants AS (
    SELECT
        d.clickability_test_id,
        COALESCE(excerpt, '') || '\n' || COALESCE(headline, '') || '\n' || COALESCE(share_text, '') AS text_blob,
        winner
    FROM
        './data/upworthy.csv' d
    JOIN
        variants
    ON
        variants.clickability_test_id = d.clickability_test_id
    WHERE
        variants.variant_count > 1
        AND variants.winner_count = 1
    ),
    unique_text_blob AS (
    SELECT
        clickability_test_id,
        COUNT(DISTINCT text_blob) AS unique_text_blob_count
    FROM
        multi_variants
    GROUP BY
        1
    )
    SELECT
        m.*
    FROM
        multi_variants m
    JOIN
        unique_text_blob
    ON
        m.clickability_test_id = unique_text_blob.clickability_test_id
    WHERE
        unique_text_blob_count > 1
""").fetchdf()

df.to_csv("./data/upworthy_processed.csv", index=False)

print(len(df))
print(df.clickability_test_id.nunique())
