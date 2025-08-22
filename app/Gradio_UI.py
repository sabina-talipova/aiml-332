import gradio as gr

class GradioUI:
    def __init__(self, agent):
        self.agent = agent

    def respond(self, message: str, history: list) -> str:
        # history можно игнорировать или использовать
        return self.agent.run(message)

    def launch(self):
        gr.ChatInterface(self.respond, title="My Local Agent (Ollama)").launch(server_name="0.0.0.0")
