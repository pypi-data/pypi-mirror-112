
import sys

import flask
from . import mtcnn
import logging
import os
import cv2
import numpy as np

import werkzeug.datastructures
from PIL import Image

from matplotlib import pyplot as plt
import threading
from time import time
from app import flask_app
from flask import request

logger = logging.Logger('app_logger', level=2)

def console_logger( anony_img, anony_fname):

    plt.imsave(fname=anony_fname, arr=anony_img)

    logger.log(msg='Mission Completed! Check your image file in the directory.', level=1)
    return anony_img

def bb_blur_pool(bb, img_file):
    nblocks = 3
    ys = abs(bb['box'][0])
    ye = ys + abs(bb['box'][2])
    xs = abs(bb['box'][1])
    xe = xs + abs(bb['box'][3])
    px_x = int((xe - xs) / nblocks) - 1 if int((xe - xs) / nblocks) % 2 == 0 else int((xe - xs) / nblocks)
    px_y = int((ye - ys) / nblocks) - 1 if int((ye - ys) / nblocks) % 2 == 0 else int((ye - ys) / nblocks)
    img_file[xs:xe, ys:ye] = cv2.GaussianBlur(img_file[xs:xe, ys:ye], (33, 33), sigmaX=nblocks, sigmaY=nblocks)
    for i in range(1, nblocks + 1):
        img_file[xs:xs+(px_x*i), ys:ys+(px_y*i)] = cv2.GaussianBlur(img_file[xs:xs+(px_x*i), ys:ys+(px_y*i)], (px_x,px_y), sigmaX=0,
                                                                    sigmaY=0)

def fc_anonymizer(face_bbs, img_file, anony_fname):

    logging.log(msg='There are {0} faces found!'.format(len(face_bbs)), level=2)
    print('There are {0} faces found!'.format(len(face_bbs)))

    threads = []
    for bb in face_bbs:
        cthread = threading.Thread(target=bb_blur_pool, args=(bb, img_file))
        cthread.start()
        threads.append(cthread)

    for t in range(len(face_bbs)):
        threads[t].join()

    return console_logger(np.array(img_file, dtype=np.uint8), anony_fname)

@flask_app.route('/run_mtcnn/', methods = ['POST', 'GET'])
def run_mtcnn(path=None):
    root_dir = '/fakepath/anony_face/app/'
    file = werkzeug.datastructures.FileStorage(stream=request.files['photo'].stream)

    if not os.path.exists('/fakepath/anony_face/app/uploads/'):
        os.makedirs(name='/fakepath/anony_face/app/uploads', mode=0o777)

    save_p = root_dir + flask_app.config['UPLOADS'] + request.files['photo'].filename
    #  root_dir + flask_app.static_folder +
    request.files['photo'].save(save_p)
    print('file: ', save_p)
    img_f = np.array(Image.open(save_p), dtype=np.uint8)
    print('image file ' , img_f.shape)
    start_t = time()  # beginning timestamp
    
    mtcnn_obj = mtcnn.mtcnn.MTCNN()
    
    fext = str.split(save_p, '.')
    fsep = '/'  # default
    if str.lower(sys.platform) == 'linux':
        fsep = '/'
    elif str.lower(sys.platform) == 'windows':
        fsep = '\\'

    last_part = fext[0].split(fsep)[-1] + '_anony' + '.' + fext[1]
    path_parts = fext[0].split(fsep)
    path_parts[-1] = last_part
    anony_fname = root_dir + flask_app.config['UPLOADS'] + last_part
    print(anony_fname)

    face_bbs = mtcnn_obj.detect_faces(img_f)
    fc_fnd = len(face_bbs) > 0
    if not fc_fnd:
        logger.log(msg='Apologise. The image may not have humans’ faces.', level=1)
        return flask.make_response(flask.jsonify({'msg': 'Apologise. The image may not have humans’ faces.'}), 202)
        # flask app request response imp later
    else:
        start_an = time()
        pthread = threading.Thread(target=fc_anonymizer, args=(face_bbs, img_f, anony_fname))
        pthread.start()
        pthread.join()

        print('Time taken to anonymize {0} face(s): {1} seconds.'.format(len(face_bbs), time() - start_an))

    print('Time taken to resolve this program instance: {0} seconds.'.format(time() - start_t))
    logger.log(msg='Time taken to resolve this program instance: {0} seconds.'.format(time() - start_t), level=1)

    return flask.make_response(flask.jsonify({'file_path': flask_app.config['UPLOADS'] + last_part}), 202)
    # u'data:img/jpeg;base64,'+ base64.b64encode(img_f).decode('utf-8')}
    #json.dumps({'photo': img_f})

@flask_app.route('/download-image/<string:fimg>/', methods=['POST'])
def download_image(fimg):
    return flask.send_from_directory(directory=flask_app.config['UPLOADS'], path=fimg, filename=fimg, as_attachment=True)
