from tkinter import *
from tkinter import ttk
from send_mail_smtp import Mail_Sender
from recieve_mail_imap import Mail_Recieve
from functools import partial

class Email_client:
    # Запуск програми та створення Вікна входу
    def __init__(self):
        self.messages = ''
        self.root = Tk()
        self.root.title("Mail user agent")
        mainframe = ttk.Frame(self.root, padding="10 10 40 40")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.login, self.password = StringVar(), StringVar()
        ttk.Label(mainframe, text="Введіть логін:").grid(column=1, row=1, sticky=(N,W,S))
        login_entry = ttk.Entry(mainframe, width=30, textvariable=self.login)
        login_entry.grid(column=2, row=1, sticky=(N,W,S,E))

        ttk.Label(mainframe, text="Введіть пароль:").grid(column=1, row=2, sticky=(N,W,S))
        pass_entry = ttk.Entry(mainframe, width=30, textvariable=self.password, show='*')
        pass_entry.grid(column=2, row=2, sticky=(N,W,S,E))

        ttk.Button(mainframe, text="Sign in", command=self.is_auth).grid(column=3, row=3, sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        login_entry.focus()
        self.root.bind('<Return>', self.is_auth)
        self.root.mainloop()

    def is_auth(self, event):
        try:
            self.messages = Mail_Recieve.read_mail(self.login.get(), self.password.get())
            self.root.title(self.login.get())
            self.mailbox()
        except Exception as e:
            print('Unsuccessful')
            print(e)

    def mailbox(self):
        self.root.unbind('<Return>')
        mainframe=ttk.Frame(self.root,relief=GROOVE,width=800,height=600, padding='5 5 5 5')
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        v = ttk.Scrollbar(mainframe, orient=VERTICAL)
        canvas = Canvas(mainframe, scrollregion=(0, 0, 1000, 1200), yscrollcommand=v.set)
        v['command'] = canvas.yview

        frame = Frame(canvas)
        frame_id = canvas.create_window((0,0),window=frame,anchor='nw')
        ttk.Sizegrip(mainframe).grid(column=2, row=1, sticky=(S,E))

        canvas.grid(column=0, row=0, sticky=(N,W,E,S))
        v.grid(column=2, row=0, sticky=(N,S))
        mainframe.grid_columnconfigure(0, weight=1)
        mainframe.grid_rowconfigure(0, weight=1)

        i = 0
        for letter in self.messages:
            From, To, Subject, msg = letter[0], letter[1], letter[2], letter[3]
            From = From[From.find('<')+1:From.find('>')]
            Subject = Subject[:Subject.find('\n')]
            ttk.Button(frame, text=From, command=partial(self.message,i), width=40).grid(column=0, row=i, sticky=W)
            ttk.Button(frame, text=Subject[10:81], command=partial(self.message,i), width=70).grid(column=1, row=i, sticky=W)
            i += 1

        ttk.Button(mainframe, text='Send mail', command=self.send).grid(sticky=(S, E))
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_frame(event):
            # update the scrollbars to match the size of the inner frame
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=frame.winfo_reqwidth())
        frame.bind('<Configure>', _configure_frame)

        def _configure_canvas(event):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(frame_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    def message(self, id):
        self.root.unbind('<Configure>')
        mainframe = ttk.Frame(self.root, width=100, height=100)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        From, To, Subject, msg = self.messages[id][0], self.messages[id][1], self.messages[id][2], self.messages[id][3]
        text = Text(mainframe, width=80, height=25)
        text.grid(column=0, row=1, sticky=W)
        text.insert('1.0', From+'\n')
        text.insert('end', To+'\n')
        text.insert('end', Subject+'\n')
        text.insert('end', msg)
        text['state'] = 'disabled'
        ttk.Button(mainframe, text='Вернутись', command=self.mailbox).grid(column=0, row=0, sticky=(N,W))

    def send(self, *args):
        try:
            Mail_Sender.send_mail(self.login.get(), self.password.get())
        except Exception as e:
            print('Unsuccessful')
            print(e)

client = Email_client()
