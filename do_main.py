import sys,pygame
import os
import json
import math
from urllib.request import urlretrieve
from pygame.locals import*
from random import randrange
from sys import exit
import cv2
import _thread
import threading

os.makedirs("./meta/", exist_ok=True)
os.makedirs("./resource/", exist_ok=True)

class Button:
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
        button_text = game_font.render(self.text, True, self.text_color, (0, 0, 0))
        li_rect = (self.rect[0]-1,self.rect[1]-1,self.rect[2]+2,self.rect[3]+2)
        pygame.draw.rect(screen, self.button_color, li_rect, 0)
        screen.blit(button_text, self.rect)


    def in_rect(self, x, y):
        inx = (x>self.rect[0]) and (x<(self.rect[0]+self.rect[2]))
        iny = (y>self.rect[1]) and (y<(self.rect[1]+self.rect[3]))
        return inx and iny




#加载资源
def get_resource(storyIds):
    image_resource_fold = './resource/'+storyIds+'/image/'
    voice_resource_fold = './resource/'+storyIds+'/voice/'
    text_resource_fold = './resource/'+storyIds+'/text/'
    os.makedirs(image_resource_fold, exist_ok=True)
    os.makedirs(voice_resource_fold, exist_ok=True)
    os.makedirs(text_resource_fold, exist_ok=True)

    json_path="./json/" 

    with open(json_path+storyIds+'.json','r') as load_f:     
        dojson = json.load(load_f)
        json_len = len(dojson['resource'])
        print(json_len)
        i = 1
        adult = dojson['adult']
        for r in dojson['resource']:  

            fileName = ""
            fileName = r['fileName']

            loading_text ='loading :' + str(i) + '/' +str(json_len)

            print(loading_text)

            loading_text_button = Button(loading_text_rect,'ojbk')
            loading_text_button.show_button()

            if (fileName[-1]=="g"):
                path = r['path']
                md5 = r['md5']
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/"+path+"/"+md5+".jpg"
                name_list = fileName.split('/')
                length = len(name_list)
                name = name_list[length-1]
          
                urlretrieve(url, image_resource_fold + name)
                print(name)
            if (fileName[-1]=="3"):
                path = r['path']
                md5 = r['md5']
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/"+path+"/"+md5+".mp3"
                name_list = fileName.split('/')
                length = len(name_list)
                name = name_list[length-1]

                urlretrieve(url, voice_resource_fold + name)
                print(name)

            if (fileName[-1]=="4"):
                path = r['path']
                md5 = r['md5']
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/"+path+"/"+md5+".mp4"
                name_list = fileName.split('/')
                length = len(name_list)
                name = name_list[length-1]

                urlretrieve(url, image_resource_fold + name)
                print(name)

            if(adult==3):
                if (fileName[-1]=="t"):
                    path = r['path']
                    md5 = r['md5']
                    url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/"+path+"/"+md5+".txt"
                    name_list = fileName.split('/')
                    length = len(name_list)
                    name = name_list[length-1]
                    name = name.replace('06.txt','05.txt')
                    urlretrieve(url, text_resource_fold +name)
                    print(name)

            if (fileName[-1] == "t"):
                path = r['path']
                md5 = r['md5']
                url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_adv/" + path + "/" + md5 + ".txt"
                name_list = fileName.split('/')
                length = len(name_list)
                name = name_list[length - 1]
                urlretrieve(url, text_resource_fold + name)
                print(name)
            i= i+1
    print("完毕")

#创建meta
def load_meta(storyIds):

    file = open('./resource/'+storyIds+'/text/'+storyIds+'.txt',"r",encoding='utf8')

    meta_file = open('./meta/'+storyIds+"_meta.json","w",encoding='utf8')

    text_data = file.read()
    text = text_data.split("\n\n")

    meta='{"resource":['
    msg = 'null'
    playvoice = 'null'
    bg = 'null'
    new_resoucer = ''
    new_msg=''
    for t in text:
        lines = t.split('\n')
        for i in lines:
            if 'msg' in i:
                msg = i.split(',')[-2].replace('</outline>','').replace('<outline width=2 color=black>','')  
        for i in lines:
            if 'playvoice' in i:
                playvoice  = i.split(',')[-1]
        for i in lines:
            if 'bg,' in i:
                bg  = i.split(',')[1]
        for i in lines:
            if 'movie,' in i:
                bg  = i.split(',')[1]

        if new_msg != msg:
            new_resoucer='{"msg" : "'+msg+'","playvoice" : "'+playvoice.split('/')[-1]+'","bg" :"' + bg.split('/')[-1] +'"},\n'
            new_msg =msg
            meta = meta+ new_resoucer

    meta = meta + ']}'
    meta = meta.replace('},\n]}','}]}')

    meta_file.write(meta)

    file.close()
    meta_file.close()
    return meta

