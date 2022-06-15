import os
import subprocess

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, redirect, request, url_for, flash
from Sounds import Sound, SoundDirectory


# PATH VARS
root_directory = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root_directory, 'src')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')
# Upload folder
UPLOAD_FOLDER = os.path.join(root_directory, 'media')  # TODO: zmenit "/var/www/html/"

# FLASK VARS
app = Flask(__name__, template_folder=templates_dir)
app.static_folder = os.path.join(templates_dir, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'.mp3'}

# python VARS
sound_directories = list()


@app.route('/')
def index():
    return render_template(template,
                           directories=sound_directories,
                           hidden_styles=add_styles(sound_directories),
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


def load():
    sound_dir_list = sorted([name for name in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))])

    for sound_dir_single in sound_dir_list:
        sound_directories.append(SoundDirectory(sound_dir_single, os.path.join(UPLOAD_FOLDER, sound_dir_single)))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_styles(directory_list):
    id_list = ["#" + str(direct.get_id()) for direct in directory_list]
    target_list = [id_name + ":target" for id_name in id_list]

    css = """{0} {{\n
        display: none;\n
        width: auto;\n
        height: auto;
      }}\n
      \n
      {1} {{\n
        display: flex;\n
      }}\n
      """.format(", ".join(id_list), ", ".join(target_list))
    return css


if __name__ == '__main__':
    load()
    app.run(host="0.0.0.0", port=9090, debug=True)
