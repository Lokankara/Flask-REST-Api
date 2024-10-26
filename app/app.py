from flask_migrate import Migrate
from flask import Flask, request, jsonify, render_template
from models import db
from controllers import main
from g4f.client import Client
from deep_translator import GoogleTranslator

# migrate = Migrate()

client = Client()
models = ["gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]

def create_app():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/process-text', methods=['POST'])
    def process_text():
        data = request.json
        input_text = data['inputText']
        languages = data['selectedLanguages']
        results = {}

        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": input_text}]
                )
                output_text = response['choices'][0]['message']['content']
                translated_responses = {}

                for lang in languages:
                    translated_responses[lang] = GoogleTranslator(source='en', target=lang).translate(output_text)

                results[model] = translated_responses

            except Exception as e:
                results[model] = f"Error: {str(e)}"

        return jsonify({'translations': results})

    @app.route('/api/generate-image', methods=['POST'])
    def generate_image():
        data = request.json
        prompt = data['prompt']

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt
            )
            image_url = response.data[0].url
            return jsonify({'imageUrl': image_url})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app
