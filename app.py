from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)

# Habilita o CORS em todas as rotas
CORS(app)

@app.route('/api/player', methods=['GET'])
def get_player_data():
    try:
        # Recebe a URL como parâmetro da consulta
        player_url = request.args.get('url')
        if not player_url:
            return jsonify({"error": "A URL do player não foi fornecida."}), 400

        # Faz a requisição para a URL do player
        response = requests.get(player_url)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar o player."}), 500

        # Converte a resposta para JSON
        data = response.json()

        # Retorna os dados extraídos do JSON
        return jsonify({
            "artist": data.get("artist", "Desconhecido"),
            "title": data.get("title", "Desconhecido"),
            "status": data.get("status", "Desconhecido"),
            "listeners": data.get("listeners", 0),
            "image": data.get("image")
        })
    except Exception as e:
        # Retorna erro se algum problema ocorrer
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000)

