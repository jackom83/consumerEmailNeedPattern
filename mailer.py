import email.utils
import imaplib
import smtplib
from configparser import ConfigParser
from email.parser import HeaderParser
from typing import List, Dict, Tuple

CONF_SECTION = 'pec'
CONF_IMAP_HOST = 'imap_host'
CONF_IMAP_PORT = 'imap_port'
CONF_SMTP_HOST = 'smtp_host'
CONF_SMTP_PORT = 'smtp_port'
CONF_USER = 'user'


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
                            'sub':  header['Subject']
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


def send_mail_response(smtp: smtplib.SMTP, mail_list_ok: List[Dict], mail_list_ko: List[Dict]):







    pass


