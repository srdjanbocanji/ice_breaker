from dotenv import load_dotenv
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup

load_dotenv(override=True)
if __name__ == "__main__":
   summary_template = """
   given the Linkedin information {information} about a person from I want you to create:
   1. a short summary
   2. two interesting facts about them
   """

   summary_prompt_template = PromptTemplate(input_variables="information", template=summary_template)
   llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
   chain = summary_prompt_template | llm | StrOutputParser()
   linkedin_profile_url = lookup("Srdjan Bocanji Software Engineer")
   print(linkedin_profile_url)
   linked_in_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
   res = chain.invoke(input={"information": linked_in_data})
   print(res)
