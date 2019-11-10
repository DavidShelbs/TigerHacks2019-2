from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import matplotlib.pyplot as plt

# DEVELOPER_KEY = "AIzaSyDW8VQHj6hgGhdPQwy-hlzU7JGPMCTfPzk"
# DEVELOPER_KEY = "AIzaSyDbf46h5-R0a-ctrGwFhQmQqPz9aMajmPE"
# DEVELOPER_KEY = "AIzaSyDwbNsN6aJPNTYHOlBpZMIDxczjwaZ-iKw"
DEVELOPER_KEY = "AIzaSyBHG5RzKAevAI2bkGY5D1FIrtrp_QWHh9s"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def search(query, max_results=1, order="relevance", token=None, location=None, location_radius=None):
    search_response = youtube.search().list(
    q=query,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    videoCaption='closedCaption',
    location=location,
    locationRadius=location_radius).execute()

    #Assign first page of results (items) to item variable
    items = search_response['items'] #50 "items"
    #Assign 1st results to title, channelId, datePublished then print
    title = items[0]['snippet']['title']
    channelId = items[0]['snippet']['channelId']
    datePublished = items[0]['snippet']['publishedAt']

    return search_response
