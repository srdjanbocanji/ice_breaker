import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools.tools import get_profile_url_tavily

load_dotenv(override=True)

def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    template = """
    given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only an URL.
    """
    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(name="Crawl Google 4 Linkedin profile page",
             func=get_profile_url_tavily,
             description="useful for when you need to get the Linkedin Page URL")
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})
    return result['output']


if __name__ == "__main__":
    linkedin_url = lookup("Srdjan Bocanji")
    print(linkedin_url)