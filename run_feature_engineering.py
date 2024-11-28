from segmentation.feature_engineering.features import RunFeatureEngineering


get_features = RunFeatureEngineering('orion')
features = get_features.process()

print(features.head())
print("Size of data: ", features.shape)
