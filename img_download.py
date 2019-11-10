# creating object
from google_images_download import google_images_download
import parse_srt
from os import path
import os
import glob
import database
import sqlite3

response = google_images_download.googleimagesdownload()

def downloadimages(query):
    db = "database.db"
    # create a database connection
    conn = database.create_connection(db)
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")
    arguments = {"keywords" : query,
    "limit" : 1,
    "output_directory" : "img",
    # "thumbnail_only" : True,
    "no_directory" : True,
    "no_download" : True,
    "silent_mode" : True,
    "prefix" : query+"_"}

    try:
        url = response.download(arguments)
        with conn:
            # create a new project
            img = (query, url[0][query][0]);
            img_id = database.create_img(conn, img)
            print(url[0][query][0])

        # if not glob.glob("img/"+query+".*"):
        #     print(query)
        #     try:
        #         url[0][query][0].replace("\\\\", "\\")
        #         os.rename(url[0][query][0], "img/"+query+"."+str(url[0][query][0][-3:]))
        #     except:
        #         print("Skipped: " + query)

    # Handling File NotFound Error
    except:
        arguments = {"keywords" : query,
        "limit" : 1,
        "output_directory" : "img",
        # "thumbnail_only" : True,
        "no_directory" : True,
        "no_download" : True,
        "silent_mode" : True,
        "prefix" : query+"_"}

        # Providing arguments for the searched query
        try:
            # Downloading the photos based
            # on the given arguments
            url = response.download(arguments)
            with conn:
                # create a new project
                img = (query, url[0][query][0]);
                img_id = database.create_img(conn, img)
                print(url[0][query][0])
        except:
            print("error fatal")

def parse_data(data):
    db = "database.db"
    # create a database connection
    conn = database.create_connection(db)
    out = list()
    for i in range(len(data)):
        line = data[i][1]
        words = line.split()
        for word in words:
            # word = word.strip(",.!?;:")
            if database.select_img(conn, word) == None and word not in out:
                out.append(word)
    return out

def parse_lines_words(data):
    db = "database.db"
    # create a database connection
    out = {}
    wordlist = list()
    conn = database.create_connection(db)
    for i in range(len(data)):
        line = data[i][1]
        words = line.split()
        # for word in words:
        #     wordlist.append(word.strip(",.!?;:/\\"))
        out[i] = words
    return out
