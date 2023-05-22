import sys
import pygame
import os
import json
import math
from urllib.request import urlretrieve
from pygame.locals import *
from random import randrange
from sys import exit
import cv2
import _thread
import threading

os.makedirs("./meta/", exist_ok=True)
os.makedirs("./resource/", exist_ok=True)


class Button:
    rect = (0, 0, 0, 0)
    text = 0
    text_color = (255, 0, 0)
    button_color = (255, 255, 255)

    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def set_rect(self, r):
        self.rect = r

    def set_text(self, t):
        self.text = t

    def set_rect_x(self, x):
        new_rect = (x, self.rect[1], self.rect[2], self.rect[3])
        self.rect = new_rect

    def set_rect_y(self, y):
        new_rect = (self.rect[0], y, self.rect[2], self.rect[3])
        self.rect = new_rect

    def set_rect_w(self, w):
        new_rect = (self.rect[0], self.rect[1], w, self.rect[3])
        self.rect = new_rect

    def set_rect_h(self, h):
        new_rect = (self.rect[0], self.rect[1], self.rect[2], h)
        self.rect = new_rect

    def show_button(self):
        button_text = game_font.render(
            self.text, True, self.text_color, (0, 0, 0))
        li_rect = (self.rect[0]-1, self.rect[1]-1,
                   self.rect[2]+2, self.rect[3]+2)
        pygame.draw.rect(screen, self.button_color, li_rect, 0)
        screen.blit(button_text, self.rect)

    def in_rect(self, x, y):
        inx = (x > self.rect[0]) and (x < (self.rect[0]+self.rect[2]))
        iny = (y > self.rect[1]) and (y < (self.rect[1]+self.rect[3]))
        return inx and iny


# 加载资源
def get_resource(storyIds):
    image_resource_fold = './resource/'+storyIds+'/image/'
    voice_resource_fold = './resource/'+storyIds+'/voice/'
    text_resource_fold = './resource/'+storyIds+'/text/'
    os.makedirs(image_resource_fold, exist_ok=True)
    os.makedirs(voice_resource_fold, exist_ok=True)
    os.makedirs(text_resource_fold, exist_ok=True)

    json_path = "./json/"

    with open(json_path+storyIds+'.json', 'r') as load_f:
        dojson = json.load(load_f)
        json_len = len(dojson['resource'])
        print(json_len)
        i = 1
        adult = dojson['adult']
        for r in dojson['resource']:

            fileName = ""
            fileName = r['fileName']

            loading_text = 'loading :' + str(i) + '/' + str(json_len)

            print(loading_text)

            loading_text_button = Button(loading_text_rect, 'ojbk')
            loading_text_button.show_button()

            path = r['path']
            md5 = r['md5']

            if (fileName[-1] == "g"):
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + \
                    path+"/"+md5+".jpg"

            if (fileName[-1] == "3"):
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + \
                    path+"/"+md5+".mp3"

            if (fileName[-1] == "4"):
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + \
                    path+"/"+md5+".mp4"

            if (fileName[-1] == "t"):
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + \
                    path + "/" + md5 + ".txt"

            name_list = fileName.split('/')
            length = len(name_list)
            name = name_list[length-1]
            if (adult == 3 and fileName[-1] == "t"):
                name = name.replace('06.txt', '05.txt')

            urlretrieve(url, image_resource_fold + name)
            print(name)
            i = i+1
    print("完毕")

# 创建meta


def load_meta(storyIds):

    file = open('./resource/'+storyIds+'/text/' +
                storyIds+'.txt', "r", encoding='utf8')

    meta_file = open('./meta/'+storyIds+"_meta.json", "w", encoding='utf8')

    text_data = file.read()
    text = text_data.split("\n\n")

    meta = '{"resource":['
    msg = 'null'
    playvoice = 'null'
    bg = 'null'
    new_resoucer = ''
    new_msg = ''
    for t in text:
        lines = t.split('\n')
        for i in lines:
            if 'msg' in i:
                msg = i.split(',')[-2].replace('</outline>',
                                               '').replace('<outline width=2 color=black>', '')
        for i in lines:
            if 'playvoice' in i:
                playvoice = i.split(',')[-1]
        for i in lines:
            if 'bg,' in i:
                bg = i.split(',')[1]
        for i in lines:
            if 'movie,' in i:
                bg = i.split(',')[1]

        if new_msg != msg:
            new_resoucer = '{"msg" : "'+msg+'","playvoice" : "' + \
                playvoice.split('/')[-1]+'","bg" :"' + \
                bg.split('/')[-1] + '"},\n'
            new_msg = msg
            meta = meta + new_resoucer

    meta = meta + ']}'
    meta = meta.replace('},\n]}', '}]}')

    meta_file.write(meta)

    file.close()
    meta_file.close()

    return meta

# 读取meta


def open_meta(storyIds):
    f = open("./meta/"+storyIds+"_meta.json", 'r', encoding='utf8')
    content = f.read()
    meta = json.loads(content)
    length = len(meta["resource"])
    return [meta, length]

# 载入cg


