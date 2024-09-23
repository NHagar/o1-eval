import pandas as pd


class StructuredDataEvaluator:
    def __init__(self, data_path, prompt_path):
        self.data_path = data_path
        self.prompt_path = prompt_path

        self.df = pd.read_csv(data_path)
        with open(prompt_path, "r") as file:
            self.prompt = file.read()
        self.prompt_steps = self.prompt.split("=====")

        self.models = ["o1-preview", "o1-mini", "gpt-4o", "gpt-4o-mini", "llama3.1"]

    def summarize_data(self):
        summary = self.df.describe()
        df_head = self.df.head()
        df_shape = self.df.shape
        df_dtypes = self.df.dtypes

        return summary, df_head, df_shape, df_dtypes
