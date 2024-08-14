from flask import Flask, request, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

# In-memory database
url_mapping = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_code = generate_short_code()
    url_mapping[short_code] = original_url
    shortened_url = url_for('redirect_to_url', short_code=short_code, _external=True)
    return render_template('index.html', shortened_url=shortened_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
