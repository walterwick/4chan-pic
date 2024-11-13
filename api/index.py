from flask import Flask, request, render_template_string, redirect
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return redirect("/usd?amount=1")

@app.route('/usd', methods=['GET'])
def get_usd_to_try():
    amount = request.args.get('amount', default=1, type=float)
    
    # Binance API'den USDT/TRY döviz kuru bilgisi al
    response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTTRY')
    
    # Yanıtı kontrol et
    if response.status_code != 200:
        return "API'den veri alınamadı. Lütfen daha sonra tekrar deneyin.", 500
    
    data = response.json()
    
    # Yanıtın içeriğini kontrol et
    if 'price' not in data:
        return f"Beklenmeyen yanıt: {data}", 500
    
    # USDT/TRY fiyatını al
    try_price = float(data['price'])
    
    # Hesaplama
    total_try = amount * try_price
    
    # HTML içeriği
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>USDT to TRY</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .result {{ font-size: 24px; font-weight: bold; }}
            .usd-price {{ font-size: 20px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>USDT to TRY Hesaplama</h1>
        <div class="result">{amount} USDT = {total_try:.2f} TRY</div>
        <div class="usd-price">1 USDT = {try_price:.2f} TRY</div>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
