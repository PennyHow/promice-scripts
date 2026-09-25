#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:20:09 2022

Script to get L0tx transmission messages from a single station using the 
tx module

@author: Penelope How, pho@geus.dk
"""

from configparser import ConfigParser
import os, imaplib, email, re, toml, sys
from glob import glob
from datetime import datetime, timedelta

from pypromice.tx.tx import getMail, L0tx
from pypromice.tx.get_l0tx import sortLines
    
# imei_target = "300534068054860" # Cave AWS
imei_target = "300234068627400" # Unassigned

#------------------------------------------------------------------------------

# Set payload formatter paths
formatter_file = '/home/pho/aws-env/pypromice/src/pypromice/resources/payload_formats.csv'
type_file = '/home/pho/aws-env/pypromice/src/pypromice/resources/payload_types.csv'

# Set credential paths
accounts_file = '../credentials/accounts.ini'
credentials_file = "../credentials/credentials.ini"

# Set last aws uid path
# Fastmail
last_uid =  289506
mailbox_name="INBOX"

# Gmail geus.aws
#last_uid =  2784000
#mailbox_name = '"[Gmail]/All Mail"'

# Logger program path
# programs_dir = 'logger_programs/Freya2015.CR1'
# programs_dir = 'logger_programs/Promice2015e.CR1'
# print('parsing %s for message formats' % programs_dir)

#------------------------------------------------------------------------------

# Define accounts and credentials ini file paths
accounts_ini = ConfigParser()
accounts_ini.readfp(open(accounts_file))
accounts_ini.read(credentials_file) 
  
# Get credentials
account = accounts_ini.get('aws', 'account')
server = accounts_ini.get('aws', 'server')
port = accounts_ini.getint('aws', 'port')    
password = accounts_ini.get('aws', 'password')
if not password:
    password = input('password for AWS email account: ')
print('AWS data from server %s, account %s' %(server, account))

#------------------------------------------------------------------------------

# Log in to email server
mail_server = imaplib.IMAP4_SSL(server, port)
typ, accountDetails = mail_server.login(account, password)
if typ != 'OK':
    print('Not able to sign in!')
    raise
    
# Grab new emails
result, data = mail_server.select(mailbox=mailbox_name, readonly=True)
print('mailbox contains %s messages' %data[0])

#------------------------------------------------------------------------------

# Get L0tx datalines from email transmissions
for uid, mail in getMail(mail_server, last_uid=last_uid):
    message = email.message_from_string(mail)
    try:
        title = message.get_all('subject')[0]
        print(uid)
        # print(title)
        imei, = re.findall(r'[0-9]+', title)
        d = datetime.strptime(message.get_all('date')[0], 
                              '%a, %d %b %Y %H:%M:%S %Z')
        # print(d)

    except:
        imei = None
        d = None

    if str(imei) in imei_target:
        print(f'AWS message for {imei}, {d.strftime("%Y-%m-%d %H:%M:%S")}')
        l0 = L0tx(message, formatter_file, type_file)

        if l0.msg:
            print(l0.msg)
            print(l0.payload)
            print(l0.msg)

#------------------------------------------------------------------------------
print('Finished')
