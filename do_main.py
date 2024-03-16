import pygame
import os,re
import json
import math
from urllib.request import urlretrieve
from pygame.locals import *
from random import randrange
from sys import exit
import cv2
import threading
import hashlib
import requests
import concurrent.futures
import time
import webbrowser
os.makedirs("./meta/", exist_ok=True)
os.makedirs("./resource/", exist_ok=True)
os.makedirs("./episode/", exist_ok=True)

user_setting_file =  open("settings.json",'r',encoding='utf8') 
user_setting = json.load(user_setting_file)
user_setting_file.close()

print('----用户设置，请到setting.json中修改------')
print(user_setting)
print('----------------------------------------')

class Button:
    rect = (0, 0, 0, 0)
    text = 0
    text_color = (255, 0, 0)
    button_color = (255, 255, 255)
    button_image =""

    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def set_img(self,img):
        self.button_image = img

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
    
    def show_image(self):
        cg = pygame.image.load(self.button_image).convert_alpha()
        screen.blit(cg, self.rect[:2])

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

def getMD5(input):
    input = '47cd76e43f74bbc2e1baaf194d07e1fa' + input
    result = hashlib.md5(input.encode()) 
    return result.hexdigest() 

def get_real_path(str1):
    e=''
    i=''
    a=''
    n=''
    if str1[0]=='c' or str1[0]=='d' or str1[0]== 'e' or str1[0]=='f':
        e = str1[6:8]+'/'
        i = str1[2:4] + "/"
        a = str1[4:6] + "/"
        n = str1[0:2] + "/" 
    elif str1[0]=='8' or str1[0] =='9' or str1[0]=='a' or str1[0] =='b':
        e = str1[4:6]+ "/"
        i = str1[0:2]+ "/"
        a = str1[6:8]+ "/"
        n = str1[2:4]+ "/"
    elif int(str1[0])>=4 and int(str1[0])<=7:
        e = str1[2:4]+ "/"
        i = str1[6:8]+ "/"
        a = str1[0:2]+ "/"
    elif int(str1[0])>=0 and int(str1[0])<=3:
        e = str1[0:2]+ "/"
        i = str1[4:6]+ "/"
    return  e + i + a + n

def get_url(file_name):
    cdn_url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_game_hd/"
    md5 = getMD5(file_name)
    path = get_real_path(md5)
    file_end = '.'+file_name.split(".")[-1]
    if '.atlas.txt' in file_name:
        file_end = '.atlas.txt'
    return cdn_url+path+md5+file_end

def download_file(url, filename):

    print(f'Downloading {filename}...')
    if os.path.exists(filename):
        print(f'{filename} 已下载，跳过.')
        return
    download_times = 5
    while download_times > 0:
        try:
            urlretrieve(url, filename)
        except:
            print("error downloading : " + filename)
            download_times = download_times - 1
            continue
        else:
            break
    print(f'{filename} downloaded.')

# 加载预览图
def load_preview(json_list):
    print("加载预览图……")
    os.makedirs('./episode/', exist_ok=True)
    for json_file in json_list:
        episode_name= "gallery/episode/"+json_file.split("_")[0]+".png"
        episode_url = get_url(episode_name)
        download_file(episode_url,"episode/"+json_file.split("_")[0]+".png")
    print("加载预览图完成")

# 加载资源
def get_resource(jsonId):

    json_path = "./json/"

    with open(json_path+jsonId+'.json', 'r') as load_f:
        dojson = json.load(load_f)
        file_dict = {}
        for r in dojson['resource']:
            fileName = "./resource/"+jsonId+"/"+r['fileName']
            name = fileName.split("/")[-1]
            path = r['path']
            os.makedirs(fileName.replace("/"+name,""),exist_ok=True)
            md5 = r['md5']
            end = fileName.split(".")[-1]

            url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + path+"/"+md5+"."+ end
            file_dict[url] = fileName

    with concurrent.futures.ThreadPoolExecutor(max_workers=下载线程数) as executor:
            futures = [executor.submit(download_file, url, filename) for url, filename in file_dict.items()]

    print("完毕")


# hs列表相关

# 重整json格式
def rename_json_list():
    files = os.listdir('./json/')
    for file in files:
        with open('./json/'+file,"r",encoding="utf8") as f:
            json_data = json.loads(f.read())
            
            new_name = str(json_data["storyIds"][0])
            adult = str(json_data["adult"])
            if adult != "1":
                new_name = new_name+"_"+adult
            new_name = new_name + ".json"
        os.rename('./json/'+file,'./json/'+new_name)

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
    while (i < 9) and (p*9+i < list_len):
        new_list.append(page_list[p*9+i])
        i = i+1
    return new_list

