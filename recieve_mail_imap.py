import imaplib
import email
class MailRecieve:
    _server = 'imap.gmail.com'
    @staticmethod
    def read_mail(user, password):
        imap = imaplib.IMAP4_SSL(MailRecieve._server)
        imap.login(user, password)
        imap.select('INBOX')
        messages = []
        _, search_data = imap.search(None, 'ALL')
        id_list = search_data[0].split()
        if not id_list:
            return []
        if len(id_list) < 20:
            last_message, first_message = len(id_list)-1, -1
        else:
            last_message, first_message = len(id_list)-1, len(id_list)-21
        for msg_id in range(last_message, first_message, -1):
            _, msg_data = imap.fetch(id_list[msg_id], '(RFC822)')
            msg_raw = msg_data[0][1]
            msg = email.message_from_bytes(msg_raw)
            messages.append(
                {'from': ('From : ' + msg['from']),
                 'to': ('To : ' + msg['to']),
                 'date': ('Date : ' + ' '.join(msg['date'].split()[:4])),
                 'subject': ('Subject : ' + msg['subject']+'\n'),
                 'msg': msg.get_payload()}
            )
        imap.logout()
        return messages
