from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a smaller, faster model for real-time responses
model_name = "microsoft/DialoGPT-small"  # Faster on GPU
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None
)

# Add pad token if missing
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Conversation context
conversation_history = []

print("LLM model loaded and ready")

@app.post("/generate")
async def generate(prompt: str = Form(...)):
    try:
        # Simple conversation prompt
        system_prompt = "You are a helpful AI assistant. Respond naturally and concisely."
        full_prompt = f"{system_prompt}\nUser: {prompt}\nAssistant:"
        
        inputs = tokenizer.encode(full_prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=64,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )
        
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        response = response.strip()
        
        # Clean up response
        if response.startswith("Assistant:"):
            response = response[10:].strip()
        
        return {"text": response}
        
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"error": str(e), "text": "I'm sorry, I couldn't process that."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
