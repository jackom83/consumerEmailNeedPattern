import argparse
import imaplib
import locale
import os
import sys
import configparser

import ipartd
import mailer

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, "it_IT.UTF8")

    arg_parser = argparse.ArgumentParser(
        prog='Modi Governance Mail Checker',
        description='Monitoring ModI-Governance PEC to listen PA needs. Send notifications to AgID employees.',
        epilog='Mail received from an incorrect address (not RTD address) is replied as not accepted')

    arg_parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    arg_parser.add_argument('-t', '--test', dest='testmode', action='store_true')
    arg_parser.add_argument('password')

    args = arg_parser.parse_args()

    try:
        # Read Config
        config_parser = configparser.ConfigParser()
        config_file = os.path.expanduser('parameters.cfg')
        config_parser.read([config_file])

        # Update IPA Data
        last_update = ipartd.update_dataset_ipa(config_parser, verbose=args.verbose)
        config_parser.set(ipartd.CONFIG_SECTION, ipartd.CONF_UPDATE_TIME, last_update.strftime('%Y-%m-%d'))
        with open(config_file, 'w') as cf:
            config_parser.write(cf)

        # Read IPA RTD Mails
        rtd_mail_list = ipartd.ipa_valid_rtd_addr(config_parser, test_mode=args.testmode, verbose=args.verbose)

        # Fetch & Classify Mail Unseen
        with mailer.imap_open_connection(config_parser, args.password, verbose=args.verbose) as imap_conn:
            mail_list = mailer.fetch_unseen_mail(imap_conn)
            (ok_mail_list, ko_mail_list) = mailer.classify_mail(mail_list, rtd_mail_list)

        with mailer.smtp_open_connection(config_parser, args.password, verbose=args.verbose) as smtp_conn:
            mailer.send_mail_response(config_parser, ok_mail_list, ko_mail_list, verbose=args.verbose)

    except (imaplib.IMAP4.error, OSError) as e:
        print(sys.exc_info()[1])
        sys.exit(1)
