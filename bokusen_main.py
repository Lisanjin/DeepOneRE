import sys,pygame
import os
import re
import json
from urllib.request import urlretrieve
from pygame.locals import*
from sys import exit
import time
import threading
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import math



#常量
display_width = 960
display_height = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)    
GAME_SIZE = (display_width,display_height)
CG_SIZE = (960,540)


#初始化
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("BOKUSEN")


screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
game_font = pygame.font.Font('msgothic.ttc',50)
text_font = pygame.font.Font('msgothic.ttc',30)
all_text_rect = pygame.Rect(30, 550, 930, 200)



#指令相关方法
def get_json(json_file_name):
    with open("./json/"+json_file_name+".json",'r') as load_f:     
        bokujson = json.load(load_f)
        return bokujson


def get_commands(jsonfile):        
    bokujson = jsonfile
    commands = bokujson['data']['code']['commands']
    return commands


def read_commands(jsonfile,num): 
        bokujson = jsonfile
        commands= get_commands(jsonfile)

        while(num<len(commands)):
        
            # print(commands[num])
            
            tags = bokujson['data']['code']['tags']
            tag = tags[int(commands[num][0])]

            parameters = bokujson['data']['code']['parameters']
            param = parameters[int(commands[num][1])]



            result = execut_commands(tag,param)    

            num = num +1

            if result == "stop":
                global commands_count
                commands_count = num
                break
            
        if num == len(commands):
            global cg_control, txt_control, anime_control, sound_control, is_play, is_main, json_list_page, json_selected
            cg_control = Cg_Controller()
            txt_control = Text_Controller()
            anime_control = Anime_Controller()
            sound_control = Sound_Controller()
            commands_count = 0
            is_play = False
            is_main = True
            json_list_page = 0
            json_selected = False
            screen.fill((0,0,0))


            
def execut_commands(tag,param):
    if tag=="bgmopt":
        pass
    if tag=="playbgm":
        print("playbgm")
        sound_file = get_sounds(param[-1])
        
        sound_control.set_sound(sound_file)

        sound_control.start()

    if tag=="image":
        
        if param[16]!="1":
            image_num = int(param[-3])
            image_type = jsonfile['data']['code']['images'][image_num].replace("https://resource-asw.bokusen.net/resource/img/script/","").split("/")[0] 
            image_order = param[-8]

            cg = get_images(image_num)

            if image_order == "fore":
                cg_control.set_fore_img(cg)
            if image_order == "back":
                cg_control.set_back_img(cg)
            if image_type == "ev":
                cg_control.set_fore_img(cg)
                cg_control.set_back_img(cg)

            cg_control.show_cg()
        
    if tag=="trans":
        pass
    if tag=="wt":
        pass
    if tag=="move":
        pass
    if tag=="wm":
        pass
    if tag=="playse":
        
        sound_file = get_sounds(param[-1])
        
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    if tag=="articles":
        txt = get_articles(param[0])
        txt_control.set_text(txt)
        txt_control.show_text()
        
    if tag=="r":
        pass
    if tag=="p":
        pass

    if tag=="cm":
        txt_control.clear_text()
        return "stop"
    
    if tag=="stopse":
        pass

    if tag=="animstart":
        if len(param[-3])>10:
            anime_control.set_loop(True)
            anime_control.set_anime_list(param[-3])
            anime_control.start()

    if tag=="animstop":
        anime_control.set_loop(False)

    if tag=="wait":
        pass
    if tag=="fadeoutbgm":
        sound_control.set_play_status(False)
    if tag=="wb":
        pass
    if tag=="fadebgm":
        pass
    if tag=="seopt":
        pass
    if tag=="fadese":
        pass
    if tag=="wf":
        pass
    return "end"

#加载资源
def get_images(num):  
    global json_file_name
    resouce_path =  "./resource/"+json_file_name+"/images/"

    file_names = os.listdir(resouce_path)
    pattern = re.compile("^"+str(num)+"\..*")
    matching_file_names = [f for f in file_names if pattern.match(f)]

    print(resouce_path+matching_file_names[0])

    return  pygame.image.load(resouce_path+matching_file_names[0]).convert_alpha()   

def get_sounds(num):    
    global json_file_name
    resouce_path =  "./resource/"+json_file_name+"/sounds/"

    file_names = os.listdir(resouce_path)
    pattern = re.compile("^"+str(num)+"\..*")
    matching_file_names = [f for f in file_names if pattern.match(f)]

    return resouce_path+matching_file_names[0]

