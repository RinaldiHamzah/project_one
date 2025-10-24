// Character counter for textarea
document.addEventListener('DOMContentLoaded', function() {
    const reviewText = document.getElementById('reviewText');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (reviewText && charCount && analyzeBtn) {
        reviewText.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count;
            
            // Enable/disable analyze button based on text input
            analyzeBtn.disabled = count === 0;
        });
        
        // Handle analyze button click
        analyzeBtn.addEventListener('click', function() {
            const text = reviewText.value.trim();
            const selectedModel = document.querySelector('input[name="model"]:checked').value;
            
            if (!text) {
                alert('Silakan masukkan teks ulasan terlebih dahulu');
                return;
            }
            
            // Show loading state
            const originalText = this.textContent;
            this.innerHTML = '<span class="loading"></span> Menganalisis...';
            this.disabled = true;
            
            // Create form data
            const formData = new FormData();
            formData.append('review_text', text);
            formData.append('model', selectedModel);
            
            // Send request to Flask backend
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    displayPredictionResult(data);
                }
            })
            
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat melakukan prediksi');
            })
            .finally(() => {
                // Reset button state
                this.textContent = originalText;
                this.disabled = false;
            });
        });
    }
});

function displayPredictionResult(result) {
    const resultsContainer = document.getElementById('predictionResults');
    
    if (!resultsContainer) return;
    
    const sentimentClass = getSentimentClass(result.sentiment);
    
    resultsContainer.innerHTML = `
        <div class="prediction-result">
            <div class="sentiment-display">
                <div class="sentiment-badge ${sentimentClass}">
                    ${result.sentiment}
                </div>
            </div>
            
            <div class="prediction-info">
                <div class="info-item">
                    <span class="info-label">Waktu Prediksi:</span>
                    <span class="info-value">${result.timestamp}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Model Digunakan:</span>
                    <span class="info-value">${getModelName(result.model_used)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="info-value" style="color: #16a34a;">Berhasil</span>
                </div>
            </div>
        </div>
    `;
}

function getSentimentClass(sentiment) {
    switch (sentiment) {
        case 'Positif':
            return 'sentiment-positive';
        case 'Negatif':
            return 'sentiment-negative';
        case 'Netral':
            return 'sentiment-neutral';
        default:
            return 'sentiment-neutral';
    }
}

function getModelName(model) {
    switch (model) {
        case 'svm':
            return 'Support Vector Machine (SVM)';
        case 'naive-bayes':
            return 'Naive Bayes';
        default:
            return model;
    }
}


function openTelegramBot() {
    window.open('https://t.me/Update_Ulasan_bot', '_blank');
}
