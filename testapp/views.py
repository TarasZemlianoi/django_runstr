from django.shortcuts import render
from moviepy.editor import *
import numpy as np
import pygame
from os import path


def index_page(request):
    return render(request, 'index.html')


def request_complete(request):
    text = request.GET['text']
    savepath = create_string(text)
    print(savepath)
    return render(request, 'request_ok.html', {'text': text, 'path': savepath[0]})


def create_string(text):
    pygame.init()

    # параметры видеоизображения
    framesize = 100
    movie_time = 3
    fps = 30
    font_size = 15
    myfont = pygame.font.SysFont('Times', font_size, bold=False, italic=False)
    frames_qty = movie_time * fps

    # ввод текста
    input_text = text
    mytext = myfont.render(input_text, False, (255, 255, 255))

    # преобразование изображения текста в numpy array
    txt_np = pygame.surfarray.array3d(mytext)
    txt_np = txt_np.transpose((1, 0, 2))

    # размеры, проходимый путь, покадровое смещение, координаты бегущей строки
    txt_length = mytext.get_size()[0]
    txt_height = mytext.get_size()[1]
    txt_move_size = framesize + txt_length
    frame_step = txt_move_size / frames_qty
    txt_x = 0
    txt_y = (framesize - txt_height) // 2

    # массив кадров
    img_array = []

    # создание кадров
    for _ in range(0, frames_qty):
        txt_x += frame_step
        img = np.zeros((framesize, framesize, 3), dtype=np.uint8)
        txt_np_slice = txt_np[:, abs(np.minimum(0, framesize - round(txt_x))):
                                 np.minimum(txt_length, round(txt_x))].copy()
        img[txt_y:txt_y + len(txt_np_slice),
        np.maximum(0, framesize - round(txt_x)):
        np.maximum(0, framesize - round(txt_x)) + len(txt_np_slice[0])] = txt_np_slice
        img_array.append(img)

    clip = ImageSequenceClip(img_array, fps=fps, durations=movie_time)
    filename = path.expanduser('~') + "\\Downloads\\" + input_text + '.mp4'
    clip.write_videofile(input_text + '.mp4')
    clip.write_videofile(filename)
    return (filename, input_text + '.mp4')






