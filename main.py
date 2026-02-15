from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def accueil():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simulateur Aviator</title>
        <meta charset="UTF-8">
        <style>
            body { 
                background: #0a0b0e; 
                color: white; 
                font-family: Arial, sans-serif; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                min-height: 100vh; 
                margin: 0; 
                padding: 20px; 
            }
            .card { 
                background: #12141a; 
                border-radius: 20px; 
                padding: 30px; 
                max-width: 400px; 
                width: 100%; 
            }
            h1 { 
                color: #00ff88; 
                text-align: center; 
                margin-bottom: 30px; 
            }
            input { 
                width: 100%; 
                padding: 12px; 
                margin: 10px 0; 
                background: #1a1d26; 
                border: 1px solid #333; 
                border-radius: 8px; 
                color: white; 
                box-sizing: border-box; 
            }
            button { 
                width: 100%; 
                padding: 15px; 
                background: #00ff88; 
                color: black; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px; 
                font-weight: bold; 
                cursor: pointer; 
                margin: 20px 0; 
            }
            .result { 
                background: #1a1d26; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
                display: none; 
            }
            .mult { 
                font-size: 48px; 
                color: #00ff88; 
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>✈️ SIMULATEUR AVIATOR</h1>
            <input type="text" id="hex1" placeholder="Hex 1 (A-F)" value="A">
            <input type="text" id="dec" placeholder="Decimal (0-99)" value="5">
            <input type="text" id="hex2" placeholder="Hex 2 (00-FF)" value="2F">
            <button onclick="predire()">PRÉDIRE</button>
            <div class="result" id="result">
                <div class="mult" id="multiplier">0.00x</div>
            </div>
        </div>
        <script>
            async function predire() {
                const data = {
                    hex1: document.getElementById('hex1').value,
                    dec: document.getElementById('dec').value,
                    hex2: document.getElementById('hex2').value
                };
                const res = await fetch('/predire', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                document.getElementById('multiplier').textContent = result.multiplier + 'x';
                document.getElementById('result').style.display = 'block';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/predire', methods=['POST'])
def predire():
    data = request.json
    hex1 = data.get('hex1', 'A')
    dec = data.get('dec', '5')
    hex2 = data.get('hex2', '2F')
    
    # Calcul simple
    seed = f"{hex1}{dec}{hex2}{time.time()}"
    hash_val = hashlib.md5(seed.encode()).hexdigest()
    num = int(hash_val[:8], 16) % 900
    mult = 1.0 + (num / 100)
    
    return jsonify({"multiplier": round(mult, 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
