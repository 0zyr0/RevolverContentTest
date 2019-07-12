import time
import requests
import json
from lxml import html
from websocket import create_connection


# req = requests.request('GET', 'http://192.168.100.43:8080')

# для таймаута
#eventlet.monkey_patch()

start_time = time.time()

ws = create_connection("ws://192.168.100.43:23245/")

for revolver in range(3600):

    with requests.Session() as s:
        # GET-запрос, альтернативный вариант obj = s.get('http://192.168.100.32:8080')
        obj = s.request('GET', 'http://192.168.100.43:8080', timeout=10)

        content = obj.content
        tree = html.fromstring(content)
        body = tree.xpath('//script[@id="return-param"]')  # все head теги

        content_s = body[0].text

        # начало строки returnParam
        start = content_s.find('screen', 0, len(content_s))

        # конец строки returnParam
        finish = str(body[0].text).find(';', 0, len(content_s))

        # получаем строку с данными
        end_content = content_s[start:finish]

        # работа с Websocket
        result = ws.recv()
        print("Received '%s'" % result)
        data = json.loads(result)
        print("Data '%s'" % data['type'])

        # if (data[type] == "READY_TO_SWITCH"):


        # вывод результата Get запроса
        print(end_content, "\n")

ws.close()
print("stop requests")
print("Time: %s minutes" % ((time.time() - start_time) / 60))





