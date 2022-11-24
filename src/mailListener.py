import imaplib
import configparser
import os


def open_connection(verbose=False):
    # Read the config file
    config = configparser.ConfigParser()
    config.read([os.path.expanduser('./src/parameters.cfg')])

    # Connect to the server
    host = config.get('pec', 'host')
    port = config.get('pec', 'port')
    if verbose: print('Connecting to ', host, ":", port, "...")
    connection = imaplib.IMAP4_SSL(host, port)

    # Login to our account
    user = config.get('pec', 'user')
    pwd = config.get('pec', 'pwd')
    if verbose: print('Logging in as', user, "...")
    connection.login(user, pwd)
    return connection


if __name__ == '__main__':
    c = open_connection(verbose=True)
    try:
        print(c)
    finally:
        c.logout()
