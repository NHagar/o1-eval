import pandas as pd


def describe_input_data(csv):
    df = pd.read_csv(csv)
    data_head = df.head()
    data_head = data_head.to_csv()

    data_shape = df.shape
    data_shape = f"Rows: {data_shape[0]}, Columns: {data_shape[1]}"

    data_description = df.describe()
    data_description = data_description.to_csv()

    data_dtypes = df.dtypes
    data_dtypes = data_dtypes.to_csv()

    output = "DATA INFORMATION:\n"
    output += f"Table: {csv}\n"
    output += f"Table head:\n{data_head}\n"
    output += f"Table shape:\n{data_shape}\n"
    output += f"Table description:\n{data_description}\n"
    output += f"Table data types:\n{data_dtypes}\n"
    output += "\n"

    return output


print(describe_input_data("./data/banklist.csv"))
