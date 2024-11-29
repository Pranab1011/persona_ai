from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from .llm_config import *
import ast
import warnings

warnings.filterwarnings("ignore")


class PromptGenerator:
    def __init__(self, datasource: str):
        self.datasource = datasource
        self.example = prompt_example_mapping.get(self.datasource)
        self.example_prompt = None
        self.prompt = None
        self.generate_example_prompt()
        self.generate_few_shot_input()

    def generate_example_prompt(self):
        self.example_prompt = ChatPromptTemplate.from_messages(
            [("human", "{input}"), ("ai", "{output}")]
        )

    def generate_few_shot_input(self):
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=self.example_prompt,
            examples=prompt_example_mapping.get(self.datasource),
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [("system", persona_prompt_prefix), few_shot_prompt, ("human", "{input}")]
        )


class PersonaGenerator:
    def __init__(self, persona_prompt: PromptGenerator):
        self.persona_prompt = persona_prompt
        self.chain = None
        self.set_up_llm()

    def set_up_llm(self):
        self.chain = self.persona_prompt.prompt | ChatOpenAI(model_name='gpt-4')

    def get_persona_details(self, stats_dict: dict):
        persona = self.chain.invoke({"input": str(stats_dict)})
        return persona


def parse_persona(persona_str: str) -> dict:
    persona_str = persona_str.replace("/", "")  # Remove slashes
    persona_str = persona_str.replace("Persona:", "")  # Remove "Persona:" label
    persona_str = persona_str.replace("'", '"')
    persona_str = persona_str.strip()
    persona_str = "{" + persona_str + "}"

    persona_dict = ast.literal_eval(persona_str)
    return persona_dict
