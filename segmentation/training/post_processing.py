from training_utils import *
import pandas as pd


class ClusterStats:
    def __init__(self, clustered_data: pd.DataFrame):
        self.clustered_data = clustered_data
        self.config = load_train_config()

    def calculate_stats(self, label_column: str):
        averages = self.clustered_data.groupby(label_column)[
            self.config.get("avg_columns")
        ].mean()
        sums = self.clustered_data.groupby(label_column)[
            self.config.get("sum_columns")
        ].sum()

        aggregates = pd.concat([averages, sums], axis=1).reset_index()

        range_stats_df = []
        for col in self.config.get("range_columns"):
            range_stats = self.clustered_data.groupby(label_column)[col].agg(
                age_range=lambda x: f"{x.min()}-{x.max()}"
            )
            range_stats_df.append(range_stats)

        ranges = pd.concat(range_stats_df, axis=1).reset_index()

        final_df = aggregates.merge(ranges, on=label_column, how="left")

        return final_df
