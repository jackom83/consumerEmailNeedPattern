import configparser
import os
import wget
import csv
from datetime import datetime

parametersPath = './src/parameters.cfg'

#example
mailList = ['rtd@istruzione.it','prova@prova.pr','sia.asprc@certificatamail.it']

#output
mailListOK = []
mailListKO = []

#set parameters
config = configparser.ConfigParser()
config.read(parametersPath)

IPADatasetURL = config.get('downloadCSVRTD','IPADatasetURL')
datasetLocation = config.get('downloadCSVRTD','datasetLocation')
updateTime = datetime.strptime(config.get('downloadCSVRTD','updateTime'),'%Y-%m-%d') 


#get IPA dataset and write on disk
nowdatetime = datetime.now()

if (nowdatetime - updateTime).days > 0:
    try:
        os.remove(datasetLocation)
    except FileNotFoundError:
        None
    
    with open(parametersPath, 'w') as configfile:
        config.write(configfile)

    wget.download(IPADatasetURL, datasetLocation)

    config.set('downloadCSVRTD','updateTime', nowdatetime.strftime('%Y-%m-%d'))

#check mail
with open(datasetLocation) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:            
            line_count += 1
        else:
            codice_ipa = row[1]
            mail_responsabile = row[10]
            mail_1 = row[12]
            mail_2 = row[14]
            mail_3 = row[16]
            
            for mail in mailList:
                if mail_responsabile and mail_responsabile == mail:
                    mailListOK.append(mail)
                    mailList.remove(mail)
                    break
                elif mail_1 and mail_1 == mail:
                    mailListOK.append(mail)
                    mailList.remove(mail)
                    break
                elif mail_2 and mail_2 == mail:
                    mailListOK.append(mail)
                    mailList.remove(mail)
                    break
                elif mail_3 and mail_3 == mail:
                    mailListOK.append(mail)
                    mailList.remove(mail)
                    break                        

            line_count += 1

            if not mailList:
                break

mailListKO = mailList

#debug
print('mailListOK = ' + str(mailListOK))
print('mailListKO = ' + str(mailListKO))


    



