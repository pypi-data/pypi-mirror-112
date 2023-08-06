#   Gary Davenport, CLI player functions 6/8/2021
#
#   plays wav files using native wav playing command line interface calls
#   for Windows 10, Linux, and MacOS
#
#   Windows10 uses the Media.Soundplayer module built into Windows 10
#   Linux uses ALSA which is part of the Linux kernel since version 2.6 and later
#   MacOS uses the afplay module which is present OS X 10.5 and later
#   

from platform import system
import subprocess
from subprocess import Popen, PIPE
import os
from threading import Thread
from time import sleep
import sndhdr

class MusicLooper:
    def __init__(self, fileName):
        self.fileName = fileName
        self.playing = False
        self.songProcess = None

    def _playwave(self):
        self.songProcess=playwave(self.fileName)

    def _playloop(self):
        while self.playing==True:
            self.songProcess=playwave(self.fileName)
            sleep(self._getWavDurationFromFile())

    def startMusicLoopWave(self):
        if self.playing==True:
            print("Already playing, stop before starting new.")
            return
        else:
            self.playing=True
            t = Thread(target=self._playloop)
            t.setDaemon(True)
            t.start()
            
    def stopMusicLoop(self):
        if self.playing==False:
            print(str(self.songProcess)+" already stopped, play before trying to stop.")
            return
        else:
            self.playing=False
            stopwave(self.songProcess)

    def _getWavDurationFromFile(self):
        frames = sndhdr.what(self.fileName)[3]
        rate = sndhdr.what(self.fileName)[1]
        duration = float(frames)/rate
        return duration

    def getSongProcess(self):
        return(self.songProcess)

    def getPlaying(self):
        return(self.playing)


def playwave(fileName, block=False):
    fileName=fileName
    if system()=="Linux": command = "exec aplay --quiet " + os.path.abspath(fileName)
    elif system()=="Windows": command="%SystemRoot%\system32\WindowsPowerShell/v1.0\powershell.exe -c (New-Object Media.SoundPlayer '"+os.path.abspath(fileName)+"').PlaySync()"
    elif system()=="Darwin": command = "exec afplay \'" + os.path.abspath(fileName)+"\'"
    else: print(str(system()+" unknown to wavecliplayer"));return None
    if block==True: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE).communicate()
    else: P = subprocess.Popen(command, universal_newlines=True, shell=True,stdout=PIPE, stderr=PIPE)
    return P

def stopwave(process):
    if process is not None:
        try:
            if process is not None:
                if system()=="Windows": 
                    os.system("taskkill /F /T /PID "+ str(process.pid) + " >NUL")          
                else: process.terminate()
        except:
            pass
            #print("process is not playing")
    else:
        pass
        #print("process ", str(process), " not playing")

def getIsPlaying(process):
    isSongPlaying=False
    if process is not None:
        try: return(process.poll() is None)
        except: pass
    return isSongPlaying

def playsound(fileName, block=True):
    return(playwave(fileName, block))

def loopwave(fileName):
    looper=MusicLooper(fileName)
    looper.startMusicLoopWave()
    return(looper)

def stoploop(looperObject):
    if looperObject is not None:
        looperObject.stopMusicLoop()
    else:
        pass
        #print("looperObject ", str(looperObject), " not playing")

def getIsLoopPlaying(looperObject):
    if looperObject is not None:
        return(looperObject.getPlaying())
    else:
        return False

stopsound=stopwave