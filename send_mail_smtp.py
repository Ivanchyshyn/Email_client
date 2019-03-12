from smtplib import SMTP_SSL as smtp
from tkinter import *
from tkinter import ttk
import json
from base64 import b64encode
from Crypto.Cipher import AES

class MailSender:
    def __init__(self, client):
        self.client = client
        self.root = self.client.root
        self.message = ''
        self.login = self.client.login.get()
        self.password = self.client.password.get()
        self.receiver = StringVar()
        self.subject = StringVar()

        mainframe = ttk.Frame(self.root, width=100, height=100)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Button(mainframe, text='Вернутись', command=self.client.mailbox).grid(column=0, row=0, sticky=(N,W))
        ttk.Button(mainframe, text='Надіслати', command=self.send).grid(column=1, row=0, sticky=(N,E))

        ttk.Label(mainframe, text="To:").grid(column=0, row=1, sticky=(N,W))
        ttk.Label(mainframe, text="Subject:").grid(column=0, row=2, sticky=(N,W))

        To_entry = ttk.Entry(mainframe, width=95, textvariable=self.receiver)
        Subject_entry = ttk.Entry(mainframe, width=95, textvariable=self.subject)

        To_entry.grid(column=0, row=1, sticky=(N,S,E))
        Subject_entry.grid(column=0, row=2, sticky=(N,S,E))

        self.text = Text(mainframe, width=80, height=25)
        self.text.grid(column=0, row=3, sticky=W)

        self.root.mainloop()
    def send(self):
        if not self.receiver.get():
            MailSender(self.client)
        else:
            try:
                popup = Toplevel(self.root)
                popup.geometry('250x160-200+150')

                key = StringVar()
                ttk.Label(popup, text="Введіть ключ (16 байт)").grid(column=0, row=0)
                key_entry = ttk.Entry(popup, width=20, textvariable=key)
                key_entry.grid(column=0, row=1)
                key_entry.focus()

                b = ttk.Button(popup, text="Okay", command=lambda:[popup.destroy(),send_cipher()])
                b.grid(column=0, row=2)
                def send_cipher():
                    cipher = AES.new(key.get().encode('utf-8'), AES.MODE_EAX)
                    ciphertext, tag = cipher.encrypt_and_digest(self.text.get('1.0', 'end').encode('utf-8'))
                    result = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, ciphertext, tag) ]
                    self.message += "From: <{login}>\nTo: <{receiver}>\nSubject: {subject}\n{text}".format(
                        login=self.login, receiver=self.receiver.get(), subject=self.subject.get(), text=' '.join(result)
                    )
                    mail = smtp('smtp.gmail.com', 465)
                    mail.login(self.login, self.password)
                    mail.sendmail(self.login, [self.receiver.get()], self.message)
                    print("Successfully sent email")
            except Exception as e:
                print("Error: unable to send email")
                print(e)
