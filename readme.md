# Distributed Training using Model Parallelism

Hands on ini menggunakan model sederhana dari `transformers` library yakni model GPT-2 yang bisa dipecah menjadi beberapa bagian dengan dua container, satu container untuk preprocessing dan pengambilan input, dan container kedua untuk bagian inferensinya.

### Step 1: Persiapan Dockerfile untuk Bagian Pertama (Preprocessing dan Input)

Buat sebuah folder baru untuk proyek ini: `model_parallelism`. Di dalam folder tersebut, buat file yang bernama `Dockerfile_part1`.

Berikut adalah isi `Dockerfile_part1`:

```dockerfile
# Menggunakan image dasar dari Python
FROM python:3.9-slim

# Menyiapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin requirements dan menginstal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin file script
COPY preprocess_input.py .

# Menjalankan service pada port 5001
EXPOSE 5001

# Menjalankan aplikasi
CMD ["python", "preprocess_input.py"]
```

#### Penjelasan:
- **`FROM python:3.9-slim`**: Menggunakan image Python yang ringan.
- **`WORKDIR /app`**: Menetapkan direktori kerja di dalam container.
- **`COPY requirements.txt .`**: Menyalin file `requirements.txt` yang berisi semua dependency model.
- **`RUN pip install -r requirements.txt`**: Menginstal dependency dari `requirements.txt`.
- **`COPY preprocess_input.py .`**: Menyalin script untuk preprocessing.
- **`EXPOSE 5001`**: Mengatur port agar bisa diakses di Kubernetes.
- **`CMD ["python", "preprocess_input.py"]`**: Menjalankan script preprocessing sebagai aplikasi utama.

#### Isi File requirements.txt
Buat file `requirements.txt` di folder yang sama dengan isi sebagai berikut:

```plaintext
transformers
torch
flask
```

#### Isi File preprocess_input.py
File ini akan berfungsi untuk menerima input dan melakukan preprocessing sederhana.

```python
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
```

### Step 2. Dockerfile untuk Bagian Kedua (Inferensi Model)

Di folder yang sama, buat `Dockerfile_part2` untuk bagian inferensi model.

```dockerfile
# Menggunakan image dasar dari Python
FROM python:3.9-slim

# Menyiapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin requirements dan menginstal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin file script untuk inferensi
COPY model_inference.py .

# Menjalankan service pada port 5002
EXPOSE 5002

# Menjalankan aplikasi
CMD ["python", "model_inference.py"]
```

#### Isi File model_inference.py
File ini akan menjalankan model GPT-2 atau model lainnya yang kita gunakan. Script ini akan menerima input dari container pertama dan menghasilkan teks.

```python
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
```

### Step 3. Build Docker Images

Setelah membuat `Dockerfile_part1` dan `Dockerfile_part2`, sekarang kita perlu membuild image Docker.

1. Build image untuk container pertama:

   ```bash
   docker build -t your_docker_image_part_1 -f Dockerfile_part1 .
   ```

2. Build image untuk container kedua:

   ```bash
   docker build -t your_docker_image_part_2 -f Dockerfile_part2 .
   ```

### Step 4. Buat File YAML untuk Deployment Model Parallelism

   Kita akan mendefinisikan beberapa container yang menjalankan bagian berbeda dari model. Berikut adalah contoh file YAML sederhana untuk deployment menggunakan Kubernetes dengan model yang dipisah dalam 2 container paralel. Simpan sebagai `model-parallelism.yaml`.

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: model-parallel-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: model-parallel
     template:
       metadata:
         labels:
           app: model-parallel
       spec:
         containers:
         - name: model-part-1
           image: your_docker_image_part_1:latest
           ports:
           - containerPort: 5001
         - name: model-part-2
           image: your_docker_image_part_2:latest
           ports:
           - containerPort: 5002
   ```

   - **model-part-1** dan **model-part-2** adalah dua container berbeda, masing-masing menjalankan bagian berbeda dari model.
   - **containerPort** mengizinkan komunikasi di antara bagian-bagian model.

###  Step 5. Deploy Model Parallelism

   Setelah file YAML disiapkan, jalankan perintah berikut untuk melakukan deploy:

   ```bash
   kubectl apply -f model-parallelism.yaml
   ```

### Step 6. Mengecek Status Deployment

   Gunakan perintah berikut untuk memastikan deployment berjalan:

   ```bash
   kubectl get pods
   ```

   Jika berhasil, kamu akan melihat Pod yang sesuai dengan nama `model-parallel-deployment`.

### Step 7. Mengakses Hasil Generate Text

   Gunakan `kubectl port-forward` untuk mengakses salah satu container dan menjalankan permintaan generate teks.

   ```bash
   kubectl port-forward pod/model-parallel-deployment-<pod-id> 8080:5001
   ```

   Lalu, akses endpoint tersebut (misalnya, melalui Python atau Curl) untuk mengirim permintaan ke model yang berjalan di Kubernetes:

   ```python
   import requests

   response = requests.post("http://localhost:8080/generate", json={"prompt": "Write a story about a robot"})
   print(response.json())
   ```

### Output Generate Text

Output hasil text generation biasanya akan tergantung pada prompt yang kamu berikan. Contohnya, jika menggunakan prompt `"Write a story about a robot"`, hasilnya mungkin seperti berikut:

   ```plaintext
   "Once upon a time, in a world where robots and humans coexisted, there was a curious robot named AI-22 who dreamt of understanding human emotions..."
   ```
