import smtplib
import requests
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '345657803@qq.com'
receivers = ['345657803@qq.com']
PASS = 'lzeszgpxyxtpbihi'


def server_chan(title, content):
    url = 'https://sc.ftqq.com/SCU38425T5d31de7e4df59fb4659595571aa736765c271faa316e9.send'
    data = {'text': title, 'desp': content}
    r = requests.post(url, data=data)
    print(r.status_code)
    pass


'''
content version1 = 

        Please Start Your Scheduler!!!
        book & write & try
        sport & studing
        video & friend
        english & exercise
        clear & NO NO NO fire

'''


def send(content=None, _receivers=None):
    if not content:
        content = '''
            数学思维：统计 + 概率
            数学：线性代数
            项目：天池 + kaggle
            面试宝典：面试题 + leetcode
            深度 + 广度：为难自己 + 新知识
        '''
    if _receivers:
        _receivers.extend(receivers)
    else:
        _receivers = receivers
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(["Scheduler Self", sender])
    message['To'] = formataddr(["My Self", sender])
    subject = 'Day Scheduler'
    message['Subject'] = subject

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, PASS)
    server.sendmail(sender, _receivers, message.as_string())
    server.quit()

    server_chan(subject, content)
    print("邮件发送成功")
