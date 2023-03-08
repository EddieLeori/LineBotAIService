from lib.utility import *
from LineBotService.app import LineBotService
import json
import requests

class LineBotAIService:
    def __init__(self):
        self.name = 'LineBotAIService'
        self.bot_server = None
        self.is_init = False
        self.ai_talk_url = "http://127.0.0.1:5124/talk"
        self.ai_img_url = "http://127.0.0.1:5124/img"
        self.notify_url = "http://127.0.0.1:5125"
        self.psw = ""
        
        self.init()

    def init(self):
        try:
            with open('option.json', 'r') as f:
                cfg = json.load(f)
                f.close()
                Log(cfg)
                if self.name not in cfg:
                    return
                if "ai_talk_url" in cfg[self.name]:
                    self.ai_talk_url = cfg[self.name]["ai_talk_url"]
                if "ai_img_url" in cfg[self.name]:
                    self.ai_img_url = cfg[self.name]["ai_img_url"]
                if "notify_url" in cfg[self.name]:
                    self.notify_url = cfg[self.name]["notify_url"]
                if "psw" in cfg[self.name]:
                    self.psw = cfg[self.name]["psw"]

                self.bot_server = LineBotService()
                self.bot_server.call_fun_message = self.message

                # init ok here
                self.is_init = True
                Log("{0} init ok.".format(self.name))
        except:
            Log(self.name + " init eror!")
            return False
        return True
    
    def run(self):
        if self.is_init == True:
            # test
            # self.notifyMsg("notifyImgs", "['https://oaidalleapiprodscus.blob.core.windows.net/private/org-mQ5dyCKqAT0huoRX2gDTDeXI/user-JHdaW4SP2a1ouYv066JaWFcK/img-YKNv6U2vuBBFUm2lMiUe2Euq.png?st=2023-03-08T01%3A03%3A35Z&se=2023-03-08T03%3A03%3A35Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-03-07T21%3A42%3A27Z&ske=2023-03-08T21%3A42%3A27Z&sks=b&skv=2021-08-06&sig=em84%2BPArDfGXHgy%2BcVn%2Bav3fJGvN/UIdccldcFK2F0k%3D']")
            # self.message("123", "img tree")
            # self.notifyMsg("notifyAll", "hi.")
            # self.message("123", "hello!")
            self.bot_server.run()

    def message(self, token, msg):
        try:
            if msg is None:
                return False
            Log('message={0}'.format(msg))
            data = {
                "question": msg
            }
            url = self.ai_talk_url
            type = "notifyAll"
            if self.ai_img_url != "" \
                and len(msg) > 4:
                pretext = msg[0:4]
                if ('img' in pretext or \
                    'IMG' in pretext or \
                    'Img' in pretext or \
                    '圖片' in pretext):
                    url = self.ai_img_url
                    type = "notifyImgs"
            # ai msg 
            response = requests.post(url, data = json.dumps(data))
            Log("response={0}".format(response))
            if response.status_code != 200:
                return False
            # notify client
            self.notifyMsg(type, response.text)
            return True
        
        except Exception as e:
            Log("message error:{0}".format(e))
            return False
        
    def notifyMsg(self, type, msg):
        try:
            if msg is None:
                return False
            # send to notify server
            d = {
                "psw": self.psw,
                "key": type,
                "value": msg
            }
            r = requests.post(self.notify_url, data = json.dumps(d))
            if r.status_code != 200:
                Log(r)
                return False
            return True
        except Exception as e:
            Log("{0} error:{1}".format(type, e))
            return False

        
