from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from upload_form.models import FileNameModel
import sys, os
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'

def form(request):
    if request.method != 'POST':
        return render(request, 'upload_form/form.html')

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    insert_data = FileNameModel(file_name = file.name)
    insert_data.save()

    #メール送信はここから
    import datetime
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    host, port = 'smtp.gmail.com', 465#587 でうまくいかなかったら
    username, password = 'yagokoro8556', 'vocaloid'# gmailのアカウント名, パスワード

    from_addr = "from_address@gmail.com"# gmailで設定必要
    to_addr = "to_address@gmail.com"# 送り先
    subject = "ファイル添付"# メールタイトル
    body = "test body"# メール本文
    mine={'type':'text','subtype':'comma-separated-values'}

    name = os.path.dirname(os.path.abspath(__name__))
    #joined_path = os.path.join(name, 'upload_form\\files\\fire.jpg')

    #アップロードされた最新のファイル一つのパスを得る

    joined_path = os.path.join(name, '.\\upload_form\\files\\')
    files = [f for f in os.listdir(joined_path)]
    FILES = [joined_path + i for i in files]
    FILES.sort(key=os.path.getmtime)
    files_sorted = []
    for i in FILES:
        l = i.split('\\')
        files_sorted.append(l[-1])
    sotai = 'upload_form\\files\\'+str(files_sorted[-1])
    joined_path = os.path.join(name, sotai)
    #ここまで
    data_path = os.path.normpath(joined_path)

    attach_file={'name':'test.jpg','path':data_path}# nameは添付ファイルの名前

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    # メール本文
    body = MIMEText(body)
    msg.attach(body)

    # 添付ファイルの設定
    attachment = MIMEBase('image', 'jpg')

    with open(attach_file['path'], 'rb') as f:
        attachment.set_payload(f.read())

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
    msg.attach(attachment)

    smtp = smtplib.SMTP_SSL(host, port)
    smtp.ehlo()
    smtp.login(username, password)
    smtp.mail(username)
    smtp.rcpt(to_addr)
    smtp.data(msg.as_string())
    smtp.quit()

    #ここまで

    return redirect('upload_form:complete')

def complete(request):
    return render(request, 'upload_form/complete.html')
