import pandas as pd


# Load and preprocess data
def load_data(file_path):
    """Load and preprocess the dataset."""
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.lower().str.replace(
        " ", "_"
    )  # Standardize column names
    return data


# Load yaml file
def load_yaml(filepath):
    """
    Load a YAML file using pyaml.
    Parameters:
    - filepath (str): The path to the YAML file.

    Returns:
    - dict: Parsed YAML content as a Python dictionary.
    """
    with open(filepath, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content


def load_train_config():
    return load_yaml("orion_training_config.yaml")
