import imaplib
import email
import re
class Mail_Recieve:
    SERVER = 'imap.gmail.com'
    @staticmethod
    def read_mail(USER, PASSWORD):
        imap = imaplib.IMAP4_SSL(Mail_Recieve.SERVER)
        imap.login(USER, PASSWORD)
        status, select_data = imap.select('INBOX')
        messages = []
        #nmessages = select_data[0].decode('utf-8')
        status, search_data = imap.search(None, 'ALL')
        id_list = search_data[0].split()
        last_message, first_message = len(id_list)-1, len(id_list)-21
        for msg_id in range(last_message, first_message, -1):
            msg_id_str = id_list[msg_id].decode('utf-8')
            status, msg_data = imap.fetch(id_list[msg_id], '(RFC822)')
            msg_raw = msg_data[0][1]
            msg = email.message_from_bytes(msg_raw)
            # mailing_list = msg.get('X-Mailing-List', 'undefined')
            mailing_list = msg.get('List-Id', 'undefined')
            mailing_list = re.sub('^(?s).*?<([^>]+?)(?:\\..*?)>.*$',
                              '\\1', mailing_list)
            email_subject = msg['subject']
            email_from = msg['from']
            email_to = msg['to']
            messages.append([('From : ' + email_from), ('To : ' + email_to), ('Subject : ' + email_subject), msg.get_payload()])
        imap.logout()
        return messages
