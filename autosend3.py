#!/usr/bin/python
# -*- coding: UTF-8 -*-
import vk
import time
import threading
import re
threads = []
users= []

def kolvo():
    while True:
        print "#######################"
        print "Quantity users: " + str(len(threads))
        print users
        time.sleep(2)

def st(log,pas):
    session = vk.Session()
    session = vk.AuthSession('5001234', log, pas, scope='wall, messages, users')
    vk_api = vk.API(session)
    api = vk.API(session)
    vk_api.account.setOffline()
    users.append(int(vk_api.users.get()[0]["uid"]))
    
    resp_account = vk_api.account.getProfileInfo()
    print "new user: " + resp_account["first_name"] + " " + resp_account["last_name"]
    while True:
        resp = vk_api.messages.get(out="0", count = "1")[1]
        userid = int(resp["uid"])
        if resp["read_state"] == 0 and resp.keys()[6] != "users_count":
            print "@@@@@@@ message @@@@@@@@@"
            result = re.findall("/start .+ .+", resp["body"])
            if len(result) == 1:
                log = re.findall(" (.+) ", resp["body"])[0]
                pas = re.findall(" .+ (.+)", resp["body"])[0]
                print "login: " + log
                print "pass: " + pas
                try:
                    session2 = vk.Session()
                    session2 = vk.AuthSession('5001234', log, pas, scope='wall, messages, users')
                    vk_api2 = vk.API(session)
                    api2 = vk.API(session)
                except:
                    vk_api.messages.send(user_id=userid, message="Неправильный лоигн или пароль")
                    print ("error Login or Password is not avalible")
                else:
                    t = threading.Thread(target=st, args = (log, pas))
                    threads.append(t)
                    t.start()
                    vk_api.messages.send(user_id=userid, message="Готово")
                    print ("new threads")
                    
            else:
                print resp["body"]
                vk_api.messages.send(user_id=userid, message="Привет! Я отвечу в ближашее время!")
                try:
                    users.index(userid)
                except:
                    vk_api.messages.send(user_id=userid, message='Если хочешь такой же автоответчик, отправь "/start логин пароль"')
        time.sleep(2)
raw_input("For start please 'Enter'")
t = threading.Thread(target=kolvo)
threads.append(t)
t.start()
st("89999696689", "PoPcorN698")
