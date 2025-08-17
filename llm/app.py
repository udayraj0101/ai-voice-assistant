from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

app = Flask(__name__)

# Load model on startup
print("Loading LLaMA model...")
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Replace with your model path

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto"
)

print("LLaMA model loaded")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        user_text = data['text']
        
        # Format prompt with instructions for concise responses
        prompt = f"<s>[INST] You are a helpful AI assistant. Give crisp, concise responses. Be direct and to the point. User: {user_text} [/INST]"
        
        # Tokenize and generate
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                use_cache=True
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        
        return jsonify({'response': response.strip()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)