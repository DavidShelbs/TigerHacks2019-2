#importing the module
from pytube import YouTube
import moviepy.editor as mp
import pytube
import os
from os import path

#where to save

#link of the video to be downloaded
def download(videoID):
    link="https://www.youtube.com/watch?v=" + videoID
    SAVE_PATH = "C:\\Users\\David\\Documents\\Git\\TigerHacks2019\\static\\music" #to_do

    if not path.exists("static/music/"+videoID+".mp4"):
    # try:
            #object creation using YouTube which was imported in the beginning
        yt = pytube.YouTube(link)
        stream = yt.streams.first()
        vid_path = stream.download(SAVE_PATH)
        os.rename(vid_path, "static/music/"+videoID+".mp4")
        return videoID
    # except:
    #     pass
    return videoID

def get_music_clip(videoID, start, end):
    download(videoID)
    if path.exists("static/music/"+videoID+".mp3"):
        os.remove("static/music/"+videoID+".mp3")
    clip = mp.VideoFileClip("static/music/"+videoID+".mp4").subclip(start,end)
    clip.audio.write_audiofile("static/music/"+videoID+".mp3")
