from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)

# Habilita o CORS em todas as rotas
CORS(app)

# URL padrão da sua rádio no AzuraCast
DEFAULT_AZURA_URL = 'https://erbj.com.br/api/nowplaying/power_dance'

@app.route('/api/player', methods=['GET'])
def get_player_data():
    try:
        # Pega a URL enviada via parâmetro (?url=...) ou usa a URL padrão do AzuraCast
        player_url = request.args.get('url', DEFAULT_AZURA_URL)

        # Cabeçalho para evitar bloqueios de requisição no servidor de origem
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        # Faz a requisição para a API da rádio (com timeout de 8 segundos para a Vercel)
        response = requests.get(player_url, headers=headers, timeout=8)

        if response.status_code != 200:
            return jsonify({
                "error": f"Erro ao acessar o player externo. Status: {response.status_code}"
            }), 500

        # Converte a resposta para JSON
        data = response.json()

        # Retorna o JSON completo (Proxy Puro)
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({"error": "Tempo limite esgotado ao conectar na rádio."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)