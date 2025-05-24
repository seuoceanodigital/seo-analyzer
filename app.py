from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analisar-seo', methods=['POST'])
def analisar_seo():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"erro": "URL não fornecida"}), 400

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "Sem título"
        description = soup.find("meta", attrs={"name": "description"})
        description_content = description.get("content", "Sem descrição") if description else "Sem descrição"

        insights = gerar_insights_ia(title, description_content)

        return jsonify({
            "titulo": title,
            "descricao": description_content,
            "insights": insights
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def gerar_insights_ia(title, description):
    return [
        f"O título '{title}' está {avaliar_titulo(title)}.",
        f"A meta descrição parece {avaliar_descricao(description)}.",
        "Considere usar mais palavras-chave no primeiro parágrafo.",
        "Inclua links internos para páginas importantes.",
        "Otimize imagens com atributos ALT relevantes."
    ]

def avaliar_titulo(t):
    return "curto demais" if len(t) < 20 else "adequado"

def avaliar_descricao(d):
    return "muito genérica" if "bem-vindo" in d.lower() else "relevante"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
