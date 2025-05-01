#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:38:23 2023

@author: pho
"""


from configparser import ConfigParser
import os, imaplib, email, unittest
from glob import glob
from datetime import datetime

from pypromice.tx import getMail, L0tx, sortLines

accounts_file = '/home/pho/Desktop/python_workspace/promice/pypromice/src/pypromice/local/credentials/accounts.ini'
credentials_file = '/home/pho/Desktop/python_workspace/promice/pypromice/src/pypromice/local/credentials/credentials.ini'
out_dir = '/home/pho/Desktop/python_workspace/promice/'
last_uid = 1800368

accounts_ini = ConfigParser()
accounts_ini.read_file(open(accounts_file))
accounts_ini.read(credentials_file)

# Get credentials
account = accounts_ini.get('aws', 'account')
server = accounts_ini.get('aws', 'server')
port = accounts_ini.getint('aws', 'port')    
password = accounts_ini.get('aws', 'password')

# Log in to email server
mail_server = imaplib.IMAP4_SSL(server, port)
typ, accountDetails = mail_server.login(account, password)
if typ != 'OK':
    print('Not able to sign in!')
    raise
    
# Grab new emails
result, data = mail_server.select(mailbox='"[Gmail]/All Mail"', 
                                  readonly=True)
print('mailbox contains %s messages' %data[0])

#------------------------------------------------------------------------------

# Get L0tx datalines from email transmissions
for uid, mail in getMail(mail_server, last_uid=last_uid):
    message = email.message_from_string(mail)
    try:
        name = str(message.get_all('subject')[0])
        d = datetime.strptime(message.get_all('date')[0], 
                              '%a, %d %b %Y %H:%M:%S %z')
    except:
        name=None
        d=None
    
    if name and 'Watson' in name or name and 'GIOS' in name:
        print(f'Watson/GIOS station message, {d.strftime("%Y-%m-%d %H:%M:%S")}')

        l0 = L0tx(message, None, None, 
                  sender_name=['emailrelay@konectgds.com','sbdservice'])
        
        if l0.msg: 
            content, attachment = l0.getEmailBody()
            attachment_name = str(attachment.get_filename())
            out_fn = attachment_name.split('able')[0]+'able.txt'
            out_path = os.sep.join((out_dir, out_fn))
    
            print(f'Writing to {out_fn}')
            print(l0.msg)
        
            with open(out_path, mode='a') as out_f:
                out_f.write(l0.msg + '\n')    