# encoding: utf-8

import sys
import time
import ConfigParser
import Skype4Py
from GoogleApiWrapper import GoogleApiWrapper

gaw = None

class Output:
    def __init__(self):
        self.buffer = ""
    def write(self, arg):
        self.buffer += arg
    def isEmpty(self):
        return self.buffer == ""

def skype_handler(msg, event):
    global gaw
    if event == u"RECEIVED":
        if msg.Body == u"プロ":
            msg.Chat.SendMessage(u"趣味")
        elif msg.Body[0:2] == u":g":
            cm = msg.Chat.SendMessage("requesting...")
            out1 = Output()
            out2 = Output()
            try:
                arg = msg.Body[3:]
                sys.stdout = out1
                sys.stderr = out2
                gaw.ArgParse(arg);
            except SystemExit:
                # skip argparser exit error
                raise
            except:
                msg.Chat.SendMessage(u"error:%s" % sys.exc_info()[0])
                raise
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                cm.Body += "\n"
                if not out1.isEmpty():
                    cm.Body += out1.buffer;
                if not out2.isEmpty():
                    cm.Body += out2.buffer;
 
def main(): 
    global gaw

    print u"start"

    print u"init google api..."
    config = ConfigParser.SafeConfigParser()
    config.read("config.proc")
    gaw = GoogleApiWrapper(config)

    print u"setup skype..."
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = skype_handler
    skype.Attach()
   
    print u"running"
    while True:
        time.sleep(1)
 
if __name__ == '__main__':
    main()
