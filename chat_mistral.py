# chat_mistral.py
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# pick whichever Mistral instruct checkpoint you requested access to:
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

# If you set HUGGINGFACE_HUB_TOKEN in the environment, make sure it's visible here.
hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN")
if hf_token:
    # ensure huggingface_hub will see it (safe to set again)
    os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token

print("Loading tokenizer + model (first run downloads weights). This may take a bit...")
tokenizer = AutoTokenizer.from_pretrained(MODEL)   # uses env token automatically
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    torch_dtype=torch.float16,
)

print("Model ready. Type a message (ctrl-c or 'exit' to quit).")
while True:
    prompt = input("\nYou: ")
    if prompt.strip().lower() in ("exit", "quit"):
        break

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    resp = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\nMistral:", resp)