# 显示列表
def load_list(json_list):

    li_h = 100
    li_w = 150
    change_cow = 0
    button_list = []
    for li in json_list:
        if change_cow % 3 == 0:
            li_w = li_w+200
            li_h = 100

        li_rect = (li_w, li_h, 192 , 108)
        li_text = li
        li_button = Button(li_rect, li_text)
        li_button.set_img("./episode/"+li.split('_')[0] + '.png')
        li_button.show_image()
        button_list.append(li_button)
        li_h = li_h + 120
        change_cow = change_cow + 1
    return button_list


class play_video(threading.Thread):
    run_count = False
    loop_count = True
    video_file_name = ""

    def __init__(self):
        threading.Thread.__init__(self)

    def set_video_file_name(self,video_file_name):
        self.video_file_name = video_file_name

    def set_run_count(self, count):
        self.run_count = count

    def set_loop_count(self, count):
        self.loop_count = count

    def run(self):
        while True:
            if self.run_count:
                break

            video_fold = './resource/' + jsonId + '/' + self.video_file_name
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


# 播放指令相关
def read_adv(jsonId):
    with open("./json/"+jsonId+'.json', 'r') as f:
        dojson = json.load(f)
        resources= dojson["resource"]
        for resource in resources:
            if "text" in resource["fileName"]:
                fileName = resource["fileName"]
                break

    txt_path = "./resource/"+jsonId+"/"+fileName
    commands =[]
    with open(txt_path, "r", encoding='utf8') as f:
        commands= f.readlines()
    return commands

def read_command(commands,count):
    while(count<len(commands)):
        
        command = commands[count].strip()
        params = command.split(",")
        print(count,params[0])
        if params[0] == "name":
            pygame.draw.rect(screen, (0,0,0), (20,730,1300,50))
            if "<outline width=2 color=black>" in params[1] :
                name = params[1].replace("<outline width=2 color=black>","").replace("</outline>","")
                name = name.replace("<size=27>","").replace("</size>","")
                if "<ruby>" in name:
                    pattern = re.compile(r'<ruby>(.*?)</ruby>')
                    matches = pattern.findall(text)
                    for r in matches:
                        name = name.replace("<ruby>"+r+"</ruby>",r.split("|")[0])
            else:
                name = '  '
            name_text = text_font.render(name, True, WHITE, (0, 0, 0))
            screen.blit(name_text, (20,730,1300,50))

        elif params[0] == "bg":
            if params[1] != "color_0_0_0":
                img_path = "./resource/"+jsonId+"/"+params[1]
                cg = pygame.image.load(img_path).convert_alpha()
            else:
                cg = pygame.image.load('color_0_0_0.jpg').convert_alpha()
            screen.blit(cg, (10, 0))

        elif params[0] == "playvoice":
            voice_path = "./resource/"+jsonId+"/"+params[2]
            pygame.mixer.music.load(voice_path)
            pygame.mixer.music.play()

        elif params[0] == "movieoff":
            global th_count
            try:
                globals()["th_"+th_count].set_run_count(True)
                print("关闭上个视频线程")
            except:
                print(th_count)
                print("关闭上个视频线程失败")
        
        elif params[0] == "movie":
            movie_file_list = params[1].split(":")
            if len(movie_file_list)==1:
                movie_file= movie_file_list[0]
            if len(movie_file_list)==2:
                video_file = './resource/' + jsonId + '/' + movie_file_list[0]
                video = cv2.VideoCapture(video_file)

                while True:
                    success, video_image = video.read()
                    if success:
                        video_surf = pygame.image.frombuffer(
                            video_image.tobytes(), video_image.shape[1::-1], "BGR")
                        video_surf = pygame.transform.scale(video_surf, CG_SIZE)
                        screen.blit(video_surf, (10, 0))
                        pygame.display.flip()
                    else:
                        break
                movie_file= movie_file_list[1]

            th_count = movie_file
            globals()["th_"+str(th_count)] = play_video()
            globals()["th_"+str(th_count)].set_video_file_name(movie_file)
            globals()["th_"+str(th_count)].start()
            th_list.append("th_"+str(th_count))

        elif params[0] == "msg":
            txt_h = 780
            pygame.draw.rect(screen, (0,0,0), (0,txt_h,1300,GAME_SIZE[1]-txt_h))
            text = params[2].replace("<outline width=2 color=black>","").replace("</outline>","")
            text = text.replace("<size=31>","").replace("</size>","")
            text_lines = text.split('\\n')
            for t in text_lines:
                textRect = (10, txt_h, 1280, 50)
                pygame.draw.rect(screen, (0,0,0), textRect)
                text = text_font.render(t, True, WHITE, (0, 0, 0))
                screen.blit(text, textRect)
                txt_h = txt_h + 50

        elif params[0] == "clickwait":
            count = count+1
            break

        else:
            pass
        count = count+1
    return count

