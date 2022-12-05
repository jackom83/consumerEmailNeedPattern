import email.utils
import imaplib
import smtplib
from configparser import ConfigParser
from datetime import datetime
from email.message import EmailMessage
from email.parser import HeaderParser
from functools import reduce
from typing import List, Dict, Tuple

import mailtemplate as mt

CONF_SECTION = 'mailer'
CONF_IMAP_HOST = 'imap_host'
CONF_IMAP_PORT = 'imap_port'
CONF_SMTP_HOST = 'smtp_host'
CONF_SMTP_PORT = 'smtp_port'
CONF_USER = 'user'
CONF_NOTIFY_LIST = 'notify_receipt_list'


def smtp_open_connection(config: ConfigParser, pec_pass: str, verbose: bool = False) -> smtplib.SMTP:
    host = config.get(CONF_SECTION, CONF_SMTP_HOST)
    port = config.get(CONF_SECTION, CONF_SMTP_PORT)
    if verbose:
        print('Connecting to ', host, ":", port, "...")

    connection = smtplib.SMTP_SSL(host, port)
    # Login to our account
    user = config.get(CONF_SECTION, CONF_USER)
    if verbose:
        print('Logging in as', user, "...")
    connection.login(user, pec_pass)
    return connection


def imap_open_connection(config: ConfigParser, pec_pass: str, verbose: bool = False) -> imaplib.IMAP4:
    host = config.get(CONF_SECTION, CONF_IMAP_HOST)
    port = config.get(CONF_SECTION, CONF_IMAP_PORT)
    if verbose:
        print('Connecting to ', host, ":", port, "...")

    connection = imaplib.IMAP4_SSL(host, port)

    # Login to our account
    user = config.get(CONF_SECTION, CONF_USER)
    if verbose:
        print('Logging in as', user, "...")
    connection.login(user, pec_pass)
    return connection


def fetch_unseen_mail(imap: imaplib.IMAP4) -> List[Dict]:
    mhp = HeaderParser()

    imap.select(mailbox="INBOX", readonly=False)
    (ret_code, messages) = imap.search(None, '(UNSEEN)')

    _mail_list = list()
    if ret_code == 'OK':
        for num in messages[0].split():
            (ret, header_data) = imap.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM REPLY-TO DATE)])')
            if ret == 'OK':
                header_string = header_data[0][1].decode('utf-8')
                header = mhp.parsestr(header_string)
                if header['Subject'].startswith('POSTA CERTIFICATA:'):
                    msg_datetime = email.utils.parsedate_to_datetime(header['Date'])
                    _mail_list.append(
                        {
                            'from': email.utils.parseaddr(header['reply-to'])[1],
                            'when': msg_datetime,
                            'sub': header['Subject']
                        }
                    )
    return _mail_list


def classify_mail(mail_list: List[Dict], rtd_mails: List[str]) -> Tuple[List[Dict], List[Dict]]:
    mail_list_ok = []
    mail_list_ko = []
    for row in mail_list:
        if row['from'] in rtd_mails:
            mail_list_ok.append(row)
        else:
            mail_list_ko.append(row)
    return mail_list_ok, mail_list_ko


def send_mail_response(config: ConfigParser, smtp: smtplib.SMTP, mail_list_ok: List[Dict], mail_list_ko: List[Dict],
                       verbose: bool = False):
    if verbose:
        print('List OK classified:')
        for m in mail_list_ok:
            print('From:', m['from'], 'Date:', m['when'], 'Subject:', m['sub'])

        print('List KO classified:')
        for m in mail_list_ko:
            print('From:', m['from'], 'Date:', m['when'], 'Subject:', m['sub'])

    for m in mail_list_ko:
        msg_subject = mt.template_response_subject.format(pec_when=m['when'].strftime('%Y-%m-%d'),
                                                          pec_sub=m['sub']
                                                          )
        msg_content = mt.template_response_ko.format(pec_when=m['when'].strftime('%Y-%m-%d'),
                                                     pec_sub=m['sub'],
                                                     pec_from=m['from']
                                                     )
        mail_message = mail_message_of(subject=msg_subject,
                                       sender=config.get(CONF_SECTION, CONF_USER),
                                       recipient=m['from'],
                                       content=msg_content)
        smtp.send_message(mail_message)

    # check notify
    if (mail_list_ok and len(mail_list_ok) > 0) or (mail_list_ko and len(mail_list_ko) > 0):

        msg_content_ko = ''
        if len(mail_list_ko) > 0:
            msg_content_ko = mt.template_notify_ko.format(
                n=len(mail_list_ko),
                msg_list=' '.join(
                    map(lambda x: '<li>From:' + x['from'] + 'at ' + x['when'].strftime('%Y-%m-%d')
                                  + 'subject: ' + x['sub'] + '</li>', mail_list_ko)
                    )
                )

        msg_content_ok = ''
        if len(mail_list_ok) > 0:
            msg_content_ok = mt.template_notify_ok.format(
                n=len(mail_list_ok),
                msg_list=' '.join(
                    map(lambda x: '<li>From:' + x['from'] + ' at ' + x['when'].strftime('%Y-%m-%d')
                                  + ' subject: ' + x['sub'] + '</li>', mail_list_ok)
                )
            )

        mail_message = mail_message_of(subject=mt.template_notify_subject,
                                       sender=config.get(CONF_SECTION, CONF_USER),
                                       recipient=config.get(CONF_SECTION, CONF_NOTIFY_LIST),
                                       content=msg_content_ko+msg_content_ok+mt.template_notify_end)
        smtp.send_message(mail_message)


def mail_message_of(subject: str, sender: str, recipient: str, content: str) -> EmailMessage:
    # construct email
    e_mail = EmailMessage()
    e_mail['Subject'] = subject
    e_mail['From'] = sender
    e_mail['To'] = recipient
    e_mail.set_content(content, subtype='html')

    return e_mail
