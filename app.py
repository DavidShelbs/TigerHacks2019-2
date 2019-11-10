from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import sqlite3
import youtube_api
import wget
import parse_lang
from contextlib import contextmanager
import img_download
import sys
from os import path
import parse_srt
import database
import download_yt
from os import path, walk
import random

lines_words = {}
videoID = ""

app = Flask(__name__)

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

@app.route('/')
def home():
    session['CURR_LINE_NUM'] = 0
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    global lines_words
    global videoID
    # global session['CURR_LINE_NUM']
    #find videoID from youtube
    # try:
    urls = list()
    session['SEARCH'] = request.form.get('search')
    search_response = youtube_api.search(query=session['SEARCH'])
    for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videoID = search_result['id']['videoId']
    #get .srt file
    if not path.exists("srt/"+videoID+".srt"):
        url = 'http://www.nitrxgen.net/youtube_cc/' + videoID + '.csv'
        wget.download(url, out="csv/"+videoID+".csv", bar=None)
        eng_index = parse_lang.parse_lang("csv/"+videoID + ".csv")
        url = 'http://www.nitrxgen.net/youtube_cc/' + videoID + '/' + eng_index + '.srt'
        filename = wget.download(url, out="srt/"+videoID+".srt", bar=None)

    session['vid_data'] = parse_srt.parse_srt("srt/"+videoID+".srt")
    words = img_download.parse_data(session['vid_data'])
    # for i in words:
    #     img_download.downloadimages(i)

    lines_words = img_download.parse_lines_words(session['vid_data'])
    curr_list = lines_words[session['CURR_LINE_NUM']]
    conn = database.create_connection("database.db")
    for i in range(len(curr_list)):
        rows = database.select_img(conn, curr_list[i])
        if rows != None:
            urls.append(rows[0])

    dynamic_image = open('templates/images.html', 'w+')
    if len(urls) <= 4:
        width = 100/5
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    elif len(urls) <= 8:
        width = 100/len(urls)
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    else:
        width = 100/8
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
        html += '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8, len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''


    dynamic_image.write(html)
    dynamic_image.close()
    start = session['vid_data'][session['CURR_LINE_NUM']][0][0]
    end = session['vid_data'][session['CURR_LINE_NUM']][0][1]
    print(session['vid_data'][session['CURR_LINE_NUM']])
    download_yt.get_music_clip(videoID, start, end)

    dynamic_vid = open('templates/video.html', 'w+')
    html = '''<audio hidden id="hint" src="static/music/''' + videoID + '''.mp3" type="audio/mpeg" controls>
    Your browser does not support the audio element.
    </audio>
    <button class="btn btn-info" onClick="togglePlay()">Hint</button>'''
    dynamic_vid.write(html)
    dynamic_vid.close()

    data = {'videoID': videoID}
    return render_template('normal.html', data=data)
    # except:
    #     return render_template('index.html')

@app.route('/next', methods=['GET', 'POST'])
def next():
    global videoID
    # global session['CURR_LINE_NUM']
    urls = list()
    session['CURR_LINE_NUM'] += 1
    curr_list = lines_words[session['CURR_LINE_NUM']]
    conn = database.create_connection("database.db")
    for i in range(len(curr_list)):
        rows = database.select_img(conn, curr_list[i].strip(",.!?"))
        if rows != None:
            urls.append(rows[0])

    dynamic_image = open('templates/images.html', 'w+')
    if len(urls) <= 4:
        width = 100/5
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    elif len(urls) <= 8:
        width = 100/len(urls)
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    else:
        width = 100/8
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
        html += '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8, len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''

    dynamic_image.write(html)
    dynamic_image.close()

    # print(session['vid_data'])
    # start = session['vid_data'][str(session['CURR_LINE_NUM'])][0][0]
    # end = session['vid_data'][str(session['CURR_LINE_NUM'])][0][1]
    # print(session['vid_data'][str(session['CURR_LINE_NUM'])])
    # download_yt.get_music_clip(videoID, start, end)
    #
    # dynamic_vid = open('templates/video.html', 'w+')
    # html = '''<audio hidden id="hint" src="static/music/''' + videoID + '''.mp3" type="audio/mpeg" controls>
    # Your browser does not support the audio element.
    # </audio>
    # <button class="btn btn-info" onClick="togglePlay()">Hint</button>'''
    # dynamic_vid.write(html)
    # dynamic_vid.close()
    #
    # data = {'videoID': videoID}

    return render_template('normal.html')

