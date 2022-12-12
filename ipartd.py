import csv
import os
from configparser import ConfigParser
from datetime import datetime
from typing import List

import requests

CONFIG_SECTION = 'ipa_rtd'
CONF_IPA_DATASET_URL = 'ipa_dataset_url'
CONF_CUR_DATASET_LOC = 'dataset_location'
CONF_UPDATE_TIME = 'update_time'
CONF_FAKE_RDT = 'fake_rtd'


def update_dataset_ipa(config: ConfigParser, verbose: bool = False) -> datetime:
    ipa_dataset_url = config.get(CONFIG_SECTION, CONF_IPA_DATASET_URL)
    dataset_location = config.get(CONFIG_SECTION, CONF_CUR_DATASET_LOC)
    update_time = datetime.strptime(config.get(CONFIG_SECTION, CONF_UPDATE_TIME), '%Y-%m-%d')
    now_datetime = datetime.now()

    if verbose:
        print('IPA RTD Dataset Last Update:', update_time, ', now is:', now_datetime)
    if ((now_datetime - update_time).days > 0) or not(os.path.isfile(dataset_location)):
        if verbose:
            print('Need update, remove old file if exist and try new download...')
        if os.path.isfile(dataset_location):
            os.remove(dataset_location)

        r = requests.get(ipa_dataset_url, stream=True)
        with open(dataset_location, 'wb') as f:
            f.write(r.content)
        update_time = now_datetime
        if verbose:
            print('IPA RTD Dataset downloaded!')

    return update_time


def ipa_valid_rtd_addr(config: ConfigParser, test_mode: bool = False, verbose: bool = False) -> List[str]:

    valid_mails = set()
    with open(config.get(CONFIG_SECTION, CONF_CUR_DATASET_LOC)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[10]:
                valid_mails.add(row[10])  # Mail Responsabile
            if row[12]:
                valid_mails.add(row[12])  # Mail 1
            if row[14]:
                valid_mails.add(row[14])  # Mail 2
            if row[16]:
                valid_mails.add(row[16])  # Mail 3

    if test_mode:
        fake_rtd = config.get(CONFIG_SECTION, CONF_FAKE_RDT)
        print('Test Mode Enabled, inject fake RTD address:', fake_rtd)
        for r in fake_rtd.split(','):
            valid_mails.add(r)

    return sorted(list(valid_mails))


