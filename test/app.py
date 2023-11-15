from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)

# Función para traducir la query de español a inglés
def translate_query(query):
    translator = Translator()
    translation = translator.translate(query, src='es', dest='en')
    return translation.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_es = request.form['food_name']
        query_en = translate_query(query_es)
        
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query_en)
        response = requests.get(api_url, headers={'X-Api-Key': 'kN27YTblQandAgiHDeJIsY5SkLq61NvtfNa69zJi'})
        
        if response.status_code == requests.codes.ok:
            result = response.json()
            return render_template('index.html', result=result)
        else:
            error_message = "Error: {} - {}".format(response.status_code, response.text)
            return render_template('index.html', error_message=error_message)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