#翻译相关
#md5
def generate_sign(appid, q, salt, secret_key):
    sign_str = appid + q + salt + secret_key
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign

#翻译请求
def translate_word(q):
    base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    from_lang = 'jp'
    to_lang = translate_to_language
    salt = '1435660288'


    appid = translate_appid
    secret_key = translate_secret_key

    sign = generate_sign(appid, q, salt, secret_key)
    # 请求参数
    params = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(base_url, params=params)
    translation = response.json()['trans_result'][0]['dst']
    return translation

def get_translate_status():
    if use_translate:
        try:
            if translate_word("幻夢境") == "幻梦境":
                print("翻译可用")
                return True
            else:
                print("翻译不可用")
                return False
        except:
            print("翻译不可用")
            return False
    else:
        return use_translate
    
        

# 常量

WHITE = (255, 255, 255)
RED = (255, 0, 0)

CG_SIZE = (1280, 720)
TEXT_SIZE = (1000, 200)

display_width = user_setting['窗口宽度']
display_height = user_setting['窗口高度']
GAME_SIZE = (display_width, display_height)

下载线程数 = user_setting['下载线程数']
use_translate = True if user_setting['翻译api']['use_translate'] == 'yes' else False
translate_appid = user_setting['翻译api']['appid']
translate_secret_key = user_setting['翻译api']['secret_key']
translate_to_language = user_setting['翻译api']['to_language']
bot_check = True if user_setting['是否喜欢furau'] == 'yes' else False

# 初始化
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("DeepOne")

screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
game_font = pygame.font.Font('msgothic.ttc', 50)


# rect
load_butto_rect = (400, 650, 100, 50)
play_button_rect = (800, 650, 100, 50)
message_rect = (450, 100, 400, 50)
pages_up_rect = (800, 550, 150, 50)
page_down_rect = (400, 550, 150, 50)
loading_text_rect = (450, 850, 400, 50)

# button
load_button = Button(load_butto_rect, 'LOAD')
play_button = Button(play_button_rect, 'PLAY')
pages_up_button = Button(pages_up_rect, "下一頁")
pages_down_button = Button(page_down_rect, "上一頁")


# ————————参数——————

# ————————控制参数————

# 寝室id
jsonId = ''
# 播放状态
is_play = False
is_main = True
json_selected = False
play_count= 0
th_list=[]
th_count = ""
commands = []

#翻译状态
translate_status = get_translate_status()
if translate_status:
    text_font = pygame.font.Font('SIMFANG.TTF', 30)
else:
    text_font = pygame.font.Font('msgothic.ttc', 30)
# 初始页码
json_list_page = 0

# 数据

# --寝室列表
rename_json_list()
# 返回jsonId列表
json_list = get_list()
load_preview(json_list)

# 寝室数量
pages_size = math.ceil(len(json_list)/9)
video_control = False


while bot_check:

    for event in pygame.event.get():

        if is_main:

            new_list = page_list(json_list_page, json_list)
            # jsonId赋值给了json_button（寝室预览按钮）的text属性
            json_button_list = load_list(new_list)

            pages_up_button.show_button()
            pages_down_button.show_button()

            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                for bt in json_button_list:
                    if bt.in_rect(x, y):
                        jsonId = bt.text
                        json_selected = True

                if pages_up_button.in_rect(x, y):
                    json_list_page = json_list_page + 1
                    if json_list_page+1 > pages_size:
                        json_list_page = 0
                    new_list = page_list(json_list_page, json_list)
                    json_button_list = load_list(new_list)
                    screen.fill((0, 0, 0))

                if pages_down_button.in_rect(x, y):
                    json_list_page = json_list_page - 1
                    if json_list_page < 0:
                        json_list_page = pages_size-1
                    new_list = page_list(json_list_page, json_list)
                    json_button_list = load_list(new_list)
                    screen.fill((0, 0, 0))

        if json_selected:
            load_button.show_button()
            play_button.show_button()

            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                if load_button.in_rect(x, y):
                    get_resource(jsonId)
                if play_button.in_rect(x, y):
                    try:
                        commands = read_adv(jsonId)
                        is_play = True
                        json_selected = False
                        is_main = False
                        screen.fill((0, 0, 0))
                    except:
                        print("先点load下载资源")

        if is_play:
            
            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]

                play_count = read_command(commands,play_count)
                if play_count == len(commands):
                    print("播放结束")
                    play_count = 0
                    is_play = False
                    is_main = True
                    json_selected = False
                    screen.fill((0,0,0))

        if event.type == QUIT:
            exit()
        
    pygame.display.flip()

print("不喜欢就爬！")

while True:
    print("————————开始植入芙拉病毒————————")
    print("————————神绊导师！启动！————————")
    webbrowser.open('https://pc-play.games.dmm.co.jp/play/cravesagax/')
    time.sleep(10)