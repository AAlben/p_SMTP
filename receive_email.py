import poplib
import base64
from email import parser

sender = '345657803@qq.com'
_pass = 'lzeszgpxyxtpbihi'
pop_conn = poplib.POP3_SSL('pop.qq.com', port=995)
pop_conn.user(sender)
pop_conn.pass_(_pass)
ret = pop_conn.stat()

today_indexes = []

index_list = list(range(1, ret[0] + 1))[::-1]
break_flag = False
for index, i in enumerate(index_list):
    if break_flag:
        break
    top_msg = pop_conn.top(i, 0)
    msgs = top_msg[1]
    print(index)
    for msg in msgs:
        try:
            _msg = msg.decode()
        except UnicodeDecodeError as e:
            continue
        except Exception as e:
            raise
        if 'From: ' in _msg:
            if 'li345657803@qq.com' in _msg:
                pass
            else:
                break
        if 'Date:' in _msg:
            if '27 Nov' in _msg:
                today_indexes.append(index)
            else:
                break_flag = True
                break

for index in today_indexes:
    content = ''
    content_flag = False
    index = len(index_list) - index
    down = pop_conn.retr(index)
    for index, line in enumerate(down[1]):
        if 'Subject' in line.decode():
            content_flag = True
            lines = line.decode().split('Subject: =?utf-8?b?')
            print(lines)
            if not lines:
                continue
        if content_flag:
            content += line.decode()
    content = base64.b64decode(content).decode()
    if 'OVER scheduler' in content:
        pass
    elif 'REST scheduler' in content:
        pass
    elif 'FAIL scheduler' in content:
        pass
    print(content)
    break
raise Exception('', '')
