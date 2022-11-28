import imaplib
from configparser import ConfigParser
import os
import sys
import time
from datetime import datetime
import email.utils
from email.parser import HeaderParser
import locale
from typing import List, Dict


import requests


def update_dataset_ipa(config: ConfigParser) -> datetime:
    ipa_dataset_url = config.get('downloadCSVRTD', 'IPADatasetURL')
    dataset_location = config.get('downloadCSVRTD', 'datasetLocation')
    update_time = datetime.strptime(config.get('downloadCSVRTD', 'updateTime'), '%Y-%m-%d')
    now_datetime = datetime.now()

    if (now_datetime - update_time).days > 0:
        os.remove(dataset_location)
        r = requests.get(ipa_dataset_url, stream=True)
        with open(dataset_location, 'wb') as f:
            f.write(r.content)
        update_time = now_datetime

    return update_time


def open_connection(config: ConfigParser, pec_pass: str, verbose: bool = False) -> imaplib.IMAP4:

    host = config.get('pec', 'host')
    port = config.get('pec', 'port')
    if verbose:
        print('Connecting to ', host, ":", port, "...")

    connection = imaplib.IMAP4_SSL(host, port)

    # Login to our account
    user = config.get('pec', 'user')
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


def classify_mail(mail_list: List[Dict]):


    pass


if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, "it_IT.UTF8")

    try:
        #Read Config
        config_parser = ConfigParser()
        config_parser.read([os.path.expanduser('parameters.cfg')])

        #Update IPA Data
        last_update = update_dataset_ipa(config_parser)
        config_parser.set('downloadCSVRTD', 'updateTime', last_update.strftime('%Y-%m-%d'))
        with open(os.path.expanduser('parameters.cfg'), 'w') as configfile:
            config_parser.write(configfile)


        #Fetch & Classify Mail Unseen
        with open_connection(config_parser, sys.argv[1], verbose=True) as imap_conn:
            mail_list = fetch_unseen_mail(imap_conn)


        for m in mail_list:
            print('From:', m['from'], 'Date:', m['when'], 'Subject:', m['sub'])


        #(ok_mail_list, ko_mail_list) = classify_mail(mail_list)

    except (imaplib.IMAP4.error,  OSError) as e:
        print(sys.exc_info()[1])
        sys.exit(1)

