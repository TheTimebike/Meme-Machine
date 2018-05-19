
import smtplib, poplib, email.utils
from time import sleep
import email.mime.text, email.mime.image, email.mime.multipart, email.mime.application
import praw
import os, glob, random

emailA = input('Please Enter the Email Address ')
emailPass = input('Please Enter the Email Password ')

#Functions
def sendMeme(receiver):
    memeLength = len(glob.glob('./*.jpg'))
    x = random.randint(1, memeLength - 1)
    memePath = './Meme%s.jpg' % x

    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = 'Here is your meme!'
    msg['From'] = 'Meme Machine'

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(emailA, emailPass)  

    f = open(memePath, 'rb')
    img = email.mime.image.MIMEImage(f.read(), _subtype="jpeg") 

    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(memePath))
    msg.attach(img)
    server.sendmail(emailA, receiver, msg.as_string())
    server.quit()

def everything():
    M = poplib.POP3_SSL('pop.gmail.com',995)
    M.user(emailA)
    M.pass_(emailPass)
    numMessages = len(M.list()[1])
    if (numMessages == 0):
        print("No Messages found, Exiting", flush=True)
        sleep(2)
        M.quit()
        return
    else:
        for i in range(numMessages):
            rawEmail = b"\n".join(M.retr(i+1)[1])
            for j in range(numMessages):
                receivedMsg = email.message_from_bytes(rawEmail)
                senderOfEmail = receivedMsg['From']
                newSender = str(str(senderOfEmail.split(" ")[len(senderOfEmail.split(" ")) - 1]).split("<")[1].split(">")[0])
                print("Email found, processing", flush=True)
                print(newSender)
                sleep(2)
                if (receivedMsg['Subject'] == "Meme Machine"):
                    sendMeme(receiver=newSender)
                    M.quit()
                else:
                    M.quit()
                    
while True:
    everything()
