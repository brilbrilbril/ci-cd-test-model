from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
generator = pipeline('text-generation', model='gpt2')

@app.route('/generate', methods=['POST'])
def generate_text():
    processed_data = request.json.get('processed_data', '')
    result = generator(processed_data, max_length=50, num_return_sequences=1)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
