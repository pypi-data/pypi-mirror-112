import click
import sys
# import cv2.gapi
import mtcnn
import logging
import os
import cv2
import numpy as np
# import imutils
from matplotlib import pyplot as plt
import threading
from time import time
# from app import flask_app
# from flask import request

@click.command()

@click.argument('file_paths')
@click.option('--save_path', default='')
def main(file_paths, save_path=None):
    face_anonymizer(file_paths, save_path)


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

    logger.log(msg='There are {0} faces found!'.format(len(face_bbs)), level=2)
    print('There are {0} faces found!'.format(len(face_bbs)))

    threads = []
    for bb in face_bbs:
        cthread = threading.Thread(target=bb_blur_pool, args=(bb, img_file))
        cthread.start()
        threads.append(cthread)

    for t in range(len(face_bbs)):
        threads[t].join()

    console_logger(np.array(img_file, dtype=np.uint8), anony_fname)

def face_anonymizer(img_n, save_path='', file_hook=None):

    t_list = []
    start_t = time()  # beginning timestamp
    mtcnn_obj = mtcnn.MTCNN(min_face_size=10)
    anony_fname= ''
    if type(img_n) is list:
        for f in img_n:
            t = threading.Thread()
            t.start()

            f = os.path.abspath(f)
            fext = str.split(f, '.')
            fsep = '/'  # default
            if str.lower(sys.platform) == 'linux':
                fsep = '/'
            elif str.lower(sys.platform) == 'windows':
                fsep = '\\'

            last_part = fext[0].split(fsep)[-1] + '_anony'
            path_parts = fext[0].split(fsep)
            path_parts[-1] = last_part
            if save_path != '':
                if not os.path.exists(save_path):
                    anony_fname = save_path + fsep + last_part + '.' + fext[1]
                elif os.path.isdir(save_path):
                    print("Non-existing save path!")
                    return
            else:
                anony_fname = fsep.join(path_parts) + '.' + fext[1]

            img_f = np.array(plt.imread(f), dtype=np.uint8)

            # img_grayscale = cv2.cvtColor(img_f, cv2.COLOR_RGB2GRAY)
            # img_grayscale = imutils.resize(img_grayscale, width=400)

            # det = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            # face_bbs = det.detectMultiScale(img_grayscale, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30),
            #                            flags=cv2.CASCADE_SCALE_IMAGE)

            face_bbs = mtcnn_obj.detect_faces(img_f)
            fc_fnd = len(face_bbs) > 0
            if not fc_fnd:
                logger.log(msg='Apologise. The image may not have humans’ faces.', level=1)
                print('Apologise. The image may not have humans’ faces.')
                return
                # flask app request response imp later
            else:
                print('Anonymized image will be saved to ', anony_fname)

                start_an = time()
                fc_anonymizer(face_bbs, img_f, anony_fname)
                print('Time taken to anonymize {0} face(s): {1} seconds.'.format(len(face_bbs), time() - start_an))

            t_list.append(t)

        for t in range(len(img_n)):
            t_list[t].join()
    else:
        img_n = os.path.abspath(img_n)
        fext = str.split(img_n, '.')
        fsep = '/' #default
        if str.lower(sys.platform) == 'linux':
            fsep = '/'
        elif str.lower(sys.platform) == 'windows':
            fsep = '\\'

        path_parts = fext[0].split(fsep)
        last_part = fext[0].split(fsep)[-1] + '_anony'
        path_parts[-1] = last_part

        if save_path != '':
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            elif not os.path.isdir(save_path):
                print("Not a directory!")
                return

            anony_fname = save_path + fsep + last_part + '.' + fext[1]
        else:
            anony_fname = fsep.join(path_parts) + '.' + fext[1]

        img_f = np.array(plt.imread(img_n), dtype=np.uint8)

        face_bbs = mtcnn_obj.detect_faces(img_f)
        fc_fnd = len(face_bbs) > 0
        if not fc_fnd:
            logger.log(msg='Apologise. The image may not have humans’ faces.', level=1)
            print('Apologise. The image may not have humans’ faces.')
            return
            # flask app request response imp later
        else:
            print('Anonymized image will be saved to ', anony_fname)

            start_an = time()
            fc_anonymizer(face_bbs, img_f, anony_fname)
            anony_time = time() - start_an

            print('Time taken to anonymize {0} face(s): {1} seconds.'.format(len(face_bbs), anony_time))
        total_time = time() - start_t
        if file_hook:
            file_hook.write((anony_fname + ',' + str(len(face_bbs)) + ',' + str(anony_time) + ',' + str(total_time) + '\n'))

        print('Time taken to resolve this program instance: {0} seconds.'.format(total_time))
        logger.log(msg='Time taken to resolve this program instance: {0} seconds.'.format(time() - start_t), level=1)

if __name__ == '__main__':
    main()
    # import shlex
    # main(shlex.split(
    #     '''file_paths
    #     --save_path '' '''))
