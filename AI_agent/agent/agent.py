


from openai import OpenAI

from pathlib import Path  # file access / reading
import subprocess # for run_shell/run_program 
from datetime import date,datetime # for memory
import json # for tool calls 



BASE_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY) # later you can switch to other API 
MODEL = "qwen3-0.6b"
ROOT = Path(__file__).resolve().parent # AI_agent/agent
SOUL = ROOT / "SOUL.md"
MEMORY = ROOT / "MEMORY.md" 
TOOLS = []

def read_file(file):
    pass

def write_file(file, content):
    pass

def run_shell(command):
    pass 

def save_memory(fact):
    pass 

available_tools = {
    "run_shell" : run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "save_memory": save_memory,
}


def system_prompt():
    soul = SOUL.read_text() if SOUL.exists() else "You are helpful assistant"
    memory = MEMORY.read_text() if MEMORY.exists() else "(none)"

    return soul + "\n\n" + "## Memory" + memory


def run_query(messages):

    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools = TOOLS
    )

    msg = response.choices[0].message

    print(msg.content)

def main():
    messages = [{"role": "system", "content": system_prompt()}]

    while True:
        try:
            user = input("you> ").strip()
        except (KeyboardInterrupt):
            print()
            break

        if not user:
            continue # go to user = input("you> ").strip() 

        messages.append({"role": "user", "content": user})

        run_query(messages)
        # The query might change MEMORY.md, rebuild system_prompt()
        messages[0] = {"role": "system", "content": system_prompt()} # self-improving step 

main()