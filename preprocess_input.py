from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/preprocess', methods=['POST'])
def preprocess():
    data = request.json.get('text', '')
    # Misalnya, preprocessing sederhana
    processed_data = data.lower()
    return jsonify({'processed_data': processed_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
