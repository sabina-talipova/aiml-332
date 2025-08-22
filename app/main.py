import yaml
from smolagents import CodeAgent, HfApiModel, load_tool
from tools.custom_tools import get_current_time_in_timezone
# from tools.final_answer import final_answer
from Gradio_UI import GradioUI
import os


model = HfApiModel(
    max_tokens=2048,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    api_key=os.getenv("HF_TOKEN")
)

with open("prompts.yaml", "r") as f:
    prompt_templates = yaml.safe_load(f)

agent = CodeAgent(
    model=model,
    tools=[get_current_time_in_timezone],
    max_steps=6,
    verbosity_level=1,
    prompt_templates=prompt_templates
)

GradioUI(agent).launch()
