import pandas as pd
#
# df = pd.read_csv("segmentation/data/orion_personas.csv")
#
# print(df.iloc[0, :].to_dict())


# from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAI

# llm = OpenAI(temperature=0.9)
# prompt = llm("Generate a detailed prompt of length less than 1000 characters to generate an image of marketing persona of online retail customer based on the following description.: Persona Title: Mature Knowledge Seeker")
# image_url = DallEAPIWrapper().run(
#     "A marketing persona for online retail on the title 'Mature Bookworm Shopper'"
# )
#
# print(image_url)
persona_groupings = {
    "demogrophics": ["Name", "Age", "Gender", "Occupation", "Income"],
    "behavioral_traits": [
        "Purchase Habits",
        "Category Insights",
        "Additional Adoption Notes",
    ],
    "psychographics": ["Lifestyle", "Motivations", "Pain Points"],
    "marketing_strategy": [
        "Target Channels",
        "Messaging",
        "Product Recommendations",
        "Engagement",
    ],
    "taglines": ["taglines"],
}

persona_df = pd.read_csv("segmentation/data/orion_personas.csv")


def generate_persona_json(persona_df):
    personas = {}
    for i in range(persona_df.shape[0]):
        persona_dict = persona_df.iloc[i, :]
        this_persona = {}
        for key, value in persona_groupings.items():
            this_persona[key] = {item: persona_dict.get(item) for item in value}

        this_persona["image"] = "personas/data/images/Tech-Savvy-Power-Shopper.png"
        personas[persona_dict.get("persona_name")] = this_persona

    return personas


# personas = generate_persona_json(persona_df)
print(persona_df.iloc[0, :])
