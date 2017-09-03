import os
os.system("protoc object_detection/protos/*.proto --python_out=.")
os.system("export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim")
os.system("python detect.py --source=1 --num-workers=4")
import threading
import time
import timeit
import tensorflow as tf

from flask import Flask, render_template, redirect, request, flash, session, url_for, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap 
from werkzeug.utils import secure_filename
from detect import image_detect
from imagescrape import makeZip

UPLOAD_FOLDER = os.path.abspath('static/images/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)

app.secret_key = 'X'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)

detection_graph = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delay_delete(delay, path):
    time.sleep(delay)
    os.remove(path)
    return

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def scrape():
    os.system('rm *.zip')
    if request.method == 'POST':
        query = str(request.form['query'])
        ZIPFILE = makeZip(query)
        session['zipfile'] = ZIPFILE
        return render_template('download.html', filename=ZIPFILE)

@app.route('/scrape')
def returnFile():
    zipfile = session.get('zipfile', None)
    ZIPFILE = str(zipfile)
    print ZIPFILE
    del_thread = threading.Thread(target=delay_delete, args=(5, '{}'.format(ZIPFILE)))
    del_thread.start()
    return send_file(ZIPFILE, attachment_filename=ZIPFILE)

@app.route('/detect', methods=['GET', 'POST'])
def render():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(url_for(render))

        file = request.files['photo']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for(render))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if (((os.stat(UPLOAD_FOLDER + '/' + filename).st_size)/1000) > 500):
                flash('Image file too big')
                return redirect(url_for(render))

            start_time = timeit.default_timer()

            image_detect(filename, detection_graph)

            elapsed = timeit.default_timer() - start_time
            print elapsed

            del_thread = threading.Thread(target=delay_delete, args=(5, '{}/{}'.format(UPLOAD_FOLDER, filename)))
            del_thread.start()
            return render_template('imagesubmit.html', filename=filename)

    return render_template('detect.html')

if __name__ == "__main__":
    app.run(port=8000)
    '''detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')'''