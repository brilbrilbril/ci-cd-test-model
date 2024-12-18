#from flask import Flask, request, jsonify
import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# generator = pipeline('text-generation', model='gpt2')

# # Define a Pydantic model for the request body
# class GenerateRequest(BaseModel):
#     processed_data: str

# @app.post("/generate")
# def generate_text(request: GenerateRequest):
#     result = generator(request.processed_data, max_length=50, num_return_sequences=1)
#     return {"generated_text": result[0]['generated_text']}

@app.get("/")
def read_root():
    return {"Hello": "Fastapi test model in container"}

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8080))
#     uvicorn.run(app, host="0.0.0.0", port=port)



# app = Flask(__name__)
# generator = pipeline('text-generation', model='gpt2')

# @app.route('/generate', methods=['POST'])
# def generate_text():
#     processed_data = request.json.get('processed_data', '')
#     result = generator(processed_data, max_length=50, num_return_sequences=1)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

# Initialize the GPT-2 model and tokenizer