#!/usr/bin/env python
import settings
import tornado.httpserver
import tornado.ioloop
import tornado.web

import re,os,subprocess

def Setup():
    pass

def UpdateYDL():

    print "Checking for youtube-dl updates"
    args = [settings.YOUTUBE_DL, "-U"]
    subprocess.call(args)

def DownloadPL(playlist):
    if len(settings.FFMPEG) > 0:
        args = [settings.YOUTUBE_DL, "--no-post-overwrites", "-x", "--ffmpeg-location", settings.FFMPEG, "--prefer-ffmpeg", "--audio-format", "mp3", "--audio-quality", "0", "https://www.youtube.com/playlist?list="+playlist, "-o", "Music/Playlist/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"]
    else:
        args = [settings.YOUTUBE_DL, "--no-post-overwrites", "-x", "--prefer-ffmpeg", "--audio-format", "mp3", "--audio-quality", "0", "https://www.youtube.com/playlist?list="+playlist, "-o", "Music/Playlist/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"]
    subprocess.call(args)

def DownloadVD(video):
    if len(settings.FFMPEG) > 0:
        args = [settings.YOUTUBE_DL, "--no-post-overwrites", "-x", "--ffmpeg-location", settings.FFMPEG, "--prefer-ffmpeg", "--audio-format", "mp3", "--audio-quality", "0", "-o", "Music/%(title)s.%(ext)s", video]
    else:
        args = [settings.YOUTUBE_DL, "--no-post-overwrites", "-x", "--prefer-ffmpeg", "--audio-format", "mp3", "--audio-quality", "0", "-o", "Music/%(title)s.%(ext)s", video]
    subprocess.call(args)

class DownloadPlaylist(tornado.web.RequestHandler):

    def get(self,playlist_id):
        playlist = playlist_id if playlist_id else ''
        if len(playlist) > 1 and re.match(VIDEO_REGEX,playlist):
            DownloadPL(playlist)
            self.write("Playlist Download Completed")
        else:
            self.write("Invalid Request")

class DownloadFile(tornado.web.RequestHandler):

    def get(self,video_id):
        video = video_id if video_id else ''
        if len(video) > 1 and re.match(VIDEO_REGEX,video):
            DownloadVD(video)
            self.write("MP3 Download Complete")
        else:
            self.write("Invalid Request")



if __name__ == "__main__":
    VIDEO_REGEX = "^([a-zA-Z0-9\_\-]+)$"
    tornado.web.Application([
        (r"/playlist/(?P<playlist_id>[^\/]+)", DownloadPlaylist),
        (r"/video/(?P<video_id>[^\/]+)",DownloadFile),
        ]).listen(8080)
    #test update with a lower time period
    tornado.ioloop.PeriodicCallback(UpdateYDL, 300000).start() #15 mins in milliseconds
    tornado.ioloop.IOLoop.instance().start()

    '''
    http://localhost:8080/playlist/PLX3EwmWe0cS9URO4KPot3LcL4tgoGZaQt
    http://localhost:8080/video/f4kqIruQcvQ
    '''