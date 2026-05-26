from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

os.environ.get("GEMINI_KEY", "AIzaSyCZoMgYYh0oe2g28thdUk9F-Sc1mwrofUI")
@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.json.get('prompt', '')
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_KEY}"
        body = {"contents": [{"parts": [{"text": user_prompt}]}]}
        r = requests.post(url, json=body, timeout=30)
        data = r.json()
        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = str(data)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"خطأ: {str(e)}"})

import os

if __name__ == '__main__':
    # جلب البورت ديناميكياً للاستضافة أو استخدام 8000 محلياً
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
