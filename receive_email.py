import re
import json
import poplib
import base64
import requests

from email import parser
from datetime import datetime

from sent_email import send

SENDER = '345657803@qq.com'
PASS = 'lzeszgpxyxtpbihi'


def take_score(now_hour):
    if now_hour == 0:
        with open('SCORE.txt', 'w') as fp:
            fp.write('0')
        return 0
    else:
        with open('SCORE.txt', 'r') as fp:
            score = fp.read()
            return int(score)


def set_score(score):
    with open('SCORE.txt', 'w') as fp:
        fp.write(str(score))


def take_index(pop_conn):
    msg_indexes = []
    ret = pop_conn.stat()
    index_list = list(range(1, ret[0] + 1))[::-1]
    break_flag = False
    _date = datetime.now().strftime('%d %b')
    now_hour = datetime.now().hour
    score = take_score(now_hour)
    for index, i in enumerate(index_list):
        if break_flag:
            break
        top_msg = pop_conn.top(i, 0)
        msgs = top_msg[1]
        print(index)
        subject_flag, from_flag, date_flag = False, False, False
        for msg in msgs:
            try:
                _msg = msg.decode()
            except UnicodeDecodeError as e:
                continue
            except Exception as e:
                raise
            if 'Subject:' in _msg:
                if 'Re: Day Scheduler' in _msg:
                    subject_flag = True
                else:
                    break
            if 'From: ' in _msg:
                if SENDER in _msg:
                    from_flag = True
                else:
                    break
            if 'Date:' in _msg:
                if _date in _msg:
                    _time = re.findall(r'(\d{2}:\d{2}:\d{2})', _msg)[0]
                    _hour = int(_time.split(':')[0])
                    if now_hour - _hour <= 1:
                        date_flag = True
                else:
                    break
        if subject_flag and from_flag and date_flag:
            break_flag = True
            msg_indexes.append(len(index_list) - index)
    return msg_indexes, score


def parse_email(index, sum_score, pop_conn):
    content = ''
    score = 0
    content_flag = False
    down = pop_conn.retr(index)
    start_content = 'Content-Transfer-Encoding: base64'
    for index, line in enumerate(down[1]):
        if start_content in line.decode():
            content_flag = True
            continue
        elif '_NextPart_' in line.decode():
            content_flag = False
            continue
        if content_flag:
            content += line.decode()
    content = base64.b64decode(content).decode('gbk')
    content_list = content.split('\n')
    robot_message = take_robot(content_list[1])

    if 'OVER scheduler' in content:
        score = 10
    elif 'REST scheduler' in content:
        score = 5
    elif 'FAIL scheduler' in content:
        score = 0

    robot_message += 'SCORE = {0}\r\n'.format(score)
    robot_message += 'TODAY SUM SCORE = {0}'.format(sum_score)
    send(robot_message)
    set_score(score)
    # print(robot_message)


def take_robot(content):
    result = ''
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": content
            }
        },
        "userInfo": {
            "apiKey": "b903c4228a2247bc934c8d92e510c26c",
            "userId": "Alben"
        }
    }
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    r = requests.post(url, json=data)
    message = json.loads(r.text)
    for item in message['results']:
        result += item['values']['text'] + '\r\n'
    return result


def receive():
    pop_conn = poplib.POP3_SSL('pop.qq.com', port=995)
    pop_conn.user(SENDER)
    pop_conn.pass_(PASS)

    msg_indexes, score = take_index(pop_conn)

    print('-' * 100)
    print(msg_indexes)
    print('-' * 100)

    for index in msg_indexes:
        parse_email(index, score, pop_conn)


if __name__ == '__main__':
    receive()
