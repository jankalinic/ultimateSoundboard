import os
import subprocess
import playsound
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from Sounds import Sound, SoundDirectory


# PATH VARS
root_directory = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root_directory, 'src')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')
# Upload folder
UPLOAD_FOLDER = os.path.join(root_directory, 'media')  # TODO: zmenit "/var/www/html/"

# FLASK VARS
app = Flask("vzp", template_folder=templates_dir)
app.static_folder = os.path.join(templates_dir, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'.mp3'}

# python VARS
sound_directories = list()


@app.route('/', methods=['POST', 'GET'])
def index(current_name="main"):
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
    return index(cur_name)


@app.route('/play_sound', methods=['POST', 'GET'])
def play_sound():
    playsound.playsound(os.path.join(UPLOAD_FOLDER, request.form.get("sound_file")))
#     mp3_file = request.form.get("sound_file")
#
#     if os.path.exists(os.path.join(UPLOAD_FOLDER, mp3_file)):
#         os.system("vzp-sender {0}".format(mp3_file))
#
#     return jsonify("Playing {0}".format(mp3_file))


@app.route('/stop_sound')
def stop_sound():
    # kill queue
    os.system("for pid in $(ps -ef | awk '/vzp-sender/ {print $2}'); do kill -9 $pid; done")
    # start proceses
    os.system("vzp-sender ")
    return jsonify("Stoping queue")


@app.route('/volume/<opt_volume>', methods=['POST', 'GET'])
def opt_volume(opt_volume):
    if opt_volume == "up":
        os.system("")
    elif opt_volume == "down":
        os.system("")
    else:
        return jsonify("Failed")

    return  jsonify("Volume")


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
    sound_dir_list = sorted([nm for nm in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, nm))])

    for sound_dir_single in sound_dir_list:
        sound_directories.append(SoundDirectory(sound_dir_single, os.path.join(UPLOAD_FOLDER, sound_dir_single)))


if __name__ == '__main__':
    load()
    app.run(host="0.0.0.0", port=9090, debug=True)