def load_cg(storyIds, image_name):
    cg_url = "./resource/"+storyIds+"/image/"+image_name
    print(cg_url)
    return pygame.image.load(cg_url).convert_alpha()

# hs列表相关
# 获取列表


def get_list():
    json_list = []
    files = os.listdir('./json/')
    for file in files:
        json_list.append(file.replace('.json', ''))
    return json_list

# 列表分页


def page_list(p, page_list):
    new_list = []
    list_len = len(json_list)
    i = 0
    while (i < 6) and (p*6+i < list_len):
        new_list.append(page_list[p*6+i])
        i = i+1
    return new_list

# 显示列表


def load_list(json_list):

    li_h = 200
    button_list = []
    for li in json_list:
        li_rect = (550, li_h, 200, 50)
        li_text = li
        li_button = Button(li_rect, li_text)
        li_button.show_button()
        button_list.append(li_button)
        li_h = li_h + 50
    return button_list


class play_video(threading.Thread):
    run_count = False
    loop_count = True

    def __init__(self, storyIds, index):
        threading.Thread.__init__(self)
        self.storyIds = storyIds
        self.index = index

    def set_run_count(self, count):
        self.run_count = count

    def set_loop_count(self, count):
        self.loop_count = count

    def run(self):
        while True:
            if self.run_count:
                break

            video_fold = './resource/' + self.storyIds + '/image/' + self.index
            video = cv2.VideoCapture(video_fold)
            success, video_image = video.read()
            run = success
            while run:
                if self.run_count:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                success, video_image = video.read()
                if success:
                    video_surf = pygame.image.frombuffer(
                        video_image.tobytes(), video_image.shape[1::-1], "BGR")
                    video_surf = pygame.transform.scale(video_surf, CG_SIZE)

                else:
                    if self.loop_count:
                        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    else:
                        self.run_count = True
                        break
                screen.blit(video_surf, (10, 0))
                pygame.display.flip()


# def play_video(storyIds,index):
#
#     video_fold = './resource/' + storyIds + '/image/' +index
#     video = cv2.VideoCapture(video_fold)
#     success, video_image = video.read()
#     video_control = False
#     run = success
#     while run:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#
#         success, video_image = video.read()
#         if success:
#             video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
#             video_surf = pygame.transform.scale(video_surf, CG_SIZE)
#             if video_control:
#                 print('break___________')
#                 break
#
#         else:
#             video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         screen.blit(video_surf, (10, 0))
#         pygame.display.flip()


# 常量
display_width = 1300
display_height = 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GAME_SIZE = (display_width, display_height)
CG_SIZE = (1280, 720)
TEXT_SIZE = (1000, 200)


# 初始化
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("DeepOne")

screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
game_font = pygame.font.Font('msgothic.ttc', 50)
text_font = pygame.font.Font('msgothic.ttc', 30)

# rect
next_button_rect = (1190, 900, 100, 50)
load_butto_rect = (400, 650, 100, 50)
play_button_rect = (800, 650, 100, 50)
message_rect = (450, 100, 400, 50)
pages_up_rect = (800, 550, 150, 50)
page_down_rect = (400, 550, 150, 50)
loading_text_rect = (450, 850, 400, 50)

# button
text_next_button = Button(next_button_rect, "next")
load_button = Button(load_butto_rect, 'LOAD')
play_button = Button(play_button_rect, 'PLAY')
pages_up_button = Button(pages_up_rect, "下一頁")
pages_down_button = Button(page_down_rect, "上一頁")


# ————————参数——————

# ————————控制参数————

# 寝室id
storyIds = ''
# 播放状态
is_play = False
is_main = True
json_selected = False
# 初始页码
json_list_page = 0

# 数据
# 寝室列表
json_list = get_list()
# 寝室数量
pages_size = math.ceil(len(json_list)/6)

video_control = False


while True:

    for event in pygame.event.get():

        

        if is_main:
            
            new_list = page_list(json_list_page, json_list)
            json_button_list = load_list(new_list)

            pages_up_button.show_button()
            pages_down_button.show_button()

            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                for bt in json_button_list:
                    if bt.in_rect(x, y):
                        json_file_name = bt.text
                        print(json_file_name)
                        json_selected = True


                if pages_up_button.in_rect(x, y):
                    json_list_page = json_list_page + 1
                    if json_list_page+1 > pages_size:
                        json_list_page = 0
                    new_list = page_list(json_list_page, json_list)
                    json_button_list = load_list(new_list)
                    screen.fill((0,0,0))

                if pages_down_button.in_rect(x, y):
                    json_list_page = json_list_page - 1
                    if json_list_page < 0:
                        json_list_page = pages_size-1
                    new_list = page_list(json_list_page, json_list)
                    json_button_list = load_list(new_list)
                    screen.fill((0,0,0))

        
        if json_selected:
            load_button.show_button()
            play_button.show_button()

            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                if load_button.in_rect(x,y):
                    get_resource(json_file_name)
                if play_button.in_rect(x,y):
                    is_play = True
                    json_selected = False
                    is_main = False
                    screen.fill((0,0,0))

        if is_play:
            print("playing")
            pass

        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            pass

    pygame.display.flip()