def get_articles(num):    
    global jsonfile
    bokujson = jsonfile
    articles = bokujson['data']['code']['articles']
    return articles[int(num)]

#资源下载
def get_resource(json_file_name):
    os.makedirs("./resource/"+json_file_name+"/sounds/", exist_ok=True)
    os.makedirs("./resource/"+json_file_name+"/images/", exist_ok=True)

    print("你先别急")
    with open("./json/"+json_file_name+".json",'r') as load_f:     
        bokujson = json.load(load_f)
        images = bokujson['data']['code']['images']
        sounds = bokujson['data']['code']['sounds']
        count = 0
        while(count<len(sounds)):
            endname = '.'+sounds[count].split('.')[-1]
            download_times = 5
            while download_times > 0:
                try:
                    urlretrieve(sounds[count], "./resource/"+json_file_name+"/sounds/"+str(count)+endname)
                    print(str(count)+endname)
                except:
                    print("error downloading : " +str(count)+endname)
                    download_times = download_times - 1
                    continue
                else:
                    break

            m4a_file = "./resource/"+json_file_name+"/sounds/"+str(count)+endname
            wav_file = m4a_file.replace("m4a","wav")
        
            AudioSegment.from_file(m4a_file).export(wav_file, format="wav")
            os.remove(m4a_file)

            count=count+1

        print("sounds end")
        count = 0
        while(count<len(images)):
            endname = '.'+images[count].split('.')[-1]
            download_times = 5
            while download_times > 0:
                try:
                    urlretrieve(images[count], "./resource/"+json_file_name+"/images/"+str(count)+endname)
                    print(str(count)+endname)
                except:
                    print("error downloading : " +str(count)+endname)
                    download_times = download_times - 1
                    continue
                else:
                    break
            count=count+1
        print("images end")
    print("下好了，开冲！")

class Button:
    is_button_on_screen = False
    rect=(0,0,0,0)
    text=0
    text_color = (255, 0, 0)
    button_color = (255, 255, 255)

    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def set_rect(self,r):
        self.rect = r

    def set_text(self,t):
        self.text = t

    def set_rect_x(self,x):
        new_rect = (x,self.rect[1],self.rect[2],self.rect[3])
        self.rect  = new_rect

    def set_rect_y(self,y):
        new_rect = (self.rect[0],y,self.rect[2],self.rect[3])
        self.rect  = new_rect

    def set_rect_w(self,w):
        new_rect = (self.rect[0],self.rect[1],w,self.rect[3])
        self.rect  = new_rect

    def set_rect_h(self,h):
        new_rect = (self.rect[0],self.rect[1],self.rect[2],h)
        self.rect  = new_rect

    def show_button(self):
        self.is_button_on_screen= True
        button_text = game_font.render(self.text, True, self.text_color, (0, 0, 0))
        li_rect = (self.rect[0]-1,self.rect[1]-1,self.rect[2]+2,self.rect[3]+2)
        pygame.draw.rect(screen, self.button_color, li_rect, 0)
        screen.blit(button_text, self.rect)

    def in_rect(self, x, y):
        inx = (x>self.rect[0]) and (x<(self.rect[0]+self.rect[2]))
        iny = (y>self.rect[1]) and (y<(self.rect[1]+self.rect[3]))
        return inx and iny

class Cg_Controller():
    fore_img = pygame.image.load("base_back.png").convert_alpha()
    back_img = pygame.image.load("base_back.png").convert_alpha()

    def set_fore_img(self,img):
        self.fore_img = img

    def set_back_img(self,img):
        self.back_img = img

    def show_cg(self):
        self.fore_img = pygame.transform.scale(self.fore_img, CG_SIZE)
        self.back_img = pygame.transform.scale(self.back_img, CG_SIZE)
        screen.blit(self.back_img, (0,0))
        screen.blit(self.fore_img, (0,0))
        pygame.display.flip() 

class Text_Controller():

    textRect =[(30,550,930,50),(30,600,930,50),(30,650,930,50),(30,700,930,50)] 
    text = ["","","",""]
    controller_stack=0

    def set_text(self,txt):
        
        self.text[self.controller_stack] = txt
        self.controller_stack = self.controller_stack+1

    def show_text(self):
        i = 0
        while(i<len(self.text)):
            message = text_font.render(self.text[i],True,WHITE,(0,0,0))
            screen.blit(message,self.textRect[i])
            i=i+1

    def clear_text(self):
        self.text = ["","","",""]
        self.controller_stack=0
        
