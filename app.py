#Ahmad Adi Pranoto
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Inisialisasi Flask
app = Flask(__name__)

# Load dataset dan preprocess data
data = pd.read_csv('processed_heart_disease_data.csv')
X = data.drop('num', axis=1)  # Kolom 'num' dianggap sebagai label target
y = data['num']

# Skala fitur dan split data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inisialisasi dan latih model KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Evaluasi awal model pada data uji
y_pred = knn.predict(X_test)
print("Evaluasi Model pada Data Uji:")
print("Akurasi:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Rute untuk halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data JSON dari permintaan
        data = request.get_json()
        input_data = [
            float(data['age']),
            float(data['sex']),
            float(data['dataset']),
            float(data['cp']),
            float(data['trestbps']),
            float(data['chol']),
            float(data['fbs']),
            float(data['restecg']),
            float(data['thalch']),
            float(data['exang']),
            float(data['oldpeak']),
            float(data['slope']),
            float(data['ca']),
            float(data['thal'])
        ]

        # Preprocessing input data
        input_data_scaled = scaler.transform([input_data])

        # Prediksi menggunakan model KNN
        prediction = knn.predict(input_data_scaled)
        result = 'Heart Disease' if prediction[0] == 1 else 'No Heart Disease'

        # Tambahkan rekomendasi berdasarkan hasil
        if prediction[0] == 1:
            recommendation = (
                "Kami menyarankan Anda untuk segera berkonsultasi dengan dokter spesialis jantung untuk diagnosa lebih lanjut. "
                "Selain itu, terapkan pola hidup sehat dengan menjaga pola makan seimbang, rutin berolahraga, dan hindari merokok atau konsumsi alkohol berlebih."
            )
        else:
            recommendation = (
                "Hasil prediksi menunjukkan Anda tidak memiliki penyakit jantung. Tetap jaga gaya hidup sehat, rutin berolahraga, "
                "dan konsumsi makanan bergizi untuk menjaga kesehatan jantung Anda."
            )

        # Kirim hasil dan rekomendasi sebagai respons JSON
        return jsonify({'result': result, 'recommendation': recommendation})

    except Exception as e:
        # Jika terjadi error, tampilkan pesan kesalahan di konsol dan kirim pesan error ke klien
        print("Error:", str(e))
        return jsonify({'error': 'An error occurred. Please check the input values and try again.'})

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
