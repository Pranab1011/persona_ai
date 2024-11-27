from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.llms import OpenAI
from llm_config import *
import os
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
        self.example_prompt = PromptTemplate(
            input_variables=list(self.example[0].keys()),
            template="\n".join(
                [f"{key}: {{{key}}}" for key in list(self.example[0].keys())[:-1]]
            )
            + "\n Persona: {persona}",
        )

    def generate_few_shot_input(self):
        self.prompt = FewShotPromptTemplate(
            examples=self.example,
            example_prompt=self.example_prompt,
            prefix=persona_prompt_prefix,
            suffix="\n".join(
                [f"{key}: {{{key}}}" for key in list(self.example[0].keys())[:-1]]
            ),
            input_variables=[f"{key}" for key in list(self.example[0].keys())[:-1]],
        )


class PersonaGenerator:
    def __init__(self, persona_prompt: PromptGenerator):
        self.persona_prompt = persona_prompt
        self.llm = None
        self.set_up_llm()

    def set_up_llm(self):
        self.llm = OpenAI(
            temperature=0.6,
        )

    def get_persona_details(self, stats_dict: dict):
        llm_input = self.persona_prompt.prompt.format(**stats_dict)
        persona = self.llm(llm_input)
        return persona



