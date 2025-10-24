import threading
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
from datetime import datetime
import requests
import os
from model_predict import ModelPredict


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
model_ml = ModelPredict()

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username and password:  # Simple validation
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', error='Username dan password harus diisi')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', username=session['username'])
class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_sentiment_result(self, review_text, sentiment, model, username):
        message = f"""
🤖 <b>Hasil Analisis Sentimen</b>

👤 <b>User:</b> {username}
📝 <b>Ulasan:</b> {review_text[:200]}{"..." if len(review_text) > 200 else ""}

💭 <b>Sentimen:</b> {sentiment}
🔧 <b>Model:</b> {model}
📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending notification: {e}")
            return None

@app.route('/predict', methods=['POST'])
def predict():
    if 'logged_in' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    review_text = request.form['review_text']
    model = request.form['model']

    if not review_text.strip():
        return jsonify({'error': 'Text review tidak boleh kosong'}), 400

    # Prediksi menggunakan model yang dipilih
    if model == "naive-bayes":
        sentiment = model_ml.model_predict_nvm(review_text)
    else:
        sentiment = model_ml.model_predict_svm(review_text)

    result = {
        'sentiment': sentiment,
        'model_used': model,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }

    # Konfigurasi Telegram Bot
    BOT_TOKEN = "8128015859:AAHy4JWf-4G4zssuaKKwWCbAOkKC3h9M65o"
    CHAT_ID = 719246465

    if len(BOT_TOKEN) > 0 and len(str(CHAT_ID)) > 0:
        try:
            notifier = TelegramNotifier(BOT_TOKEN, CHAT_ID)
            telegram_result = notifier.send_sentiment_result(
                review_text=review_text,
                sentiment=sentiment,
                model=model,
                username=session['username']
            )

            if telegram_result and telegram_result.get('ok'):
                result['telegram_sent'] = True
                result['telegram_message'] = 'Hasil berhasil dikirim ke Telegram Bot'
            else:
                result['telegram_sent'] = False
                result['telegram_message'] = 'Gagal mengirim ke Telegram Bot'
        except Exception as e:
            result['telegram_sent'] = False
            result['telegram_message'] = f'Error: {str(e)}'
    else:
        result['telegram_sent'] = False
        result['telegram_message'] = 'Telegram Bot belum dikonfigurasi'

    return jsonify(result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)