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
            if '345657803@qq.com' in _msg:
                from_flag = True
            else:
                break
        if 'Date:' in _msg:
            if '27 Nov' in _msg:
                date_flag = True
            else:
                break_flag = True
                break
    if subject_flag and from_flag and date_flag:
        today_indexes.append(index)

print('-' * 100)
print(today_indexes)
print('-' * 100)

for index in today_indexes:
    content = ''
    content_flag = False
    index = len(index_list) - index
    down = pop_conn.retr(index)
    start_content = 'Content-Transfer-Encoding: base64'
    for index, line in enumerate(down[1]):
        print(line)
        if start_content in line.decode():
            content_flag = True
            continue
        elif '_NextPart_' in line.decode():
            content_flag = False
            continue
        if content_flag:
            content += line.decode()
    content = base64.b64decode(content).decode('gbk')
    if 'OVER scheduler' in content:
        pass
    elif 'REST scheduler' in content:
        pass
    elif 'FAIL scheduler' in content:
        pass
    print(content)
raise Exception('', '')
