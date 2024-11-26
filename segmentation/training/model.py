from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np
from training_utils import *


class ModelDBSCAN:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.config = load_train_config()

    def prepare_training_data(self):
        # Step 2: Standardize only the numerical features
        scaler = StandardScaler()
        numerical_scaled = scaler.fit_transform(
            self.data[self.config.get("numerical_features")]
        )

        # Step 3: Concatenate scaled numerical features and one-hot-encoded features
        self.X_preprocessed = np.hstack(
            [
                numerical_scaled,
                self.data[self.config.get("one_hot_encoded_features")].values,
            ]
        )

        # Optional: Convert back to DataFrame for better readability
        final_columns = self.config.get("numerical_features") + self.config.get(
            "one_hot_encoded_features"
        )
        self.X_preprocessed_df = pd.DataFrame(
            self.X_preprocessed, columns=final_columns
        )

    def fit(self):
        dbscan = DBSCAN(
            eps=self.config.get("eps"), min_samples=self.config.get("min_samples")
        )
        self.dbscan_labels = dbscan.fit_predict(self.X_preprocessed)

    def transform(self):
        self.data["db_cluster"] = self.dbscan_labels

    def calculate_silhouette(self):
        non_noise_data = self.X_preprocessed[self.dbscan_labels != -1]
        non_noise_labels = self.dbscan_labels[self.dbscan_labels != -1]

        if len(set(non_noise_labels)) > 1:  # Ensure there are at least 2 clusters
            silhouette = silhouette_score(non_noise_data, non_noise_labels)
            print(f"Silhouette Score (excluding noise): {silhouette}")
        else:
            print(
                "Silhouette score cannot be computed as there are fewer than 2 clusters."
            )
