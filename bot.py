# -*- coding: utf-8 -*-
import os, time
import requests
from datetime import datetime
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage


def get_results(query):
    requestparams = {
        'input': query,
        'format': 'plaintext',
        'output': 'JSON',
        'type': 'full',
    }

    # Going through the API explorer means we can get by without hitting free API key limits ;)
    waurl = 'https://www.wolframalpha.com/input/apiExplorer.jsp'
    referer = 'https://products.wolframalpha.com/api/explorer/'

    res = requests.get(waurl, params=requestparams,
                       headers={'referer': referer})
    return res.json()


def format_results(results):
    if not results['queryresult']['success']:
        return "_no valid result :(_"

    pods = results['queryresult']['pods']
    out_text = ""
    for pod in pods:
        out_text = out_text + '*' + pod['title'] + '*\n'
        out_text = out_text + \
            "\n".join(subpod['plaintext'] for subpod in pod['subpods']) + "\n"

    return out_text


def handle_message(message, contact):
    if isinstance(message, Message):
        send_msg = True
        if message.get_js_obj()['isGroupMsg']:
            if message.content.split(' ')[0].lower() != 'wa':
                send_msg = False
            else:
                query = " ".join(message.content.split(' ')[1:])
        else:
            if message.content.split(' ')[0].lower() == 'wa':
                query = " ".join(message.content.split(' ')[1:])
            else:
                query = message.content

        if send_msg:
            print(f"\nQuery: {query}")
            result_txt = format_results(get_results(query))
            contact.chat.send_message2(result_txt)


profiledir = os.path.join(".", "firefox_cache")
if not os.path.exists(profiledir):
    os.makedirs(profiledir)

driver = WhatsAPIDriver(profile=profiledir, client='remote',
                        command_executor="http://127.0.0.1:4444/wd/hub")
print("Waiting for QR")
driver.wait_for_login()
print("Saving session")
driver.save_firefox_profile(remove_old=False)
print("Bot started")

while True:
    print(f"\rchecking for more messages - {datetime.now()}", end='')
    for contact in driver.get_unread():
        for message in contact.messages:
            handle_message(message, contact)
    time.sleep(1)
