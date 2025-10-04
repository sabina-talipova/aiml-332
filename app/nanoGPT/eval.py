import os
import json
import math
import torch
import tiktoken
from model import GPTConfig, GPT

@torch.no_grad()
def eval(model, enc, eval_file, device="cuda"):

    with open(eval_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_logprob = 0.0
    total_tokens = 0

    for ex in data:
        prompt, response = ex["prompt"], ex["response"]

        prompt_ids = enc.encode(prompt)
        response_ids = enc.encode(response)

        x = torch.tensor([prompt_ids], dtype=torch.long, device=device)
        logits, _ = model(x)
        logits = logits[:, -1, :]

        logprob = 0.0
        for token in response_ids:
            probs = torch.softmax(logits, dim=-1)
            prob = probs[0, token].item()
            logprob += torch.log(torch.tensor(prob + 1e-10))
            total_tokens += 1

            x = torch.tensor([[token]], dtype=torch.long, device=device)
            logits, _ = model(x)
            logits = logits[:, -1, :]

        total_logprob += logprob.item()
        print(f"Prompt: {prompt}\nResponse: {response}\n"
              f"LogProb: {logprob.item():.4f}\n")

    # perplexity
    avg_logprob = total_logprob / total_tokens
    ppl = math.exp(-avg_logprob)

    print(f"Summed log probability over dataset: {total_logprob:.4f}")
    print(f"Perplexity over dataset: {ppl:.4f}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate GPT on prompt-response pairs")
    parser.add_argument("out_dir", type=str, help="Directory with model checkpoint")
    parser.add_argument("--eval_file", type=str, default="eval_data.json")
    parser.add_argument("--init_from", type=str, default="resume")
    parser.add_argument("--start", type=str, default="\n")
    parser.add_argument("--num_samples", type=str, default="10")
    parser.add_argument("--max_new_tokens", type=str, default="500")
    parser.add_argument("--temperature", type=str, default="0.8")
    parser.add_argument("--top_k", type=str, default="200")
    parser.add_argument("--seed", type=str, default="1337")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--compile", type=str, default="False")
    parser.add_argument("--show_probs", type=str, default="False")

    args = parser.parse_args()

    ckpt_path = os.path.join(args.out_dir, "ckpt.pt")
    checkpoint = torch.load(ckpt_path, map_location=args.device)

    model_args = checkpoint["model_args"]
    model = GPT(GPTConfig(**model_args))
    state_dict = checkpoint["model"]
    model.load_state_dict(state_dict)
    model.eval().to(args.device)

    enc = tiktoken.get_encoding("gpt2")

    eval(model, enc, args.eval_file, args.device)