import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '345657803@qq.com'
receivers = ['345657803@qq.com']
PASS = 'lzeszgpxyxtpbihi'


def send(content=None, _receivers=None):
    if not content:
        content = '''
        Please Start Your Scheduler!!!
        book & write & try
        sport & studing
        video & friend
        english & exercise
        clear & NO NO NO fire
        '''
    if not _receivers:
        receivers.extend(_receivers)
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(["Scheduler Self", sender])
    message['To'] = formataddr(["My Self", sender])
    subject = 'Day Scheduler'
    message['Subject'] = subject

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, PASS)
    server.sendmail(sender, receivers, message.as_string())
    server.quit()
    print("邮件发送成功")
