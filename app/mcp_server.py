import sys
import json
import datetime

def send_message(message: dict):
    data = json.dumps(message)
    sys.stdout.write(f"Content-Length: {len(data)}\r\n{data}")
    sys.stdout.flush()

def read_message():
    headers = {}
    while True:
        line = sys.stdin.readline()
        line = line.strip()
        # print(f"DEBUG raw line mcp: {line!r}")
        if line in ["\r\n", "\n", ""]:
            break
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        headers[key.strip()] = value.strip()
    if "Content-Length" not in headers:
        return None
    length = int(headers["Content-Length"])
    body = sys.stdin.read(length)
    return json.loads(body)

def main():
    while True:
        message = read_message()
        if not message:
            continue

        if message["method"] == "initialize":
            send_message({
                "jsonrpc": "2.0",
                "id": message["id"],
                "result": {"capabilities": {"tools": True}}
            })

        elif message["method"] == "list_tools":
            send_message({
                "jsonrpc": "2.0",
                "id": message["id"],
                "result": [
                    {
                        "name": "get_time",
                        "description": "Return current time",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "timezone": {"type": "string"}
                            }
                        }
                    }
                ]
            })

        elif message["method"] == "call_tool":
            params = message["params"]
            if params["name"] == "get_time":
                tz = params["arguments"]["timezone"]
                now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                result = {"time": f"{now} UTC (timezone param={tz})"}
                send_message({
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "result": result
                })
        else:
          send_message({
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": "No result"
          })

if __name__ == "__main__":
    main()
