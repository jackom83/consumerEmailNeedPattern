import imaplib
import configparser
import os
import sys
import time
import datetime
import email.utils
from email.parser import HeaderParser
import locale




def open_connection(pec_pass, verbose=False):
    # Read the config file
    config = configparser.ConfigParser()
    config.read([os.path.expanduser('parameters.cfg')])

    # Connect to the server
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


if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
    mhp = HeaderParser()
    try:
        imap = open_connection(sys.argv[1], verbose=True)

        imap.select(mailbox="INBOX", readonly=False)
        (ret_code, messages) = imap.search(None, '(UNSEEN)')

        if ret_code == 'OK':
            for num in messages[0].split():
                (ret, header_data) = imap.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM REPLY-TO DATE)])')
                if ret == 'OK':
                    header_string = header_data[0][1].decode('utf-8')
                    header = mhp.parsestr(header_string)
                    if header['Subject'].startswith('POSTA CERTIFICATA:'):
                       # msg_from = email.utils.parseaddr(header['From'])
                        msg_datetime = email.utils.parsedate_to_datetime(header['Date'])

                        print('From:', header['From'], 'Reply-to:', email.utils.parseaddr(header['reply-to'])[1], 'Date:', msg_datetime, 'Subject:', header['Subject'])
                        #imap.store(num, '+FLAGS', '\\Seen')

    except (imaplib.IMAP4.error,  OSError) as e:
        print(sys.exc_info()[1])
        sys.exit(1)
    finally:
        imap.logout()
