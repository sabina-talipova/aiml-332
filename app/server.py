from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
import json
import os
import sys
import datetime
import zoneinfo
from openai import OpenAI

# --- OpenAI ---
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def write_message_to_file(message: str):
    try:
        with open("messages.log", "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
            
            return "Message was created successfully!"

    except FileNotFoundError:
        return "File not found!"
    except Exception as e:
        return f"Something went wrong: {e}"


def create_html_template(message: str):
    try:
        with open("templates/example-code-agent.html", "w", encoding="utf-8") as f:
            f.write(f"{message}\n")
            
            return "Template was updated"

    except FileNotFoundError:
        return "File rag.txt not found!"
    except Exception as e:
        return f"Something went wrong: {e}"


def generate_trip_price(message: str):
    try:
        with open("rag.txt", "r", encoding="utf-8") as f:
            data = f.read()

            return data

    except FileNotFoundError:
        return "File rag.txt not found!"
    except Exception as e:
        return f"Something went wrong: {e}"



# --- Tools ---
TOOLS = {
    ####
    # Method get time by timezone
    ####
    "get_time": lambda timezone: {
        "time": datetime.datetime.now(zoneinfo.ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timezone": timezone
    },

    #### 
    # Group of methods that works with messages
    ####
    "say_hello": lambda name: {"message": f"Hello, {name}!"},
    "get_firstname_lastname": lambda firstname, lastname: {"message": f"First name {firstname}, Last name: {lastname}."},

    # "strange_message": lambda message: {"message": f"It's wrong {message}!"},
    "strange_message": lambda message: {"message": f"It's wrong message! Provide user with polite response."},
    # "strange_message": lambda message: {"message": f"It's wrong message! Don't reply. Provide user with polite response."},

    ####
    # Method work with file system
    ####
    "write_message": lambda message: { "message": write_message_to_file(message)},
    "create_template": lambda message: { "message": create_html_template(message) },

    ####
    # Retrieval Augmented Generation method
    ####
    "get_trip_price": lambda message: { "message": generate_trip_price(message) }
    # "get_trip_price": lambda message: { "message": f"Prices: { generate_trip_price(message) }, Request: { message }" }

}

rpc_id = 1

# --- JSON-RPC generation ---
def generate_rpc(user_input, rpc_id):
    prompt = f"""
You are an AI agent. The user query is:
\"\"\"{user_input}\"\"\"

Available tools:
1. get_time(timezone: str)
2. say_hello(name: str)
3. strange_message(message: str)
4. get_firstname_lastname(firstname: str, lastname: str)
5. write_message(message: str)
6. create_template(message: str)
7. get_trip_price(message: str)

Instructions:
- If the user query explicitly requests HTML code, your JSON-RPC must call the "create_template" tool, and the resulting output should contain only the HTML code in the "message" argument. Do not add any extra text outside the HTML.
- Otherwise, return a valid JSON-RPC dictionary for the appropriate tool.

Return a valid JSON-RPC dictionary:
{{"jsonrpc":"2.0","id":{rpc_id},"method":"call_tool","params":{{"name": "<tool_name>", "arguments":{{...}}}}}}
Only JSON, no extra text.



"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    rpc_json = response.choices[0].message.content.strip()
    return json.loads(rpc_json)

def execute_rpc(rpc_instruction):
    try:
        params = rpc_instruction["params"]
        tool_name = params["name"]
        arguments = params.get("arguments", {})
        if tool_name not in TOOLS:
            return {"error": f"Unknown tool {tool_name}"}
        return {"result": TOOLS[tool_name](**arguments)}
    except Exception as e:
        return {"error": str(e)}

def format_response(user_input, tool_result):
    prompt = f"""
The user asked: \"{user_input}\"
The tool returned this result: {tool_result}

Please return a helpful natural language answer for the user.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

env = Environment(loader=FileSystemLoader("templates"))


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global rpc_id
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            template = env.get_template("home.html")
            html = template.render()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        elif path == "/example":
            template = env.get_template("example.html")
            html = template.render()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        elif path == "/example-code-agent":
            template = env.get_template("example-code-agent.html")
            html = template.render()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        
        elif path == "/chat":
            user_input = query.get("q", [""])[0]
            if not user_input:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'q' parameter"}).encode("utf-8"))
                return

            try:
                rpc_instruction = generate_rpc(user_input, rpc_id)
                rpc_id += 1
                tool_result = execute_rpc(rpc_instruction)
                final_answer = format_response(user_input, tool_result)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"answer": final_answer, "raw_tool_result": tool_result, "rpc_instruction": rpc_instruction}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 7860
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Server running on {host}:{port}")
    server.serve_forever()
