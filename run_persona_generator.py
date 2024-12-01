import pandas as pd
from segmentation.inferencing.agent_inference.persona_generator import (
    PromptGenerator,
    PersonaGenerator,
    parse_persona,
)
from tqdm import tqdm
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

    segments_stats = pd.read_csv(f"segmentation/data/{args.datasource}_segments.csv")
    segments_stats = segments_stats[segments_stats["db_cluster"] != -1]
    segments_stats = segments_stats.drop("db_cluster", axis=1)

    persona_gen = PersonaGenerator(PromptGenerator(datasource=args.datasource))
    persona_list = []

    for i in tqdm(range(segments_stats.shape[0])):
        persona_str = persona_gen.get_persona_details(
            segments_stats.iloc[1, :].to_dict()
        )
        persona_json = parse_persona(persona_str.content)
        persona_list.append(persona_json)

    persona_df = pd.DataFrame(persona_list)
    persona_df.to_csv(f"segmentation/data/{args.datasource}_personas.csv")
