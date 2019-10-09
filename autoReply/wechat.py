import itchat
import requests
import json

def getResponse(_info):
    api_url = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": _info
            },
        },
        "userInfo": {
            "apiKey": "fad2cd7cfc334d7e8d128946d891cd45",
            "userId": "66666"
        }
    }
    data = json.dumps(data).encode('utf8')
    response = requests.post(url=api_url, data=data, headers={'Content-Type': 'application/json'})
    rdict = response.json()
    return rdict["results"][0]["values"]["text"]

@itchat.msg_register(itchat.content.TEXT)
def autoReply(msg):
    if msg['User']['NickName']!="嘻嘻嘻":
        return
    else:
        content = getResponse(msg['Content'])
        itchat.send(content, toUserName=msg['FromUserName'])
if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()










