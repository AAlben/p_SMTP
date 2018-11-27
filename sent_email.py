import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '345657803@qq.com'
receivers = ['345657803@qq.com']

content = '''
Please Start Your Scheduler!!!
book & write
sport & studing
video & friend
english & exercise
clear
'''

message = MIMEText(content, 'plain', 'utf-8')
message['From'] = formataddr(["Scheduler Self", sender])
message['To'] = formataddr(["My Self", sender])
subject = 'Day Scheduler'
message['Subject'] = subject

server = smtplib.SMTP_SSL("smtp.qq.com", 465)
server.login(sender, 'lzeszgpxyxtpbihi')
server.sendmail(sender, receivers, message.as_string())
server.quit()
print("邮件发送成功")

