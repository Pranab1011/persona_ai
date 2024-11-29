from segmentation.feature_engineering.features import RunFeatureEngineering
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasource",
        type=str,
        help="Name of the dataset that needs to be modelled",
        required=True,
    )
    args = parser.parse_args()

    get_features = RunFeatureEngineering(args.datasource)
    features = get_features.process()

    features.to_csv(f"segmentation/data/{args.datasource}_features.csv")

    # print(features.head())
    # print("Size of data: ", features.shape)