class Anime_Controller(threading.Thread):
    anime_list=[] 
    fps = 15
    loop = True

    def __init__(self):
        threading.Thread.__init__(self)

    def set_anime_list(self,str):
        self.anime_list = str.rstrip().split(" ")

    def set_loop(self,status):
        self.loop = status
        
    def run(self):
        while self.loop:
            i = 0
            while i<len(self.anime_list):
                img = get_images(int(self.anime_list[i]))
                img = pygame.transform.scale(img, CG_SIZE)

                screen.blit(img,(0,0))
                pygame.display.flip() 
                time.sleep(1/self.fps)
                i=i+1
                if i==len(self.anime_list):
                    i=0
                if not self.loop:
                    break

class Sound_Controller(threading.Thread):
    sounds_resource = ""
    is_play = True

    def __init__(self):
        threading.Thread.__init__(self)

    def set_sound(self,s):
        self.sounds_resource= s

    def set_play_status(self,status):
        self.is_play = status

    def run(self):
        while self.is_play:

            print("play:"+self.sounds_resource)
            sound = AudioSegment.from_file(self.sounds_resource)
            
            play(sound, loop=True)

            if not self.is_play:

                break

        
#hs列表
#获取列表
def get_list():
    json_list = []
    files= os.listdir('./json/')
    for file in files:
        json_list.append(file.replace('.json',''))
    return json_list

#列表分页
def page_list(p,page_list):
    new_list=[]
    list_len = len(json_list)
    i=0
    while (i<6) and (p*6+i <list_len):
        new_list.append(page_list[p*6+i])
        i= i+1
    return new_list

#显示列表
def load_list(json_list):

    li_h = 200
    button_list=[]
    for li in json_list :
        li_rect =(200,li_h,600,50)
        li_text = li
        li_button = Button(li_rect,li_text)
        li_button.show_button()
        button_list.append(li_button)
        li_h = li_h + 50        
    return button_list


#数据
json_file_name = "demo"
jsonfile = get_json(json_file_name)
commands = get_commands(jsonfile)
json_list = get_list()
pages_size = math.ceil(len(json_list)/6)

#控制器
cg_control = Cg_Controller()
txt_control = Text_Controller()
anime_control = Anime_Controller()
sound_control = Sound_Controller()
commands_count = 0
is_play = False
is_main = True
json_list_page = 0
json_selected = False

pages_up_rect = (600,550,150,50)
page_down_rect = (150,550,150,50)
load_rect = (600,650,150,50)
play_rect = (150,650,150,50)


pages_up_button = Button(pages_up_rect,"下一页")
pages_down_button = Button(page_down_rect,"上一页")
load_button = Button(load_rect,"load")
play_button = Button(play_rect,"play")


while True:
 
    for event in pygame.event.get():
        if is_play:

            if event.type == MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (0, 0, 0), all_text_rect)
            
                read_commands(jsonfile,commands_count)

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
                    

        if is_main:
            new_list =  page_list(json_list_page,json_list)
            json_button_list = load_list(new_list)

            pages_up_button.show_button()
            pages_down_button.show_button()

            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                print(json_list_page)

                

                for bt in json_button_list:
                    if bt.in_rect(x,y):
                        json_file_name= bt.text
                        jsonfile = get_json(json_file_name)
                        commands = get_commands(jsonfile)

                        

                        json_selected = True

                        print(bt.text)

                if pages_up_button.in_rect(x,y):
                    json_list_page = json_list_page + 1
                    if json_list_page+1 > pages_size:
                        json_list_page = 0
                    new_list =  page_list(json_list_page,json_list)
                    json_button_list = load_list(new_list)

                if pages_down_button.in_rect(x,y):
                    json_list_page = json_list_page - 1
                    if json_list_page < 0 :
                        json_list_page = pages_size-1
                    new_list =  page_list(json_list_page,json_list)
                    json_button_list = load_list(new_list)


        
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            
            pass
            


            # get_resource("json_file_name")

            # pygame.draw.rect(screen, (0, 0, 0), all_text_rect)
            
            # read_commands(jsonfile,commands_count)



    pygame.display.flip()         