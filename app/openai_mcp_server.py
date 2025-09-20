import sys
import json
import datetime
import zoneinfo

TOOLS = {
    "get_time": lambda timezone: {
        "time": datetime.datetime.now(zoneinfo.ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timezone": timezone
    },
    "say_hello": lambda name: {"message": f"Hello, {name}!"},
    "strange_message": lambda message: {"message": f"It's wrong {message}!"},
    "get_firstname_lastname": lambda firstname, lastname: {"message": f"First name {firstname}, Last name: {lastname}."}
}

def send_message(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def read_message():
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)

def main():
    while True:
        msg = read_message()
        if not msg:
            continue

        if msg.get("method") == "call_tool":
            tool_name = msg["params"]["name"]
            args = msg["params"]["arguments"]
            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                send_message({"jsonrpc":"2.0","id": msg["id"],"result": result})
            else:
                send_message({"jsonrpc":"2.0","id": msg["id"],"result": f"Unknown tool {tool_name}"})

if __name__ == "__main__":
    main()
