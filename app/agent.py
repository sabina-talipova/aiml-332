import subprocess
import json
import re

def make_request(process, message):
    data = json.dumps(message)
    process.stdin.write(f"Content-Length: {len(data)}\r\n{data}")
    process.stdin.flush()

    headers = {}
    while True:
        line = process.stdout.readline()
        # print(f"DEBUG raw line: {line!r}")
        if line in ["\r\n", "\n", ""]:
            break
        key, value = line.split(": ", 1)
        headers[key.strip()] = value.strip()
    length = int(headers["Content-Length"])
    body = process.stdout.read(length)
    return json.loads(body)

def main():
    process = subprocess.Popen(
        ["python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    make_request(process, {"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    tools = make_request(process, {"jsonrpc": "2.0", "id": 2, "method": "list_tools"})
    print([t["name"] for t in tools["result"]])
    print("My request")

    req_id = 3
    while True:
        user_input = input("\n>>> ")

        if user_input.lower() in ["exit", "quit"]:
            print("EXIT.")
            break

        if "time" in user_input.lower():
            match = re.search(r"([A-Za-z]+/[A-Za-z_]+)", user_input)
            timezone = match.group(1) if match else "UTC"

            call = make_request(process, {
                "jsonrpc": "2.0",
                "id": req_id,
                "method": "call_tool",
                "params": {"name": "get_time", "arguments": {"timezone": timezone}}
            })
            print("Answer", call["result"]["time"])
            req_id += 1
        else:
            print("I don't know your time")

if __name__ == "__main__":
    main()
