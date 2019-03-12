import imaplib
import email
import re
class MailRecieve:
    SERVER = 'imap.gmail.com'
    @staticmethod
    def read_mail(USER, PASSWORD):
        imap = imaplib.IMAP4_SSL(MailRecieve.SERVER)
        imap.login(USER, PASSWORD)
        status, select_data = imap.select('INBOX')
        messages = []
        status, search_data = imap.search(None, 'ALL')
        id_list = search_data[0].split()
        if len(id_list) == 0: return []
        if len(id_list) < 20:
        	last_message, first_message = len(id_list)-1, -1
        else:
        	last_message, first_message = len(id_list)-1, len(id_list)-21
        for msg_id in range(last_message, first_message, -1):
            status, msg_data = imap.fetch(id_list[msg_id], '(RFC822)')
            msg_raw = msg_data[0][1]
            msg = email.message_from_bytes(msg_raw)
            email_subject = msg['subject']
            email_from = msg['from']
            email_to = msg['to']
            messages.append(
                [('From : ' + email_from), ('To : ' + email_to), ('Subject : ' + email_subject+'\n'), msg.get_payload()]
            )
        imap.logout()
        return messages
