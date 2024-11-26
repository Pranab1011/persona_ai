import pandas as pd

from abstract import BaseFeatureEngineer
from features_utils import *


class FeatureEngineer(BaseFeatureEngineer):
    def __init__(
        self,
        data: pd.DataFrame,
        purchase_window_months: int,
        purchase_window_weeks: int,
    ):
        self.data = data
        self.n_months = purchase_window_months
        self.n_weeks = purchase_window_weeks
        self.config = load_features_config()

    def get_latest_purchase_date(self):
        latest_purchase = (
            self.data.groupby("customer_id")["purchase_date"].max().reset_index()
        )
        latest_purchase.columns = ["customer_id", "latest_purchase_date"]
        self.data = self.data.merge(latest_purchase, on="customer_id")
        self.data["latest_purchase_date"] = pd.to_datetime(
            self.data["latest_purchase_date"]
        )

    def get_n_months_cutoff(self):
        self.data["three_month_cutoff"] = self.data[
            "latest_purchase_date"
        ] - pd.DateOffset(months=self.n_months)

    def get_last_n_months_total_purchase_amount(self):
        self.get_latest_purchase_date()
        self.get_n_months_cutoff(self.n_months)
        data_last_n_months = self.data[
            self.data["purchase_date"] >= self.data[f"{self.n_months}_month_cutoff"]
        ]
        total_purchase_last_n_months = (
            data_last_n_months.groupby("customer_id")["total_purchase_amount"]
            .sum()
            .reset_index()
        )
        total_purchase_last_n_months.columns = [
            "customer_id",
            f"total_purchase_last_{self.n_months}_months",
        ]
        self.data = self.data.merge(
            total_purchase_last_n_months, on="customer_id", how="left"
        )

    def get_last_n_months_avg_purchase_amount(self):
        data_last_n_months = self.data[
            self.data["purchase_date"] >= self.data[f"{self.n_months}_month_cutoff"]
        ]
        avg_purchase_last_n_months = (
            data_last_n_months.groupby("customer_id")["total_purchase_amount"]
            .mean()
            .reset_index()
        )
        avg_purchase_last_n_months.columns = [
            "customer_id",
            f"avg_purchase_last_{self.n_months}_months",
        ]
        self.data = self.data.merge(
            avg_purchase_last_n_months, on="customer_id", how="left"
        )

    def assign_month(self, row):
        if row["purchase_date"] > row["month_1_start"]:
            return "month_1"
        elif row["month_2_start"] < row["purchase_date"] <= row["month_1_start"]:
            return "month_2"
        elif row["month_3_end"] < row["purchase_date"] <= row["month_2_start"]:
            return "month_3"
        else:
            return None

    def get_last_n_months_purchase_amount_by_month(self):
        self.data["latest_purchase_date"] = pd.to_datetime(
            self.data["latest_purchase_date"]
        )

        for i in range(1, self.n_months + 1):
            self.data[f"month_{i}_start"] = self.data[
                "latest_purchase_date"
            ] - pd.DateOffset(months=i)
            if i < self.n_months:
                self.data[f"month_{i}_end"] = self.data[
                    f"month_{i + 1}_start"
                ] - pd.Timedelta(days=1)
            else:
                self.data[f"month_{i}_end"] = (
                    self.data["latest_purchase_date"]
                    - pd.DateOffset(months=self.n_months)
                    - pd.Timedelta(days=1)
                )

        for i in range(1, self.n_months + 1):
            self.data[f"month_{i}_start"] = self.data[f"month_{i}_start"].astype(str)
            self.data[f"month_{i}_end"] = self.data[f"month_{i}_end"].astype(str)

        self.data["purchase_month"] = self.data.apply(self.assign_month, axis=1)

        monthly_totals = self.data.pivot_table(
            index="customer_id",
            columns="purchase_month",
            values="total_purchase_amount",
            aggfunc="sum",
        ).reset_index()

        column_rename_map = {
            f"month_{i}": f"purchase_month_{i}" for i in range(1, self.n_months + 1)
        }
        monthly_totals = monthly_totals.rename(columns=column_rename_map)

        monthly_totals = monthly_totals.fillna(0)

        self.data = self.data.merge(monthly_totals, on="customer_id", how="left")

    def assign_week(self, row):
        if row["purchase_date"] > row["week_1_start"]:
            return "week_1"
        elif row["week_2_start"] < row["purchase_date"] <= row["week_1_start"]:
            return "week_2"
        elif row["week_3_start"] < row["purchase_date"] <= row["week_2_start"]:
            return "week_3"
        elif row["week_4_end"] < row["purchase_date"] <= row["week_3_start"]:
            return "week_4"
        else:
            return None

    def get_last_n_weeks_purchase_amount_by_week(self):
        self.data["latest_purchase_date"] = pd.to_datetime(
            self.data["latest_purchase_date"]
        )

        for i in range(1, self.n_weeks + 1):
            self.data[f"week_{i}_start"] = self.data[
                "latest_purchase_date"
            ] - pd.DateOffset(weeks=i)
            if i < self.n_weeks:
                self.data[f"week_{i}_end"] = self.data[
                    f"week_{i + 1}_start"
                ] - pd.Timedelta(days=1)
            else:
                self.data[f"week_{i}_end"] = (
                    self.data["latest_purchase_date"]
                    - pd.DateOffset(months=self.n_weeks)
                    - pd.Timedelta(days=1)
                )

        for i in range(1, self.n_weeks + 1):
            self.data[f"week_{i}_start"] = self.data[f"week_{i}_start"].astype(str)
            self.data[f"week_{i}_end"] = self.data[f"week_{i}_end"].astype(str)

        self.data["purchase_week"] = self.data.apply(self.assign_week, axis=1)

        weekly_totals = self.data.pivot_table(
            index="customer_id",
            columns="purchase_week",
            values="total_purchase_amount",
            aggfunc="sum",
        ).reset_index()

        column_rename_map = {
            f"week_{i}": f"purchase_week_{i}" for i in range(1, self.n_weeks + 1)
        }
        weekly_totals = weekly_totals.rename(columns=column_rename_map)

        weekly_totals = weekly_totals.fillna(0)

        self.data = self.data.merge(weekly_totals, on="customer_id", how="left")

    def get_category_counts(self):
        category_counts = (
            self.data.groupby(["customer_id", "product_category"])["quantity"]
            .sum()
            .reset_index()
        )

        category_wise_items = category_counts.pivot(
            index="customer_id", columns="product_category", values="quantity"
        ).reset_index()

        # Fill NaN with 0 for categories with no purchases
        category_wise_items = category_wise_items.fillna(0)

        # Rename columns for clarity (optional)
        category_wise_items.columns.name = None  # Remove the multi-level column name
        category_wise_items = category_wise_items.rename(
            columns=lambda x: f"category_{x}" if x != "customer_id" else x
        )

        self.data = self.data.merge(category_wise_items, on="customer_id", how="left")

    def get_most_common_payment_method(self):
        payment_counts = (
            self.data.groupby("customer_id")["payment_method"]
            .value_counts()
            .reset_index(name="count")
        )
        most_common_payment = payment_counts.sort_values(
            by=["customer_id", "count"], ascending=[True, False]
        ).drop_duplicates(subset="customer_id")
        most_common_payment = most_common_payment.rename(
            columns={"payment_method": "most_common_payment_method"}
        )
        self.data = self.data.merge(
            most_common_payment[["customer_id", "most_common_payment_method"]],
            on="customer_id",
            how="left",
        )

    def one_hot_encode_columns(self, columns_to_encode):
        """One-hot encodes specified columns in a DataFrame."""

        self.data = self.data.copy()  # Create a copy to avoid modifying the original DataFrame

        for col in columns_to_encode:
            if col in self.data.columns:
                dummies = pd.get_dummies(self.data[col], prefix=col, dummy_na=False)
                self.data = pd.concat([self.data, dummies], axis=1)
                self.data = self.data.drop(col, axis=1)  # Remove original column
            else:
                print(f"Warning: Column '{col}' not found in the DataFrame.")

    def fit(self):
        self.get_last_n_months_avg_purchase_amount()
        self.get_last_n_months_purchase_amount_by_month()
        self.get_last_n_weeks_purchase_amount_by_week()
        self.get_category_counts()
        self.get_most_common_payment_method()
        self.one_hot_encode_columns(self.config.get('columns_to_encode'))

    def transform(self) -> pd.DataFrame:
        columns_to_use = self.config.get('columns_to_use')
        return self.data[columns_to_use]

    def get_feature_names(self) -> list:
        pass
