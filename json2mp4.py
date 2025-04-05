import json
from pydub import AudioSegment
import ffmpeg



def read_adv(jsonId,use_translate = False):
    with open("./json/"+jsonId+'.json', 'r') as f:
        dojson = json.load(f)
        resources= dojson["resource"]
        for resource in resources:
            if "text" in resource["fileName"]:
                fileName = resource["fileName"]
                break

    if use_translate:
        txt_path = "./resource/"+jsonId+"/"+fileName.replace(".txt","_CN.txt")
    else:
        txt_path = "./resource/"+jsonId+"/"+fileName
    commands =[]
    with open(txt_path, "r", encoding='utf8') as f:
        commands= f.readlines()
    return commands

def export_video(jsonId,use_translate = False):
    commands = read_adv(jsonId,use_translate)

    full_audio = AudioSegment.silent(duration=0)
    prev_audio_length = 0

    movie_info = []
    movie_length = 0
    recording_bg_path = "color_0_0_0.png"
    
    srt_info = []

    full_length = 0

    for command in commands:
        command = command.strip()
        params = command.split(",")
        command_name = params[0]
        if command_name == "bg":
            if params[1] != "color_0_0_0":
                bg_path = "./resource/"+jsonId+"/"+params[1]
            else:
                bg_path = "color_0_0_0.png"

            if recording_bg_path != bg_path:
                movie_info.append({
                    "recording_bg_path": recording_bg_path,
                    "movie_length": movie_length
                })
                recording_bg_path = bg_path
                movie_length = 0
        if command_name == "bgoff":
            movie_info.append({
                "recording_bg_path": recording_bg_path,
                "movie_length": movie_length
            })

        if command_name == "playvoice":
            voice_path = "./resource/"+jsonId+"/"+params[2].strip()
            voice_length,audio = get_voice_length(voice_path)
            movie_length += voice_length
            prev_audio_length = voice_length
            full_audio += audio

        if command_name == "msg":
            msg = params[2].replace("<outline width=2 color=black>","").replace("</outline>","").replace("<size=31>","").replace("</size>","")
            if params[1] == "0":
                msg_length,audio = get_msg_length(msg)
                movie_length += msg_length
                full_audio += audio
                prev_audio_length = msg_length
            srt_info.append(
                {
                    "msg": msg,
                    "start_time": full_length,
                    "end_time": full_length + prev_audio_length
                }
            )
            
            full_length += prev_audio_length
        
    full_audio.export(f"./resource/{jsonId}/{jsonId}.mp3", format="mp3")
    get_movie(movie_info, jsonId)
    get_srt(jsonId,srt_info)

def get_msg_length(msg):
    msg_length = round(len(msg)/15, 2)
    audio = AudioSegment.silent(duration=msg_length * 1000)
    return msg_length,audio

def get_voice_length(path):
    audio = AudioSegment.from_file(path)  # 支持多种格式
    duration_seconds = len(audio) / 1000  # 毫秒转秒
    return duration_seconds,audio

def get_movie(movie_info, jsonId):
    # 用来保存生成视频流的输入参数列表
    inputs = []

    # 遍历 movie_info 列表，生成每个视频流并拼接
    for index, movie in enumerate(movie_info):
        bg_path = movie["recording_bg_path"]
        length = movie["movie_length"]
        
        # 使用 ffmpeg 创建视频流
        video_stream = ffmpeg.input(bg_path, loop=1, framerate=5, t=length).filter("setsar", "1")
        inputs.append(video_stream)

    audio_file = f'./resource/{jsonId}/{jsonId}.mp3'
    audio_stream = ffmpeg.input(audio_file)

    # 使用 ffmpeg 拼接视频流
    output_file = f'./resource/{jsonId}/{jsonId}.mp4'
    concat_video = ffmpeg.concat(*inputs, v=1, a=0)  # 拼接视频流
    output = ffmpeg.output(concat_video, audio_stream, output_file, acodec='aac')  # 移除 vcodec='copy'
    ffmpeg.run(output)

def get_srt(jsonId,srt_info):
    srt_text = ""
    for index,srt in enumerate(srt_info):
        srt_text += f"{index+1}\n"
        start_time = srt['start_time']
        end_time = srt['end_time']
        msg = srt['msg']

        # 将秒转换为SRT时间码格式
        def seconds_to_srt_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            # 保留3位毫秒
            millisecs = int((secs - int(secs)) * 1000)
            return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millisecs:03d}"

        # 转换为SRT时间码
        start_srt = seconds_to_srt_time(start_time)
        end_srt = seconds_to_srt_time(end_time)

        # 构建SRT格式字符串
        srt_format = f"{start_srt} --> {end_srt}\n"
        srt_text += srt_format
        srt_text += msg.replace('\\n', '\n') + "\n\n"
    
    with open(f"./resource/{jsonId}/{jsonId}.srt", "w", encoding="utf-8") as f:
        f.write(srt_text)

        
