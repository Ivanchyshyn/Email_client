"""
This is implemented interface for Email client.
"""

from tkinter import StringVar, Text, Tk, Toplevel, ttk
from tkinter import N, W, E, S, GROOVE
from functools import partial
from base64 import b64decode
from Crypto.Cipher import AES
from recieve_mail_imap import MailRecieve
from scroll import scroll_bar

class EmailClient:
    """ Starting program and creating login window """
    def __init__(self):
        self.messages = self.text = self.ciphertext = ''
        self.root = Tk()
        self.root.title("Mail user agent")
        mainframe = ttk.Frame(self.root, padding="10 10 40 40")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.login, self.password = StringVar(), StringVar()
        ttk.Label(mainframe, text="Введіть логін:").grid(column=1, row=1, sticky=(N, W, S))
        login_entry = ttk.Entry(mainframe, width=35, textvariable=self.login)
        login_entry.grid(column=2, row=1, sticky=(N, W, S, E))

        ttk.Label(mainframe, text="Введіть пароль:").grid(column=1, row=2, sticky=(N, W, S))
        pass_entry = ttk.Entry(mainframe, width=35, textvariable=self.password, show='*')
        pass_entry.grid(column=2, row=2, sticky=(N, W, S, E))

        ttk.Button(mainframe, text="Ввійти", command=self._is_auth).grid(column=3, row=3, sticky=W)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        login_entry.focus()
        self.root.bind('<Return>', self._is_auth)
        self.root.mainloop()

    def _is_auth(self, *event):
        """ Checking authentication of given login/password """
        try:
            self.messages = MailRecieve.read_mail(self.login.get(), self.password.get())
            self.root.title(self.login.get())
            self.mailbox()
        except Exception as ex:
            popup = Toplevel(self.root)
            popup.geometry('150x100+320+180')
            ttk.Label(popup, text="Ви ввели невірні дані").grid(column=0, row=0, sticky=(N, W, S, E))
            btn = ttk.Button(popup, text="Окей", command=popup.destroy)
            btn.grid(column=0, row=1, sticky=(W, E))
            btn.focus()

            self.root.unbind('<Return>')
            popup.bind('<Return>', lambda e: btn.invoke())
        finally:
            self.root.bind('<Return>', self._is_auth)
            del event

    def mailbox(self):
        """ User mailbox with 20 messages per page """
        self.root.unbind('<Return>')
        mainframe = ttk.Frame(self.root, relief=GROOVE, width=800, height=600, padding='5 5 5 5')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.grid_columnconfigure(0, weight=1)
        mainframe.grid_rowconfigure(0, weight=1)

        frame = scroll_bar(mainframe)

        i = 0
        for letter in self.messages:
            From, Subject = (letter['from'], letter['subject'])

            From = From[From.find('<')+1:From.find('>')]
            Subject = Subject[:Subject.find('\n')]
            ttk.Button(frame, text=From, command=partial(self.message, i), width=40).grid(column=0, row=i, sticky=W)
            ttk.Button(frame, text=Subject[10:81], command=partial(self.message, i), width=70).grid(column=1, row=i, sticky=W)
            i += 1

        ttk.Button(mainframe, text='Надіслати', command=self.send_mail).grid(sticky=(S, E))

    def message(self, msg_id):
        """ Reading message """
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        From, To, Date, Subject, self.ciphertext = (self.messages[msg_id]['from'],
                                                    self.messages[msg_id]['to'],
                                                    self.messages[msg_id]['date'],
                                                    self.messages[msg_id]['subject'],
                                                    self.messages[msg_id]['msg'])

        self.text = Text(mainframe, width=80, height=25)
        self.text.grid(column=0, row=1, sticky=W)
        self.text.insert('1.0', From+'\n')
        self.text.insert('end', To+'\n')
        self.text.insert('end', Date+'\n')
        self.text.insert('end', Subject+'\n')
        self.text.insert('end', self.ciphertext)
        self.text['state'] = 'disabled'
        ttk.Button(mainframe, text='Вернутись', command=self.mailbox).grid(column=0, row=0, sticky=(N, W))
        ttk.Button(mainframe, text='Розшифрувати', command=self.decrypt_message).grid(column=1, row=0, sticky=(N, E))

    def decrypt_message(self):
        """ Window to enter a key to decrypt ciphertext """
        popup = Toplevel(self.root)
        popup.geometry('250x200-320+180')

        key = StringVar()
        ttk.Label(popup, text="Введіть ключ (16 символів)").grid(column=0, row=0)
        key_entry = ttk.Entry(popup, width=20, textvariable=key, show='*')
        key_entry.grid(column=0, row=1)
        key_entry.focus()

        btn = ttk.Button(popup, text="Окей", command=lambda: [popup.destroy(), _decrypt()])
        btn.grid(column=0, row=2)
        def _decrypt():
            b64 = self.ciphertext.split()
            jv = [b64decode(b64[k]) for k in range(3)]

            cipher = AES.new(key.get().encode(), AES.MODE_EAX, nonce=jv[0])
            plaintext = cipher.decrypt_and_verify(jv[1], jv[2])
            self.text['state'] = 'normal'
            self.text.delete('6.0', 'end')
            self.text.insert('end', '\n')
            self.text.insert('end', plaintext.decode('utf-8'))
            self.text['state'] = 'disabled'

    def send_mail(self, *event):
        """ Send mail using smtp """
        try:
            from send_mail_smtp import MailSender
            MailSender(self)
        except Exception as ex:
            print('Unsuccessful')
            print(ex)
        finally:
            del event

EmailClient()
