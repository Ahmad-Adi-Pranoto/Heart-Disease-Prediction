const form = document.getElementById('heartForm');
const predictBtn = document.getElementById('predictBtn');
const resultDiv = document.getElementById('result');
const notification = document.getElementById('notification');
const overlay = document.getElementById('overlay');
const notificationMessage = document.getElementById('notificationMessage');
const formError = document.getElementById('formError');

// Fungsi untuk memvalidasi form
function validateForm() {
    let isValid = true;
    formError.innerHTML = '';

    const inputs = Array.from(form.elements).filter(e => e.type !== "button");
    inputs.forEach(input => {
        if (!input.value) {
            isValid = false;
            formError.innerHTML = "Please fill in all fields.";
        }
    });

    return isValid;
}

// Fungsi untuk menjalankan prediksi
function predict() {
    if (validateForm()) {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `
                <h3>Hasil Prediksi: ${data.result}</h3>
                <p><strong>Rekomendasi:</strong> ${data.recommendation}</p>
            `;
            notificationMessage.innerHTML = `
                <p>Berdasarkan data yang Anda masukkan:</p>
                <strong style="font-size: 1.5em;">Hasil Prediksi: ${data.result}</strong>
                <hr style="margin: 15px 0; border: 1px solid #ccc;">
                <p><strong>Rekomendasi:</strong><br>${data.recommendation}</p>
            `;
            notification.style.display = 'block';
            overlay.style.display = 'block';
        })

        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

// Fungsi untuk menutup notifikasi
function closeNotification() {
    notification.style.display = 'none';
    overlay.style.display = 'none';
}

// Menambahkan event listener untuk pindah ke input berikutnya dengan Enter
Array.from(form.elements).forEach((input, index, elements) => {
    if (input.type !== "button") {
        input.addEventListener('keypress', (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                if (index < elements.length - 2) { 
                    elements[index + 1].focus();
                } else {
                    predict();
                }
            }
        });
    }
});

predictBtn.addEventListener('click', predict);
