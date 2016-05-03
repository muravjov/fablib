#!/usr/bin/env python
# coding: utf-8

import pyzmail
import os
import logging

def send_mail(subject, content, recipients, mail_settings, is_html=False):
    sender = (u'No reply', mail_settings["from"])
       
    prefered_encoding='utf-8'
    text_encoding='utf-8'
    
    dat = content, text_encoding
    if is_html:
        html = dat
        text_content = None
    else:
        html = None
        text_content = dat
    
    payload, mail_from, rcpt_to, msg_id=pyzmail.compose_mail(\
            sender, \
            recipients, \
            subject, \
            prefered_encoding, \
            text_content, \
            html=html, \
            attachments=[
                #('attached content', 'text', 'plain', 'text.txt', 'us-ascii')
            ])
    
    #print payload
    #print mail_from, rcpt_to, msg_id
    
    smtp_provider = mail_settings["smtp_provider"]
    if smtp_provider == "gmail":
        smtp_host = 'smtp.gmail.com'
        kwargs = {
            "smtp_port": 587,
            "smtp_mode": 'tls',
            "smtp_login": sender[1],
            "smtp_password": mail_settings["password"]
        }
    elif smtp_provider == "1gb":
        kwargs = {
            #"smtp_port": 25, # либо 465, если не работает 25, см. в личном кабинете
        }
        
        # :TRICKY: согласно тех.поддержке 1gb.ru, слова которой подтвердил Тим,
        # для автоматической рассылки использовать нужно только robots.1gb.ru, а
        # те сервера, что указаны в учетках, предназначены для использования человеком
        # (Thunderbird, Outlook и т.д.)
        
        if mail_settings.get("is_robots_smtp"):
            smtp_host = 'robots.1gb.ru'
        else:
            smtp_host = 'smtp-9.1gb.ru'
            
            kwargs = {
                #"smtp_port": 25, # либо 465, если не работает 25, см. в личном кабинете
                "smtp_login":    mail_settings["login"],
                "smtp_password": mail_settings["password"],
            }
    else:
        assert False
    
    ret=pyzmail.send_mail(payload, mail_from, rcpt_to, smtp_host, **kwargs)

    # что делать в случае проблем?
    if isinstance(ret, dict):
        if ret:
            logging.error('Mail, failed recipients:', ', '.join(ret.keys()))
    else:
        logging.error('Mail error: %s', ret)
