from flask import Flask, render_template_string, request, jsonify, send_file
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://a.4cdn.org/s/catalog.json'
    response = requests.get(url)
    data = response.json()
    
    images = []
    base_url = 'https://i.4cdn.org/s/'

    for thread in data:
        for post in thread['threads']:
            if 'tim' in post and 'ext' in post:
                img_url = f"{base_url}{post['tim']}{post['ext']}"
                images.append(img_url)
    
    # HTML şablonu
    html = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>4chan S Board Resimleri</title>
      </head>
      <body>
        <h1>4chan S Board Resimleri</h1>
        <div>
          {% for img in images %}
            <img src="{{ url_for('proxy_image') }}?image_url={{ img }}" alt="Image" style="max-width: 300px; margin: 10px;">
          {% endfor %}
        </div>
      </body>
    </html>
    '''
    
    return render_template_string(html, images=images)

@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('image_url')
    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400
    
    try:
        # Görüntüyü 4chan'den çekiyoruz
        response = requests.get(image_url)
        response.raise_for_status()
        return send_file(BytesIO(response.content), mimetype='image/jpeg')
    except requests.exceptions.RequestException as e:
        # Hata mesajını logluyoruz
        print(f"Error fetching image: {e}")
        return jsonify({'error': 'Image could not be fetched'}), 500

if __name__ == '__main__':
    app.run(debug=True)
