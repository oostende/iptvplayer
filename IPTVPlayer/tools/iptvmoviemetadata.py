# -*- coding: utf-8 -*-
#
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, byteify, RemoveDisallowedFilenameChars, GetMovieMetaDataDir

###################################################

###################################################
# FOREIGN import
###################################################
import codecs
try:    import json
except: import simplejson as json
from copy import deepcopy
###################################################
#{
#"host":"",
#"title":"",
#"file_path":"",
#
#"tracks":
#    {
#        "audio":-1,
#        "video":-1,
#        "subtitles":
#        {
#            "idx":-1,
\
#            "tracks":[
#                {"title":"", "id":"126", "provider":"opensubtiles.org", "lang":"pl", "delay_ms":0, "path":"/ole/sub_pl.srt"},
#                {"title":"", "id":"123", "provider":"opensubtiles.org", "lang":"en", "delay_ms":0, "path":"/ole/sub_en.srt"},
#            ]
#        }
#    },
#"aspect_ratio":-1,
#"video_options":{"aspect":"4:3", "policy":None, "policy2":None}
#"last_position":0
#}

def localPrintDBG(txt):
    #printDBG(txt)
    pass

class IPTVMovieMetaDataHandler():
    META_DATA      = {"host":"", "title":"", "file_path":"", "aspect_ratio":-1, "last_position":-1,"tracks":{"audio":-1, "video":-1, "subtitles":{"idx":-1, "tracks":[]} } }
    SUBTITLE_TRACK = {"title":"", "id":"", "provider":"", "lang":"", "delay_ms":0, "path":""}
    EXTENSION = 'iptv'
    ENCODING  = 'utf-8'
    
    def __init__(self, host="", title="", filePath=""):
        printDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>... [%s]\n" % self.META_DATA)
        localPrintDBG("IPTVMovieMetaDataHandler.__init__ host[%s], title[%s], filePath[%s]" % (host, title, filePath))
        if "" != host:
            fileName = "{0}_{1}.{2}".format(host, title, self.EXTENSION)
        else:
            fileName = filePath.split('/')[-1]+'.' + self.EXTENSION
        
        self.filePath = GetMovieMetaDataDir( RemoveDisallowedFilenameChars( fileName ) )
        self.data = deepcopy( self.META_DATA )
        self.data.update( {"host":host, "title":title, "file_path":filePath} )
        self.isModified = False
        
    def load(self):
        localPrintDBG("IPTVMovieMetaDataHandler.load")
        sts = False
        try:
            try:
                with codecs.open(self.filePath, 'r', self.ENCODING, 'replace') as fp:
                    data = byteify( json.loads(fp.read()) )
                if data != {}:
                    sts = True
                    self.data.update(data)
            except:
                printExc()
        except:
            printExc()
        return sts
    
    def save(self, force=False):
        localPrintDBG("IPTVMovieMetaDataHandler.save force[%s]" % force)
        sts = False
        if not force:
            force = self.isModified
        if force:
        
            try:
                with codecs.open(self.filePath, 'w', self.ENCODING) as fp:
                    fp.write(json.dumps(self.data))
                sts = True
            except: 
                printExc()
        return sts
    
    ##################################################
    # SUBTITLES
    ##################################################
    def getSubtitlesTracks(self):
        localPrintDBG("IPTVMovieMetaDataHandler.getSubtitlesTracks")
        tracks = []
        try:
            for item in self.data['tracks']['subtitles']['tracks']:
                track = deepcopy( self.SUBTITLE_TRACK )
                track.update(item)
                tracks.append(track)
        except:
            printExc()
        return tracks

    def getSubtitleTrack(self):
        localPrintDBG("IPTVMovieMetaDataHandler.getSubtitleTrack")
        track = None
        try:
            if self.getSubtitleIdx() > -1:
                track = self.getSubtitlesTracks()[self.getSubtitleIdx()]
        except:
            printExc()
        return track
        
    def setSubtitleTrackDelay(self, delay_ms):
        localPrintDBG("IPTVMovieMetaDataHandler.setSubtitleTrackDelay")
        sts = False
        try:
            if self.getSubtitleIdx() > -1:
                self.data['tracks']['subtitles']['tracks'][self.getSubtitleIdx()]['delay_ms'] = delay_ms
            sts = True
        except:
            printExc()
        if sts: self.isModified = True
        return sts
        
    def getSubtitleTrackDelay(self):
        delay_ms = 0
        try:
            delay_ms = self.data['tracks']['subtitles']['tracks'][self.getSubtitleIdx()]['delay_ms']
        except:
            printExc()
        return delay_ms
        
    def getSubtitleIdx(self):
        localPrintDBG("IPTVMovieMetaDataHandler.getSubtitleIdx")
        idx = -1
        try:
            idx = self.data['tracks']['subtitles']['idx']
            if idx >= len( self.getSubtitlesTracks() ):
                idx = -1
        except:
            printExc()
        return idx
        
    def setSubtitleIdx(self, idx):
        localPrintDBG("IPTVMovieMetaDataHandler.setSubtitleIdx idx[%s]" % idx)
        sts = False
        try:
            if idx < len( self.getSubtitlesTracks() ):
                self.data['tracks']['subtitles']['idx'] = idx
                sts = True
        except:
            printExc()
        if sts: self.isModified = True
        return sts
        
    def addSubtitleTrack(self, subtitlesTrack):
        localPrintDBG("IPTVMovieMetaDataHandler.addSubtitleTrack")
        idx = -1
        try:
            track = deepcopy( self.SUBTITLE_TRACK )
            track.update(subtitlesTrack)
            localPrintDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> track[%s]" % track)
            self.data['tracks']['subtitles']['tracks'].append(track)
            idx = len(self.data['tracks']['subtitles']['tracks']) - 1
        except:
            printExc()
        if idx > -1: self.isModified = True
        return idx
        
    def removeSubtitleTrack(self, idx):
        localPrintDBG("IPTVMovieMetaDataHandler.removeSubtitleTrack")
        sts = False
        currIdx = self.getSubtitleIdx()
        try:
            del self.data['tracks']['subtitles']['tracks'][idx]
            if currIdx == idx:
                self.setSubtitleIdx(-1)
        except:
            printExc()
        if sts: self.isModified = True
        return sts
        
    ##################################################
    # SUBTITLES
    ##################################################
    def getVideoOption(self, option):
        localPrintDBG("IPTVMovieMetaDataHandler.getVideoOption")
        ret = None
        try:
            return self.data['video_options'][option]
        except:
            printExc()
        return ret
        
    def setVideoOption(self, option, value):
        localPrintDBG("IPTVMovieMetaDataHandler.getVideoOption")
        sts = False
        try:
            if 'video_options' not in self.data:
                self.data['video_options'] = {}
            self.data['video_options'][option] = value
            sts = True
        except:
            printExc()
        if sts: self.isModified = True
        return sts
        
    ##################################################
    # LAST POSITION
    ##################################################
    def getLastPosition(self):
        localPrintDBG("IPTVMovieMetaDataHandler.getLastPosition")
        lastPosition = -1
        try:
            lastPosition = self.data['last_position']
        except:
            printExc()
        return lastPosition
        
    def setLastPosition(self, lastPosition):
        localPrintDBG("IPTVMovieMetaDataHandler.setLastPosition")
        sts = False
        try:
            self.data['last_position'] = lastPosition
            sts = True
        except:
            printExc()
        if sts: self.isModified = True
        return sts
        
            