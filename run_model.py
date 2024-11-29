import pandas as pd
from segmentation.training.model import ModelDBSCAN


features = pd.read_csv("segmentation/data/orion_features.csv")
clustering = ModelDBSCAN(features)
clustering.prepare_training_data()
clustering.fit()
clustering.transform()
clustering.calculate_silhouette()
