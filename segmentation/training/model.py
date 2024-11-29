from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np
from joblib import Parallel, delayed
from sklearn.metrics import pairwise_distances
from .training_utils import *
from ..common_utils import *
import time


class ModelDBSCAN:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.config = load_train_config()
        self.logger = setup_logger()

    def prepare_training_data(self):
        # Step 2: Standardize only the numerical features
        scaler = StandardScaler()
        numerical_scaled = scaler.fit_transform(
            self.data[self.config.get("numerical_features")]
        )

        self.logger.info("Numerical features were scaled")

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

        self.logger.info("Training data is prepared.")

    def compute_distances(self, X):
        return pairwise_distances(X, metric="euclidean", n_jobs=-1)

    def fit(self):
        self.logger.info("Starting computing distance")
        compute_distance_start_time = time.time()

        distance_matrix = self.compute_distances(self.X_preprocessed)

        compute_distance_end_time = time.time()
        duration = compute_distance_end_time - compute_distance_start_time
        self.logger.info(
            f"Pairwise distances are computed. Time taken: {duration} seconds"
        )

        self.logger.info("Starting model training")
        training_start_time = time.time()

        dbscan = DBSCAN(
            eps=self.config.get("eps"),
            min_samples=self.config.get("min_samples"),
            metric="precomputed",
        )
        self.dbscan_labels = dbscan.fit_predict(distance_matrix)

        training_end_time = time.time()
        duration = training_end_time - training_start_time
        self.logger.info(f"Model is trained. Time taken to train model {duration}")

    def transform(self):
        self.data["db_cluster"] = self.dbscan_labels

    def calculate_silhouette(self):
        self.logger.info("Calculating Silhouette Score")
        non_noise_data = self.X_preprocessed[self.dbscan_labels != -1]
        non_noise_labels = self.dbscan_labels[self.dbscan_labels != -1]

        if len(set(non_noise_labels)) > 1:  # Ensure there are at least 2 clusters
            silhouette = silhouette_score(non_noise_data, non_noise_labels)
            self.logger.info("Silhouette Score Calculated")
            print(f"Silhouette Score (excluding noise): {silhouette}")
        else:
            print(
                "Silhouette score cannot be computed as there are fewer than 2 clusters."
            )
