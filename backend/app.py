from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/extrair', methods=['POST'])
def extrair():
    data = request.json
    url = data.get('url')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "titulo": info.get('title'),
                "descricao": info.get('description'),
                "duracao": info.get('duration_string'),
                "miniatura": info.get('thumbnail'),
                "canal": info.get('uploader'),
                "link_audio": info.get('url') 
            })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)