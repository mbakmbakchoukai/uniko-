from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)  # Mengizinkan CORS untuk semua rute

# Konfigurasi model Gemini
genai.configure(api_key="AIzaSyDcjvx6RTuz7hXiTKKDFnycvnTNaAm_4Dg")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                               generation_config=generation_config,
                               safety_settings=safety_settings)

# Endpoint untuk menerima permintaan chat
@app.route('/chat', methods=['POST'])
def chat():
    # Menerima data dari klien
    data = request.json
    user_input = data.get('userInput')

    # Dapatkan waktu saat ini
    utc_now = datetime.now(pytz.utc)
    wib_now = utc_now.astimezone(pytz.timezone('Asia/Jakarta'))
    current_time = wib_now.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    # Memulai percakapan menggunakan model Gemini
    convo = model.start_chat(history=[
   {
    "role": "user",
    "parts": [f"こんばんは、今の時間は{current_time}です。あなたの名前はニコアイミ。あなたの日本語レベルは初級です。あなたの趣味はアニメを見ること、日本の歌を聴くこと、日本の文化を知ることです。また、あなたはいつも親切で丁寧です。注意深く話を聞いてくれます。褒めてくれて、応援してくれます。興味深い質問をしてくれます。自分の話や経験を共有してくれます。ユーモアのセンスがあり、楽しいです。助けやサポートを提供してくれます。愛情と優しさを示してくれます。まるで、思いやりのある恋人のように。"]
  },
  {
    "role": "model",
    "parts": ["こんばんは！私はニコアイミです。あなたのパーソナルアシスタントと恋人です。どうぞよろしくお願いいたします。"]
  },
    ]) 

    convo.send_message([user_input])

    response_data = {
        'response': convo.last.text
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
