import os
import subprocess

from jinja2 import Environment, FileSystemLoader
from flask import Flask
from flask import render_template, redirect, request, url_for
from werkzeug.utils import secure_filename



root_directory = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root_directory, 'src')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')

UPLOAD_FOLDER = os.path.join(root_directory, 'media')

app = Flask(__name__)
app.static_folder = templates_dir + '/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template(template,
                           style_css=url_for('static', filename='style.css'),
                           scripts_js=url_for('static', filename='scripts.js'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    return redirect("/#{}".format(request.form.get("search_name")))  # works


@app.route('/volumeup', methods=['POST', 'GET'])
def volumeup():
    # subprocess.run("amixer set Master 10%+")
    return redirect("/")


@app.route('/volumedown', methods=['POST', 'GET'])
def volumedown():
    # subprocess.run("amixer set Master 10%-")
    return redirect("/")


@app.route('/stop', methods=['POST', 'GET'])
def stop():
    # subprocess.run("kill process")  # Todo
    return redirect("/")


@app.route('/normalize', methods=['POST', 'GET'])
def normalize():
    # subprocess.run("mp3gain -r *.mp3")
    return redirect("/")


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(root_directory, request.form.get("folder"), f.filename))

    return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)