#读取meta
def open_meta(storyIds):
    f = open("./meta/"+storyIds+"_meta.json",'r',encoding='utf8')
    content = f.read()
    meta = json.loads(content)
    length = len(meta["resource"])
    return [meta,length]

#载入cg
def load_cg(storyIds,image_name):
    cg_url= "./resource/"+storyIds+"/image/"+image_name
    print(cg_url)
    return  pygame.image.load(cg_url).convert_alpha()

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
    i=0
    while (i<6) and (p*6+i <list_len):
        new_list.append(page_list[p*6+i])
        i= i+1
    return new_list

#显示列表
def load_list(json_list):

    li_h = 200
    for li in json_list :
        li_rect =(525,li_h,250,50)
        li_text = li
        li_button = Button(li_rect,li_text)
        li_button.show_button()
        li_h = li_h + 50

class play_video(threading.Thread):
    run_count = False
    loop_count = True


    def __init__(self, storyIds,index):
        threading.Thread.__init__(self)
        self.storyIds = storyIds
        self.index = index

    def set_run_count(self,count):
        self.run_count=count

    def set_loop_count(self,count):
        self.loop_count=count

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
                    video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                    video_surf = pygame.transform.scale(video_surf, CG_SIZE)

                else:
                    if self.loop_count:
                        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    else:
                        self.run_count=True
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


#常量
display_width = 1300
display_height = 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)    
GAME_SIZE = (display_width,display_height)
CG_SIZE = (1280,720)
TEXT_SIZE = (1000,200)


#初始化
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("DeepOne")

screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
game_font = pygame.font.Font('msgothic.ttc',50)
text_font = pygame.font.Font('msgothic.ttc',30)

#rect
next_button_rect =(1190,900,100,50)
load_butto_rect = (425,650,100,50)
play_button_rect = (825,650,100,50)
message_rect = (450,100,400,50)
prev_rect = (425,550,100,50)
next_rect =(825,550,100,50)
loading_text_rect =(450,850,400,50)

#button
text_next_button = Button(next_button_rect,"next" )
load_button = Button(load_butto_rect,'LOAD')
play_button = Button(play_button_rect,'PLAY')
prev_button = Button(prev_rect,'prev')
next_button = Button(next_rect,'next')

#————————参数——————

# 初始页码
page=0
# 寝室列表
json_list = get_list()
# 列表长度
list_len = len(json_list)
print(list_len)

# 分页大小
page_size = 6
# 页数
pages = int(math.ceil(list_len / page_size))
# 当页列表
new_list = page_list(page,json_list)


load_list(new_list)

# ————————控制参数————

# 寝室id
storyIds = ''
# 播放状态 -1：主页
play_count =-1
prev_page = False
next_page = True
video_control = False


