from dotenv import load_dotenv
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup
from output_parsers import summary_parser

load_dotenv(override=True)
if __name__ == "__main__":
   summary_template = """
   given the Linkedin information {information} about a person from I want you to create:
   1. a summary
   2. two interesting facts about them
   
   \n {format_instructions}
   """


   summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template, partial_variables={"format_instructions": summary_parser.get_format_instructions()})
   llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

   linkedin_profile_url = lookup("Veljko veljkovic frontend")
   print(linkedin_profile_url)
   linked_in_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
   chain = summary_prompt_template | llm | summary_parser
   res = chain.invoke(input={"information": linked_in_data})
   print(res)