# @app.route('/back', methods=['GET', 'POST'])
# def back():
#     global videoID
#     # global session['CURR_LINE_NUM']
#     urls = list()
#     session['CURR_LINE_NUM'] -= 1
#     curr_list = lines_words[session['CURR_LINE_NUM']]
#     conn = database.create_connection("database.db")
#     for i in range(len(curr_list)):
#         rows = database.select_img(conn, curr_list[i])
#         if rows != None:
#             urls.append(rows[0])
#
#     dynamic_image = open('templates/images.html', 'w+')
#     if len(urls) <= 4:
#         width = 100/5
#         html = '''<div class="row justify-content-center" style="margin:20px;">'''
#         for i in range(len(urls)):
#             html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
#         html += '''</div>'''
#     elif len(urls) <= 8:
#         width = 100/len(urls)
#         html = '''<div class="row justify-content-center" style="margin:20px;">'''
#         for i in range(len(urls)):
#             html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
#         html += '''</div>'''
#     else:
#         width = 100/8
#         html = '''<div class="row justify-content-center" style="margin:20px;">'''
#         for i in range(8):
#             html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
#         html += '''</div>'''
#         html += '''<div class="row justify-content-center" style="margin:20px;">'''
#         for i in range(8, len(urls)):
#             html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
#         html += '''</div>'''
#
#     dynamic_image.write(html)
#     dynamic_image.close()
#     print(session['vid_data'])
#     start = session['vid_data'][str(session['CURR_LINE_NUM'])][0][0]
#     end = session['vid_data'][str(session['CURR_LINE_NUM'])][0][1]
#     print(session['vid_data'][str(session['CURR_LINE_NUM'])])
#     download_yt.get_music_clip(videoID, start, end)
#
#     dynamic_vid = open('templates/video.html', 'w+')
#     html = '''<audio hidden id="hint" src="static/music/''' + videoID + '''.mp3" type="audio/mpeg" controls>
#     Your browser does not support the audio element.
#     </audio>
#     <button class="btn btn-info" onClick="togglePlay()">Hint</button>'''
#     dynamic_vid.write(html)
#     dynamic_vid.close()
#
#     data = {'videoID': videoID}
#     return render_template('normal.html', data=data)

@app.route('/normal', methods=['GET', 'POST'])
def normal():
    global videoID
    global lines_words
    session['CURR_LINE_NUM'] += 0
    videoIDs = ['E1ZVSFfCk9g', 'CnAmeh0-E-U', 'SlPhMPnQ58k']
    videoID = random.choice(videoIDs)

    if not path.exists("srt/"+videoID+".srt"):
        url = 'http://www.nitrxgen.net/youtube_cc/' + videoID + '.csv'
        wget.download(url, out="csv/"+videoID+".csv", bar=None)
        eng_index = parse_lang.parse_lang("csv/"+videoID + ".csv")
        url = 'http://www.nitrxgen.net/youtube_cc/' + videoID + '/' + eng_index + '.srt'
        filename = wget.download(url, out="srt/"+videoID+".srt", bar=None)

    session['vid_data'] = parse_srt.parse_srt("srt/"+videoID+".srt")
    words = img_download.parse_data(session['vid_data'])
    for i in words:
        img_download.downloadimages(i)

    urls = list()
    lines_words = img_download.parse_lines_words(session['vid_data'])
    curr_list = lines_words[session['CURR_LINE_NUM']]
    conn = database.create_connection("database.db")
    for i in range(len(curr_list)):
        rows = database.select_img(conn, curr_list[i].strip(",.!?"))
        if rows != None:
            urls.append(rows[0])


    dynamic_image = open('templates/images.html', 'w+')
    if len(urls) <= 4:
        width = 100/5
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    elif len(urls) <= 8:
        width = 100/len(urls)
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
    else:
        width = 100/8
        html = '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''
        html += '''<div class="row justify-content-center" style="margin:20px;">'''
        for i in range(8, len(urls)):
            html += '''<div class=dynamic_image style="width: ''' + str(width) + '''%"><img src="''' + urls[i] + '''" class="dynamic_image"><br><input type="text" class=dynamic_image></div>'''
        html += '''</div>'''

    dynamic_image.write(html)
    dynamic_image.close()

    return render_template('normal.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    # app.run(debug=True, host='192.168.0.22', port=80)
    app.run(debug=True,host='0.0.0.0', port=80)