while True:
 
    for event in pygame.event.get():

        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            # print('pages:',pages)
            # print('page:', page)
            #
            # print("prev_page:", prev_page)
            # print("next_page:", next_page)


            x = event.pos[0]
            y = event.pos[1]

            # print('x:',x)
            # print("y:",y)
            # print(next_button.rect[1])
            # print(next_button.in_rect(x, y))
            list_num = len(new_list)

            if (page == 0) and (play_count == -1):
                next_button.show_button()
                next_page = True
                prev_page = False
            elif (page == pages-1) and (play_count == -1):
                prev_button.show_button()
                next_page = False
                prev_page = True
            elif (play_count == -1):
                next_button.show_button()
                prev_button.show_button()
                next_page = True
                prev_page = True

            #向上翻页
            if prev_button.in_rect(x,y) and prev_page:
                page= page -1
                screen.fill((0, 0, 0))
                new_list = page_list(page, json_list)
                print(new_list)
                load_list(new_list)
                if page>0:
                    prev_button.show_button()

            if next_button.in_rect(x,y) and next_page :

                page= page +1
                screen.fill((0, 0, 0))
                new_list = page_list(page, json_list)
                print(new_list)
                load_list(new_list)
                if page<pages :
                    next_button.show_button()
            
            
            if (x>525 and x<775) and (y>200 and y<200+list_num*50) and (play_count == -1):
                print(list_num)
                list_count = (int)((y-200)/50)
                storyIds = new_list[list_count]

                message ='選中：'+ storyIds


                message_button =Button(message_rect,message)

                load_button.show_button()
                play_button.show_button()

                message_button.show_button()

            if  (storyIds != '') and (play_count == -1) :
                if load_button.in_rect(x,y):
                    print("LODA"+storyIds)
                    get_resource(storyIds)
                elif play_button.in_rect(x,y):
                    print("PLAY"+storyIds)
                    load_meta(storyIds)
                    play_count = 0
                    screen.fill((0, 0, 0))
                    text_next_button.show_button()




            if   text_next_button.in_rect(x,y) and (play_count != -1 ):
                length = open_meta(storyIds)[1]
                meta = open_meta(storyIds)[0]

                if play_count<length:
                    screen.fill((0, 0, 0))
                    text_next_button.show_button()
                    print(play_count)

                    image_name = meta["resource"][play_count]["bg"]
                    text = meta["resource"][play_count]["msg"]
                    voice = meta["resource"][play_count]["playvoice"]

                    if play_count == length-1 and meta["resource"][play_count]["bg"][-1]=='4':
                        th1.set_run_count(True)

                    if image_name=='color_0_0_0.jpg':
                        if meta["resource"][play_count-1]["bg"][-1] == '4' and play_count!=0:
                            th1.set_run_count(True)
                        cg = pygame.image.load('color_0_0_0.jpg').convert_alpha()
                        screen.blit(cg, (10, 0))
                    else:
                        if image_name[-1] == '4' and meta["resource"][play_count - 1]["bg"]=='color_0_0_0':
                            print(image_name)
                            th1 = play_video(storyIds, image_name)
                            th1.set_loop_count(False)
                            th1.start()
                        if image_name[-1]=='4' and image_name!= meta["resource"][play_count-1]["bg"] and meta["resource"][play_count - 1]["bg"]!='color_0_0_0':
                            th1.set_run_count(True)
                            print("runcount:",th1.run_count)
                            th1 = play_video(storyIds, image_name)
                            th1.start()
                        # if int(image_name[-5]) - int(meta["resource"][play_count-1]["bg"][-5]) == 2 :
                        #     image_index =str(int(image_name[-5])-1)
                        #     image_name = image_name[:8]+image_index+image_name[9:]
                        #     th1.set_run_count(True)
                        #
                        #     th1 = play_video(storyIds, image_name)
                        #     th1.set_loop_count(False)
                        #
                        #     th1.start()
                        #     th1.join()
                        #
                        #     th1.set_run_count(True)
                        #
                        #     image_name = meta["resource"][play_count]["bg"]
                        #     th1 = play_video(storyIds, image_name)
                        #     th1.start()
                        if image_name[-1]=='g':
                            cg = load_cg(storyIds,image_name)
                            cg = pygame.transform.scale(cg, CG_SIZE)
                            screen.blit(cg, (10,0))

                    txt_h = 730
                    if (text != '' ) and ( text != 'endwmsg'):
                        text_lines = meta["resource"][play_count]["msg"].split('\n')
                        for t in text_lines:
                            textRect =(10,txt_h,1280,50)
                            text = text_font.render(t,True,WHITE,(0,0,0))
                            screen.blit(text,textRect)
                            txt_h = txt_h+ 50

                    if play_count>1 :
                        if (voice!='null') and (voice != meta["resource"][play_count-1]["playvoice"]):
                            print('./resource/'+storyIds+'/voice/'+voice)
                            pygame.mixer.music.load('./resource/'+storyIds+'/voice/'+voice)
                            pygame.mixer.music.play()


                    play_count = play_count+1
                else:
                    screen.fill((0, 0, 0))
                    play_count = -1
                    storyIds = ''
                    load_list(new_list)
    pygame.display.flip() 