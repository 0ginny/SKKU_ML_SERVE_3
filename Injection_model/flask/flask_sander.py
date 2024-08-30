from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    public_ip = get_public_ip()
    return render_template('index.html', public_ip=public_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
