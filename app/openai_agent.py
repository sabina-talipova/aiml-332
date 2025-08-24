import subprocess
import json
import os

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

mcp = subprocess.Popen(
    ["python", "openai_mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

def send_to_mcp(msg):
    mcp.stdin.write(json.dumps(msg) + "\n")
    mcp.stdin.flush()
    resp = mcp.stdout.readline().strip()
    return json.loads(resp)

def generate_rpc(user_input, rpc_id):
    prompt = f"""
You are an AI agent. The user query is:
\"\"\"{user_input}\"\"\"

Available tools:
1. get_time(timezone: str)
2. say_hello(name: str)

Return a valid JSON-RPC dictionary for MCP:
{{"jsonrpc":"2.0","id":{rpc_id},"method":"call_tool","params":{{"name": "<tool_name>", "arguments":{{...}}}}}}

Do not add any extra text, only JSON.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":prompt}],
        temperature=0
    )
    rpc_json = response.choices[0].message.content.strip()
    print(rpc_json)
    return json.loads(rpc_json)

# -----------------------------
# CLI loop
# -----------------------------
rpc_id = 1
print("OpenAI Agent CLI ready. Type 'exit' to quit.")
while True:
    user_input = input(">>> ")
    if user_input.lower() in ["exit","quit"]:
        break

    try:
        rpc_instruction = generate_rpc(user_input, rpc_id)
        rpc_id += 1

        response = send_to_mcp(rpc_instruction)
        print("🛠 MCP Response:", response.get("result"))
    except Exception as e:
        print("Error:", e)
