from flask_migrate import Migrate
from flask import Flask, request, jsonify, render_template
from models import db
from controllers import main
from g4f.client import Client
from deep_translator import GoogleTranslator
import markdown

# migrate = Migrate()

client = Client()
models = [ "gpt-4o", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"]

def create_app():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/sap')
    def modelling():
        return render_template('modelling.html')


    @app.route('/api/process-text', methods=['POST'])
    def process_text():
        input_text = request.json['inputText']
        language = request.json['language']
        results = {}

        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": GoogleTranslator(source=language, target='en').translate(input_text)}]
                )
                output_text = response.choices[0].message.content
                output = markdown.markdown(output_text)
                translated_responses = {}
                translated_responses['ru'] = GoogleTranslator(source='en', target='ru').translate(output)
                translated_responses['en'] = output
                return jsonify({'translations': translated_responses})
            except Exception as e:
                print(f"Error: {str(e)}")
                continue

    @app.route('/api/generate-image', methods=['POST'])
    def generate_image():
        prompt = request.json['prompt']

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt="a white siamese cat",
            )

            image_url = response.data[0].url
            print(f"Generated image URL: {image_url}")
            return {}

        except Exception as e:
             print(e)

    return app
