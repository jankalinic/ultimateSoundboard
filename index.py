import difflib
import os
import subprocess
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, redirect, request, url_for
from Sounds import Sound, SoundDirectory


# PATH VARS
root_directory = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root_directory, 'src')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')
search_template = env.get_template('search.html')

# Upload folder
UPLOAD_FOLDER = os.path.join(root_directory, 'media')

# FLASK VARS
app = Flask("vzp", template_folder=templates_dir)
app.static_folder = os.path.join(templates_dir, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'.mp3'}

# python VARS
sound_directories = list()


@app.route('/', methods=['POST', 'GET'])
def index(current_name="main"):
    load()

    for directory in sound_directories:
        if directory.get_name() == current_name.upper():
            current_directory = directory
            break

    return render_template(template,
                           directories=sound_directories,
                           cur_dir=current_directory,
                           style_css=url_for('static', filename='style.css'),
                           scripts_js=url_for('static', filename='scripts.js'))


@app.route('/name/<cur_name>', methods=['POST', 'GET'])
def name(cur_name):
    load()
    return index(cur_name)


@app.route('/play_sound', methods=['POST', 'GET'])
def play_sound():
    file_to_play = os.path.join(root_directory, UPLOAD_FOLDER, request.form.get("sound_file"))
    os.system("{0}/vzp-send {1}".format(root_directory, file_to_play))
    return "Playing"


@app.route('/stop_sound', methods=['POST', 'GET'])
def stop_sound():
    # kill queue
    os.system("for pid in $(ps -ef | awk '/vzp-send/ {print $2}'); do kill -9 $pid; done")
    os.system("for pid in $(ps -ef | awk '/mpg123/ {print $2}'); do kill -9 $pid; done")
    return "Stopped"


@app.route('/set_volume', methods=['POST', 'GET'])
def set_volume():
    opt_vol = request.form.get("volume")
    if opt_vol == "up":
        os.system("amixer set Master 10%+")
    elif opt_vol == "down":
        os.system("amixer set Master 10%-")
    return "Volume"


@app.route('/normalize', methods=['POST', 'GET'])
def normalize():
    os.system("mp3gain -r {0}/*/*.mp3".format(os.path.join(root_directory, UPLOAD_FOLDER)))
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(root_directory, UPLOAD_FOLDER, request.form.get("folder"), f.filename))

    load()
    return redirect(url_for('index'))


@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_path = os.path.join(root_directory, UPLOAD_FOLDER, request.form.get("folder_name"))
    if not os.path.exists(folder_path):
        os.system("mkdir " + folder_path)

    load()
    return redirect(url_for('index'))


@app.route('/read', methods=['POST'])
def read():
    file = os.path.join(root_directory, UPLOAD_FOLDER, "main", "tts_output.mp3")
    os.system("gtts-cli {0} --lang en --output {1}".format(request.form.get("text"), file))
    time.sleep(3)
    os.system("{0}/vzp-send {1}".format(root_directory, file))
    load()
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get("search_term")
    sound_list = list()
    folders_list = [x[0] for x in os.walk(UPLOAD_FOLDER)]
    folders_list.pop(0)

    for folder in folders_list:
        files_in_folder = [x[2] for x in os.walk(folder)][0]
        for file in files_in_folder:
            if search_term in file:
                sound_list.append(Sound(name=file, dir_id=folder.split("/")[-1], path=os.path.join(folder, file)))

    return render_template(search_template,
                           directories=sound_directories,
                           search_term=search_term,
                           sounds=sound_list,
                           style_css=url_for('static', filename='style.css'),
                           scripts_js=url_for('static', filename='scripts.js'))


def load():
    global sound_directories
    sound_directories = list()
    sound_dir_list = sorted([nm for nm in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, nm))])

    for sound_dir_single in sound_dir_list:
        sound_directories.append(SoundDirectory(sound_dir_single, os.path.join(UPLOAD_FOLDER, sound_dir_single)))


def run():
    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == '__main__':
    run()
