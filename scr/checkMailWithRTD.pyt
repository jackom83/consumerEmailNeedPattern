import configparser
import os
import wget
import csv


#input
mailList = ['rtd@istruzione.it','vincenzo.travascio@gmail.com']

#output
mailListOK = []
mailListKO = []


#set parameters
config = configparser.ConfigParser()
config.read('./scr/parameters.cfg')

IPADatasetURL=config.get('downloadCSVRTD','IPADatasetURL')
datasetLocation=config.get('downloadCSVRTD','datasetLocation')

#get IPA dataset and write on disk
try:
    os.remove(datasetLocation)
except FileNotFoundError:
    None

wget.download(IPADatasetURL, datasetLocation)

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
            
            mailListKO = mailList

            line_count += 1

print('mailListOK = ' + str(mailListOK))
print('mailListKO = ' + str(mailListKO))

    



