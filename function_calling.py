from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
import os,subprocess
import re
import time

ddg_search = DuckDuckGoSearchResults()
ROOT_DIR = "./x/medium"
def execute_shell_echo(command: str) -> str:
    os.chdir(ROOT_DIR)
    if command.startswith("echo"):
        result = subprocess.run(command, capture_output=True, shell=True)
        output = f"STDOUT:{result.stdout.decode()}\nSTDERR:{result.stderr.decode()}"
    else:
        output = f"STDERR: not a valid echo command!"
    return output

llm = ChatOpenAI(model="gpt-3.5-turbo")

question= "Research the stock price of Nvidia and generate an investment plan. Save the result in a file plan.txt."
prompt="""Answer the following questions as best you can. You have access to the following tools:
    
    WebSearch: "Search the web to answer questions about current events. Input should be a search query. Output is a JSON array of the query results."
    SaveResult: "Run the 'echo' tool to save the result. Input is the full Shell command."

    Use the following format:
    
    Thought: you should always think about what to do
    Action: the action to take, should be one of [ListFiles, ReadFile, RunTest]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Always generate Action and Action Input. Missing them will produce an error!
    Begin!
    
    Question:
    {}

    Thought:
""".format(question)
stop = ['Observation:', '\n\tObservation:', 'Observation ', '\n(', ' (']

input=str(prompt)
iteration = 0
while iteration < 5:
    iteration=iteration+1
    try:
        output = llm.invoke(input=input).content
        time.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")
        input=input[:len(input)//2]
        continue

    print(f"\n{output}\n")

    regex = (
            r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        )
    text = output

    action_match = re.search(regex, text, re.DOTALL)
    if action_match:
        action = action_match.group(1).strip()
        action_input = action_match.group(2)
        tool_input = action_input.strip("\n")
        if text.startswith("Thought:"):
            input = input+text[8:]
        else:
            input = input+text
        
        if action=="WebSearch":
            tool_output= ddg_search._run(tool_input)
        elif action=="SaveResult":
            tool_output = execute_shell_echo(tool_input)
        else:   
            tool_output = "Error: Action "+f"'{action}' is not a valid tool!"

        print(f"------- tool_output ------- \n{tool_output}\n")

    elif 'Final Answer:' in text:
        print(f"\n\n{text}")
        exit()
    else: 
        tool_output = "Error: wrong response missing Action and Action Input!"  
        print(f"****** wrong LLM response ******\n{text}\n")

    input = input+"\nObservation: "+tool_output+"\n"






