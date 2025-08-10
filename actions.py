import time, random, os, string , secrets
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import createProfiles
from EmailClient import save_to_files
from createProfiles import mainlnesia, getFirstPart, mailforspam, login_to_gmail, close_secend_window
import re
import json
import time
import pyotp
from itertools import combinations
import requests
from bs4 import BeautifulSoup
import os,time,random
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import subprocess
import sys
import base64
import string
from filelock import FileLock
from selenium.webdriver.common.action_chains import ActionChains

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

    
class GmailActions():
    def urls():
        LoginUrl = "https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession"
        MainUrl = "https://mail.google.com/mail/u/0/"
        AccountUrl = "https://myaccount.google.com/"
        pliUrl = "https://myaccount.google.com/?pli=1"
        pliUrlMail = "https://mail.google.com/mail/u/0/?pli=1"
        SpamUrl = "https://mail.google.com/mail/u/0/#spam"

        url_list = [MainUrl, AccountUrl, pliUrl, pliUrlMail, SpamUrl]
        return url_list

    @classmethod
    def read_file(cls, filename):
        try:
            # Get the current working directory using os.getcwd()
            folder = "ressources"
            actsPath = os.path.join(folder, filename)
            # Concatenate the file name to the current working directory to form the absolute file path
            with open(actsPath, 'r') as file:
                data = file.read().splitlines()
                return data
        except:
            print(f"File {filename} not found.")
            return None

    @classmethod
    def close_secend_window(cls, driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    
    def checkAccount(IspUser, driver, close = False,support=False,manual=False,stay=False):
        LoginUrl = "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AaSxoQzm968VljTGXXK-IuqveUXb4V0LSpMHkPLtHcJXBRD44RhmWlkyucT011lBGvtnJfthH0sF&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1090154760%3A1716904486100740&ddm=0"
        MainUrl ='https://mail.google.com/mail/u/0/'
        try:
            driver.get(MainUrl)
            #close_secend_window(driver)
        except Exception as e:
            try:
                driver.refresh()  # Second attempt
            except Exception as e:
                save_to_files("proxy_failed", IspUser.showString())
                driver.quit()
                return
        currentUrl = driver.current_url
        separators = ['#inbox', '#spam']
        for separator in separators:
            try:
                currentUrl = currentUrl.split(separator, 1)[0]
            except:pass
        url_list = GmailActions.urls()
        try:
            driver.find_element(By.CSS_SELECTOR,"div[class='error-code']")
            save_to_files("proxy_failed", IspUser.showString())
            driver.quit()
            return
        except:pass
        
        if currentUrl in url_list and close:
            #close X gsuit
            try:
                driver.find_element(By.CSS_SELECTOR,"div[class='T-P-aut-UR T-P-aut']").click()
            except:pass
            save_to_files("ok", IspUser.showString())
            driver.quit()
        elif currentUrl != MainUrl:
            result = createProfiles.login_to_gmail(IspUser, driver, close, support, manual,stay)
            return result

    @classmethod
    def openMsg(cls, driver):
        try:
            driver.implicitly_wait(3)
            rows =driver.find_elements(By.CSS_SELECTOR,'tr[class="zA yO"], tr[class="zA zE"]')
            for row in rows:
                try:
                    row.click()
                    break
                except:pass
        except:pass
        driver.implicitly_wait(10)

    @classmethod
    def loginWait(cls, driver):
        while True:
            try:
                currentUrl = driver.current_url
            except:
                driver.quit()
                break
    @classmethod  
    def ReporNotSpam(cls, driver):
        spamUrl = "https://mail.google.com/mail/u/0/#spam"
        try:
            driver.get(spamUrl)
        except:
            return
        # driver.refresh()
        time.sleep(random.randint(2, 4))
        cls.search(driver)
        while True:
            try:

                cls.openMsg(driver)
                    
                driver.find_element(By.CSS_SELECTOR,"button[class='bzq bzr IdsTHf']").click()
            except:
                try:
                    refresh = driver.find_element(By.CSS_SELECTOR,'div[class="T-I J-J5-Ji nu T-I-ax7 L3"]')
                    refresh.click()
                except:
                    try:
                        driver.refresh()
                        driver.find_element(By.CSS_SELECTOR,"div[class='J-J5-Ji amH J-JN-I']")
                    except:
                        driver.quit()
                        break
    
    @classmethod
    def selectPage(cls, driver):
        selectall = driver.find_element(By.CSS_SELECTOR,"div[class='T-I J-J5-Ji T-Pm T-I-ax7 L3 J-JN-M-I']")
        selectall.click()
    
    @classmethod
    def notSpam(cls, driver):
        driver.find_element(By.CSS_SELECTOR,"div[class='T-I J-J5-Ji aFj T-I-ax7 T-I-Js-Gs mA']").click()

    @classmethod 
    def selectPage_notSpam(cls, driver):
        spamUrl = "https://mail.google.com/mail/u/0/#spam"
        try:
            driver.get(spamUrl)
        except:
            return
        cls.search(driver)
        while True:
            try:
                cls.selectPage(driver)
                cls.notSpam(driver)
                try:
                    refresh = driver.find_element(By.CSS_SELECTOR,'div[class="T-I J-J5-Ji nu T-I-ax7 L3"]')
                    refresh.click()
                except:pass
            except: break
    @classmethod
    def nextMsg(cls, driver):
        try:
            nextBtn = driver.find_element(By.CSS_SELECTOR,"[jslog='168965; u014N:cOuCgd,Kr2w4b;']")
            nextBtn.click()
        except:pass
    
    @classmethod
    def nextPage(cls, driver):
        nextPage = driver.find_elements(By.CSS_SELECTOR,"div[class*='T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3']")
        if len(nextPage)>1:
            nextPage[1].click()
        else:
            nextPage[0].click()          

    @classmethod
    def click(cls, driver):
        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
            largest_image = None
            largest_area = 0
            for img in image_elements:
                width = int(img.get_attribute("width") or 0)
                height = int(img.get_attribute("height") or 0)
                area = width * height

                if area > largest_area:
                    largest_area = area
                    largest_image = img
            largest_image.click()
            if len(driver.window_handles)>1:
                time.sleep(random.randint(5, 8))
                cls.close_secend_window(driver)
                time.sleep(random.randint(1, 2))
            wrong_img=None
            wrong_img = driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-aPU-JX')
            if wrong_img:
                back_btn= driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-Jq-I.aLF-aPX-auO-I.J-J5-Ji.aLF-aPX-I')
                back_btn.click()

        except:pass
        
    @classmethod
    def inbox_openClick(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return
        
    @classmethod
    def markAsImportant(cls, driver):
        try:
            hover_element= driver.find_element(By.CSS_SELECTOR, "div[class='T-I J-J5-Ji nf T-I-ax7 L3']") 
            hover_element.click()
            time.sleep(random.randint(2, 4))
            important = driver.find_elements(By.CSS_SELECTOR, "div.J-N[jslog='172448; u014N:cOuCgd,Kr2w4b;']")
            important[0].click()
        except:
            try:
                hover_element.click()
                time.sleep(random.randint(2, 4))
            except:pass
    
    @classmethod
    def inbox_openClickImportant(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.markAsImportant(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return
    
    @classmethod
    def addStar(cls, driver):
        try:
            star = driver.find_element(By.CSS_SELECTOR,".zd.bi4")
            star.click()
            time.sleep(random.randint(2, 5))
        except:pass
    
    @classmethod
    def inbox_openClickStart(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.addStar(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return
    
    @classmethod
    def inbox_openClickImportantStart(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.markAsImportant(driver)
            cls.addStar(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return

    @classmethod
    def reply(cls, driver):
        try:
            replys = cls.read_file("replys.txt")
            if replys:
                replyMsg = random.choice(replys)
            else:
                replyMsg = generate_random_string()
            replyBtn = driver.find_element(By.CSS_SELECTOR, ".T-I.J-J5-Ji.T-I-Js-IF.aaq.T-I-ax7.L3")
            replyBtn.click()
            time.sleep(random.randint(2, 5))
            replyInput = driver.find_element(By.CSS_SELECTOR, ".Am.aO9.Al.editable.LW-avf.tS-tW")
            replyInput.clear()
            replyInput.send_keys(replyMsg)
            time.sleep(random.randint(2, 5))
            # try:
            #     cover = driver.find_element(By.ID,"link_enable_notifications_hide")
            #     cover.click()
            # except:pass
            try:
                driver.find_element(By.CSS_SELECTOR, "span[id='link_enable_notifications_hide']").click()    
            except:pass
            driver.execute_script("window.scrollTo(0, 2000)")
            sendReply = driver.find_element(By.CSS_SELECTOR, "div[role='button'].T-I.J-J5-Ji.aoO.v7.T-I-atl.L3")
            sendReply.click()
            time.sleep(random.randint(2, 5))
        except:pass
        
    @classmethod
    def inbox_openClickReply(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.reply(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return
    @classmethod
    def archive(cls, driver):
        try:
            archive = driver.find_elements(By.CSS_SELECTOR,"div.T-I.J-J5-Ji.lR.T-I-ax7.T-I-Js-Gs.T-I-Js-IF.mA")
            archive[1].click()
            time.sleep(random.randint(2, 5))
        except:pass

    @classmethod
    def inbox_openClickArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.click(driver)
            cls.archive(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return

    @classmethod
    def selectPage_notSpam_inbox_OpenClickImportantStar(cls, driver, nbMsgs):
        cls.selectPage_notSpam(driver)
        driver.get("https://mail.google.com/mail/u/0/")
        cls.search(driver)
        cls.inbox_openClickImportantStart(driver, nbMsgs)
        try:
            driver.current_url
        except:
            return

    @classmethod
    def selectPage_notSpam_inbox_OpenClickReply(cls, driver, nbMsgs):
        cls.selectPage_notSpam(driver)
        driver.get("https://mail.google.com/mail/u/0/")
        cls.inbox_openClickReply(driver, nbMsgs)
        try:
            driver.current_url
        except:
            return
    
    @classmethod
    def importContact(cls, IspUser, driver ):
        try:
            current_project_path = os.getcwd()
            try:
                file_path = current_project_path+"\\ressources\\contacts.csv"
            except:pass
            while True:
                try:
                    contact_url='https://contacts.google.com/'
                    driver.get(contact_url)
                except:
                    save_to_files("add_contact_failed", IspUser.showString())
                    break
                try:
                    parent_a_element = driver.find_element(By.CSS_SELECTOR,".d5NbRd-EScbFb-JIbuQc.dgqZp")
                    parent_a_element.click()
                except:pass
                try:
                    file_input = driver.find_element(By.XPATH,"//input[@type='file']")
                    file_input.send_keys(file_path)
                    time.sleep(random.randint(3, 5))
                except:pass
                # try:
                #     txt=""
                #     span = driver.find_element(By.XPATH,"//span[@jsname='wRkGLe']")
                #     txt = span.text
                # except:pass                
                try:
                    imprt = driver.find_element(By.CSS_SELECTOR,"button[jsaction*='click'][data-mdc-dialog-action='ok']")
                    imprt.click()
                    save_to_files("add_contact_done", IspUser.showString())
                    time.sleep(random.randint(8, 10))
                    break
                except:
                    pass
        except:
            save_to_files("add_contact_failed", IspUser.showString())
        
    @classmethod
    def changePassword(cls, IspUser, driver):
        try:
            cls.checkAccount(IspUser, driver, False,False,False,False)
            new_password = IspUser.newPassword
            if new_password == None:
                print("syntax incorrect: To change password pls follow this sayntax password:::newpassword")
            else:
                driver.get("https://myaccount.google.com/signinoptions/rescuephone")
                cls.handle_otp(driver, IspUser)
                try:
                    old_password = IspUser.password
                    time.sleep(random.randint(3, 5))
                    password_field = driver.find_element(By.XPATH,"//input[@type='password' and @name='Passwd']")
                    time.sleep(random.randint(3, 5))
                    password_field.send_keys(old_password)
                    time.sleep(random.randint(3, 5))
                    next = driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf']")
                    next.click()
                    try:
                        password_field = driver.find_element(By.XPATH,"//input[@type='password' and @name='Passwd']")
                        time.sleep(random.randint(3, 5))
                        password_field.send_keys(old_password)
                        time.sleep(random.randint(3, 5))
                        next = driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf']")
                        next.click()
                    except:pass
                except:pass
                time.sleep(random.randint(3,5))
                url = driver.current_url
                # Replace "rescuephone" with "password" in the URL
                new_url = url.replace("rescuephone", "password")
                time.sleep(random.randint(3, 5))
                driver.get(new_url)
                time.sleep(random.randint(3, 5))
                while True:
                    url = driver.current_url 
                    if new_url ==url:
                        break
                    else:
                        driver.get(new_url)
                    time.sleep(random.randint(3, 5))
                newpwd_input = driver.find_elements(By.CSS_SELECTOR,".VfPpkd-fmcmS-wGMbrd.uafD5")
                newpwd_input[0].send_keys(new_password)
                time.sleep(random.randint(3, 5))
                newpwd_input[1].send_keys(new_password)
                time.sleep(random.randint(3, 5))
                nextbtn = driver.find_element(By.XPATH,"//button[@type='submit']")
                nextbtn.click()
                time.sleep(random.randint(8, 10))
                save_to_files("password_changed",IspUser.showString())
        except Exception as e:
            save_to_files("password_NotChanged",IspUser.showString())
    
    @classmethod
    def changeRecovry(cls, IspUser, driver, bouth=False):
        try:
            new_recovery =  IspUser.newRecovery
            if new_recovery == None:
                print("syntax incorrect: To change password pls follow this sayntax recovery:::newrecovery")
            else:
                recovryLink = "https://myaccount.google.com/u/8/recovery/email?"
                if not bouth:
                    cls.checkAccount(IspUser, driver, False,False,False,False)
                    try:
                        password = IspUser.password
                        driver.get(recovryLink)
                        cls.enter_password(driver, password)
                        cls.handle_otp(driver, IspUser)
                        time.sleep(random.randint(3,5))
                        #driver.execute_script("window.scrollTo(0, 500)")
                        #driver.find_element(By.CSS_SELECTOR, "a[href*='signinoptions/rescuephone?']").click()
                        # password_field = driver.find_element(By.XPATH,"//input[@type='password' and @name='Passwd']")
                        # time.sleep(random.randint(3,5))
                        # password_field.send_keys(password)
                        # time.sleep(random.randint(3,5))
                        # next = driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf']")
                        # next.click()
                        # time.sleep(random.randint(3,5))
                    except:pass
                else:
                    driver.get(recovryLink)
                    cls.handle_otp(driver, IspUser)
                    time.sleep(random.randint(3,5))
                urlrecov = driver.current_url
                # Replace "rescuephone" with "recovry" in the URLs
                new_urlrecov = urlrecov.replace("signinoptions/rescuephone", "recovery/email")
                driver.get(new_urlrecov)
                time.sleep(random.randint(3,5))
                try:
                    driver.find_elements(By.CSS_SELECTOR,"button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")[1].click()
                except:pass
                newrecovery_input = driver.find_element(By.CSS_SELECTOR,'input[type="email"]')
                newrecovery_input.clear()
                time.sleep(random.randint(1,2))
                newrecovery_input.send_keys(new_recovery)
                time.sleep(random.randint(3,5))
                nextbtn = driver.find_element(By.CSS_SELECTOR,".UywwFc-LgbsSe.UywwFc-LgbsSe-OWXEXe-dgl2Hf.wMI9H")
                nextbtn.click()
                time.sleep(random.randint(3,5))
                save_to_files("recovery_changed",IspUser.showString())
                time.sleep(2)
        except:
            save_to_files("recovery_NotChanged",IspUser.showString())
    
    @classmethod
    def changePasswordRecovry(cls, IspUser, driver):
        cls.changePassword(IspUser, driver)
        cls.changeRecovry(IspUser, driver, True)
    
    @classmethod
    def cleanAll(cls, driver):
        driver.get("https://mail.google.com/mail/u/0/#all")
        i=0
        driver.refresh()
        while True:
            i+=1
            try:
                try:
                    parent = driver.find_element(By.CSS_SELECTOR,".J-J5-Ji.amH.J-JN-I")
                except:
                    break
                all= driver.find_element(By.CSS_SELECTOR,"span[class*='T-Jo J-J5-Ji']")
                all.click()
                try:
                    # parent = driver.find_element(By.CSS_SELECTOR, "div.ya.yb")
                    full = driver.find_element(By.CSS_SELECTOR,"div[class='T-I J-J5-Ji nX T-I-ax7 T-I-Js-Gs  mA']")
                    full.click()
                    time.sleep(random.randint(1, 3))
                except:pass
                delete =driver.find_element(By.CSS_SELECTOR,"div[data-tooltip='Delete']")
                delete.click() 
                time.sleep(random.randint(1, 3))
                driver.find_element(By.CSS_SELECTOR,".J-at1-auR.J-at1-atl").click()
                time.sleep(10)
                if i==5:
                    driver.refresh()
                    i=0
            except:
                try:
                    driver.current_url
                except:
                    break
    
    @classmethod
    def markAsRead(cls, driver):

        try:
            driver.find_element(By.CSS_SELECTOR,"div[class*='T-I J-J5-Ji m9 T-I-ax7']").click()
        except:pass

    @classmethod
    def search(cls, driver):
        try:
            seachkey = cls.read_file("search.txt")
            try: 
                search_input = driver.find_element(By.CSS_SELECTOR,"input[aria-owns='gs_sbt50']")
                search_input.send_keys(seachkey)
                search_input.send_keys(Keys.RETURN)
                driver.refresh()
            except:pass
        except:
            print("search.txt not exist")
    
    @classmethod
    def allStar(cls, driver):
        try:
            hover_element= driver.find_element(By.CSS_SELECTOR, ".T-I.J-J5-Ji.nf.T-I-ax7.L3")
            hover_element.click()
            time.sleep(random.randint(2, 4))
            star = driver.find_element(By.CSS_SELECTOR, "div.J-N[jslog='56746; u014N:cOuCgd,Kr2w4b;']")
            star.click()
            time.sleep(random.randint(2, 4))
        except:
            try:
                hover_element.click()
            except:pass
    
    @classmethod
    def inbox_selectpageReadImportantStart_bySearch(cls, driver, nbMsgs): 
            cls.search(driver)
            for i in range(nbMsgs):
                cls.selectPage(driver)
                cls.markAsRead(driver)
                cls.markAsImportant(driver)
                cls.allStar(driver)
                cls.nextPage(driver)
                try:
                    driver.current_url
                except:
                    return
        
    @classmethod
    def actionByChoice(cls, IspUser, driver, nbMsgs):
        acts_filename="actions.txt"
        acts_list = cls.read_file(acts_filename)
        cat, acts_func = acts_list[0].split(":")
        acts_func = acts_func.split(";")

        if acts_func =="changePassword":
            cls.changePassword(IspUser, driver)
        elif acts_func =="changeRecovry":
            cls.changeRecovry(IspUser, driver)
        elif acts_func =="changePasswordRecovry":
            cls.changePasswordRecovry(IspUser, driver)
        elif acts_func =="importContact":
            cls.importContact(IspUser, driver)
        elif acts_func =="clean":
            cls.cleanAll(IspUser, driver)
        elif acts_func =="checkAccount" or acts_func =="createProfiles":
            cls.checkAccount(IspUser, driver)
        else:
            if acts_func:
                instance = GmailActions()
                if cat =="spam":
                    driver.get("https://mail.google.com/mail/u/0/#spam")
                    driver.refresh()
                for i in range(nbMsgs):
                    for act in acts_func:
                        method  = getattr(GmailActions, act, None)

                        # Check if the function exists
                        if method and callable(method) and hasattr(method, '__self__') and method.__self__ is GmailActions:
                            # Call the class method with the driver parameter
                            method(driver)
                        else:
                            save_to_files('log',f"Function '{act}' not found or not callable.")

    def selectPage_notSpam_inbox_selectpageReadImportantStartArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.selectPage_notSpam(driver)
            cls.selectPage(driver)
            cls.markAsRead(driver)
            cls.markAsImportant(driver)
            cls.allStar(driver)
            cls.archive(driver)
            try:
                driver.current_url
            except:
                return

    @classmethod
    def inbox_openStartReply(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            cls.openMsg(driver)
            cls.addStar(driver)
            cls.reply(driver)
            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return
    
    @classmethod
    def notPromotions(cls, driver, nbMsgs):
        driver.get("https://mail.google.com/mail/u/0/#category/promotions")
        driver.refresh()
        time.sleep(random.randint(3,5))
        for i in range(nbMsgs):
            try:
                All = driver.find_element(By.CSS_SELECTOR,"span[class*='T-Jo J-J5-Ji']")
                All.click()
                time.sleep(random.randint(3,5))
                not_promo = driver.find_element(By.CSS_SELECTOR,"div[class*='T-I J-J5-Ji T-I-ax7 L3']")
                not_promo.click()
                time.sleep(random.randint(3,5))
                try:
                    driver.find_element(By.CSS_SELECTOR, "dic[class='J-J5-Ji amH J-JN-I']")
                except:break
            except:
                break
            try:
                driver.current_url
            except:
                return
    
    @classmethod
    def randomActions(cls, driver, nbMsgs):
        function_data = [
            (cls.click, [driver]),
            (cls.markAsImportant, [driver]),
            (cls.addStar, [driver]),
            (cls.reply, [driver]),
            (cls.archive, [driver])
        ]

        for _ in range(nbMsgs):
            cls.openMsg(driver)
            
            # Randomly determine the number of functions to select (between 1 and the total number of functions)
            num_functions_to_select = random.randint(1, len(function_data))

            # Randomly select the specified number of UNIQUE functions with their respective arguments
            selected_functions = random.sample(function_data, k=num_functions_to_select)

            # Execute the selected functions
            for selected_function, args in selected_functions:
                selected_function(*args)

            cls.nextMsg(driver)
            try:
                driver.current_url
            except:
                return

    @classmethod
    def first_login_changePassword(cls, IspUser, driver):
        try:
            cls.checkAccount(IspUser, driver)
            new_password = IspUser.newPassword
            if new_password == None:
                print("syntax incorrect: To change password pls follow this sayntax password:::newpassword")
            else:
                time.sleep(random.randint(3, 5))
                newpwd_input = driver.find_elements(By.CSS_SELECTOR,"input[name='Password']")
                newpwd_input[0].send_keys(new_password)
                time.sleep(random.randint(3, 5))
                newpwd_input = driver.find_elements(By.CSS_SELECTOR,"input[name='ConfirmPassword']")
                newpwd_input[0].send_keys(new_password)
                time.sleep(random.randint(3, 5))
                nextbtn = driver.find_element(By.CSS_SELECTOR,"input[type='submit']")
                nextbtn.click()
                time.sleep(random.randint(8, 10))
                save_to_files("password_changed",IspUser.showString())
        except:
            save_to_files("password_NotChanged",IspUser.showString())
    
    @classmethod
    def disable_forwarding(cls, driver):
        try:
            driver.get("https://mail.google.com/mail/u/0/#settings/fwdandpop")
            time.sleep(2)
            input = driver.find_elements(By.CSS_SELECTOR,"input[name='sx_em']")[0]
            input_value = input.get_attribute('value')
            if input_value=="0":
                input.click()
                time.sleep(1)
                driver.find_element(By.XPATH,"/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[4]/td/div/button[1]").click()
                time.sleep(3)
        except:pass
        try:
            driver.current_url
        except:
            return
    @classmethod
    def recovery(cls,driver, IspUser):
        # Handling Recovery input
        try:
            recov = driver.find_elements(By.CSS_SELECTOR, "div[role='link'][data-accountrecovery='false']")
            try:
                recov[2].click()
                recoveryInput = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                recoveryInput.send_keys(IspUser.recovery)
                time.sleep(1)
                nextBtn= driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']")
                nextBtn.click()
            except:
                try:
                    secendpart = getFirstPart(IspUser.recovery, True)
                    current_url = driver.current_url
                    current_url = current_url.split('?', 1)[0]
                    if secendpart =="mailforspam.com" and current_url =='https://accounts.google.com/signin/v2/challenge/selection':
                        recov[0].click()
                        mailPart = getFirstPart(IspUser.recovery)
                        mailforspam(driver, mailPart)
                    if secendpart !="mailforspam.com" and current_url =='https://accounts.google.com/signin/v2/challenge/selection':
                        driver.quit()
                        save_to_files("recovery_problem", IspUser.showString())
                except:pass

                try:
                    # Recov Wrong
                    recov_wrong = driver.find_element(By.CSS_SELECTOR,"div[class='Ekjuhf Jj6Lae']")
                except:
                    try:
                        # Too many Reterys
                        recov_wrong = driver.find_element(By.CSS_SELECTOR,"div[jsname='TMYUoe']")
                    except:pass
                try:
                    if recov_wrong:
                        save_to_files("wrong_recovery", IspUser.showString())
                        driver.quit()
                        return True
                except:pass

        except:pass

    @classmethod
    def twoFactourAuth(cls, ispUser, driver):
        try:
            driver.get("https://myaccount.google.com/two-step-verification/authenticator")
            cls.enter_password(driver,ispUser.password)
            url = driver.current_url
            url = url.split('?')[0]
            if url == 'https://accounts.google.com/signin/v2/challenge/selection' or url == 'https://accounts.google.com/v3/signin/challenge/selection':
                cls.recovery(driver, ispUser)
            cls.handle_otp(driver, ispUser)
            time.sleep(3)
            url = driver.current_url
            url, _ = url.split("?")
            if url == "https://accounts.google.com/v3/signin/challenge/pwd":
                try:
                    pwd = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
                except:
                    try:
                        pwd = driver.find_element("xpath", '//input[@type="password" and @name="Passwd"]')
                    except:
                        pass
                try:
                    if pwd:
                        pwd.send_keys(ispUser.password)
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                except:pass
            driver.find_element(By.CSS_SELECTOR,"button[class*='AeBiU-LgbsSe']").click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR,"button[class*='mUIrbf-LgbsSe']").click()
            time.sleep(2)

            secret = driver.find_element(By.CSS_SELECTOR,"ol.AOmWL div > strong").text
            otp = cls.generate_otp(ispUser.email, secret)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe']")[6].click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"input[type='text']").send_keys(otp)
            time.sleep(2)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe']")[7].click()
            time.sleep(2)

        except:pass
    @classmethod
    def enter_password(cls, driver, password):
        time.sleep(1)
        url = driver.current_url
        url, _ = url.split("?")
        if  url == 'https://accounts.google.com/v3/signin/challenge/pwd':
            try:
                pwd = driver.find_element("xpath", '//input[@type="password" and @name="Passwd"]')
                
            except:
                try:
                    pwd = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
                except:
                    pass
            try:
                if pwd:
                    pwd.send_keys(password)
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                    time.sleep(2)
            except:pass

    @classmethod
    def app_password(cls, ispUser, driver):
        try:
            driver.get("https://myaccount.google.com/apppasswords")
            cls.enter_password(driver,ispUser.password)
            url = driver.current_url
            url = url.split('?')[0]
            if url == 'https://accounts.google.com/signin/v2/challenge/selection' or url == 'https://accounts.google.com/v3/signin/challenge/selection':
                cls.recovery(driver, ispUser)
            cls.handle_otp(driver, ispUser)
            otp = cls.request_otp(ispUser.email)
            if otp == "":
                save_to_files("otp_invalid", ispUser.showString())
                driver.quit()
                return True
            
            values = [
                "smtp",
                "gmail",
                "gmail smtp",
                "send",
                "password",
                "app password",
                "my app",
            ]
            random_value = random.choice(values)
            pwds = driver.find_elements(By.CSS_SELECTOR,"button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")
            for pwd in pwds:
                try:
                    pwd.click()
                except:pass
            try:
                driver.find_element(By.CSS_SELECTOR,"input[class='VfPpkd-fmcmS-wGMbrd ']").send_keys(random_value)
            except:
                try:
                    driver.get('https://myaccount.google.com/signinoptions/twosv')
                    time.sleep(2)
                    cls.enter_password(driver,ispUser.password)
                    try:
                        try:
                            driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[1].click()
                        except:
                            driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[0].click()
                        time.sleep(2)
                        driver.find_elements(By.CSS_SELECTOR,"button[class*='mUIrbf-LgbsSe']")[1].click()
                        time.sleep(2)
                        driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[2].click()
                        time.sleep(2)
                        driver.find_element(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']").click()
                    except:pass
                    time.sleep(2)
                    driver.get("https://myaccount.google.com/apppasswords")
                    time.sleep(2)
                    cls.handle_otp(driver, ispUser)
                    cls.enter_password(driver,ispUser.password)
                    cls.handle_otp(driver, ispUser)
                    driver.find_element(By.CSS_SELECTOR,"input[class='VfPpkd-fmcmS-wGMbrd ']").send_keys(random_value)
                except:pass
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button[class*='AeBiU-LgbsSe']").click()
            time.sleep(1)
            element = driver.find_element(By.XPATH, '//header[@class="VuF2Pd lY6Rwe"]//div[@dir="ltr"]')
            app_password = ''.join(span.text for span in element.find_elements(By.TAG_NAME, 'span'))
            while len(app_password)<15:
                time.sleep(1)
                element = driver.find_element(By.XPATH, '//header[@class="VuF2Pd lY6Rwe"]//div[@dir="ltr"]')
                time.sleep(1)
                app_password = ''.join(span.text for span in element.find_elements(By.TAG_NAME, 'span'))
                
            smtp_path = os.path.join("result", "smtp.txt")
            with open(smtp_path, "a") as f:
                    f.write(f"{ispUser.email}:{app_password}\n")
        except Exception as e:
            pass

    @classmethod
    def load_secrets(cls):
        try:
            secret_path = os.path.join("result", "secrets.json")
            try:
                with open(secret_path, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                # Create the file if it does not exist and return an empty dictionary
                with open(secret_path, 'w') as f:
                    json.dump({}, f)  # Initialize with an empty JSON object
                return {}
        except Exception as e :
            save_to_files("log",e.args[0]+"\n")
        
    # Save secrets to the JSON file
    @classmethod
    def save_secrets(cls, email, secrets):
        secret_path = os.path.join("result", "secrets.json")
        lock_path = secret_path + ".lock"

        # Ensure the 'result' directory exists
        os.makedirs(os.path.dirname(secret_path), exist_ok=True)

        lock = FileLock(lock_path)

        with lock:
            existing_secrets = cls.load_secrets()

            existing_secrets[email] = secrets

            with open(secret_path, 'w') as f:
                json.dump(existing_secrets, f, indent=4)

    # Function to extract the secret from the otpauth URL
    @classmethod
    def extract_secret_from_otpauth(cls,otpauth_url):
        # Regex to match and extract the secret from the URL
        match = re.search(r'secret=([A-Za-z0-9]+)', otpauth_url)
        if match:
            return match.group(1)
        return None
    
    @classmethod
    def generate_otp(cls,email, secret):
        try:
            # Use the extracted secret to generate OTP
            secret = secret.replace(' ', '')
            cls.save_secrets(email, secret)
            totp = pyotp.TOTP(secret)
            otp = totp.now()
        except Exception as e :
            save_to_files("log",e.args[0])

        return otp
    @classmethod
    def request_otp(cls,email):
        try:
            # Load existing secrets
            secrets = cls.load_secrets()
            secrets = {k.strip().lower(): v.strip() for k, v in secrets.items()}
            if email in secrets:
                secret = secrets[email]
                totp = pyotp.TOTP(secret)
                new_otp = totp.now()
                return new_otp
            return ""
        except Exception as e :
            save_to_files("log",e.args[0]+"\n")
    @classmethod
    def insert_dots(cls, email, num_dots):
        local, domain = email.split('@')
        positions = list(range(1, len(local)))
        
        dot_combinations = combinations(positions, num_dots)
        results = []
        
        for combo in dot_combinations:
            dotted_local = local
            offset = 0
            for pos in combo:
                dotted_local = dotted_local[:pos+offset] + '.' + dotted_local[pos+offset:]
                offset += 1
            results.append(dotted_local + '@' + domain)
        
        return results
    @classmethod
    def handle_otp(cls, driver, IspUser):
        try:
            time.sleep(1)
            url = driver.current_url
            url, _ = url.split("?")
            if url == "https://accounts.google.com/v3/signin/challenge/totp" or url == "https://accounts.google.com/signin/v2/challenge/totp":
                try:
                    otp = cls.request_otp(IspUser.email)
                    if otp == "":
                        save_to_files("otp_app", IspUser.showString())
                        driver.quit()
                        return True
                    else:
                        driver.find_element(By.CSS_SELECTOR,"input[type='tel']").send_keys(otp)
                        driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ ']").click()
                        time.sleep(2)
                except Exception as e :pass
        except:pass
    @classmethod
    def generate_combinations_for_file(cls, IspUser,driver):
            # Generate combinations with 1 dot
            one_dot = cls.insert_dots(IspUser.email, 1)
            # Generate combinations with 2 dots
            #two_dots = cls.insert_dots(IspUser.email, 2)

            driver.get("https://mail.google.com/mail/u/1/#settings/accounts")
            for combo in one_dot:
                cls.change_from(combo,driver)
            # for combo in two_dots:
            #     cls.change_from(combo,driver)
    @classmethod
    def change_from(cls, email, driver):
        try:
            driver.get("https://mail.google.com/mail/u/0/#settings/accounts")
            time.sleep(2)
            add_email = driver.find_elements(By.CSS_SELECTOR,"span[class='sA']")
            add_email[-1].click()
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[name='cfa']").send_keys(email)      
        except:pass
        
        try:
            
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[id='focus']").click()
            
            driver.switch_to.window(windows[0])
            close_secend_window(driver)
            save_to_files("from_aded", email+"\n")
        except:
            driver.switch_to.window(windows[0])
            driver.close()
            save_to_files("from_Failed", email)
    
        
    @classmethod
    def confirm_device(cls, IspUser, driver):
        try:
            driver.get('https://myaccount.google.com/u/0/notifications')
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"a[class='PfHrIe']").click()
            time.sleep(2)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe']")[1].click()
        except:pass
        

    @classmethod
    def less_secure(cls, IspUser, driver):
        try:
            driver.get('https://myaccount.google.com/u/0/lesssecureapps')
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-scr2fc']").click()
            save_to_files("les_secure_on", IspUser.showString())
        except:pass

    @classmethod
    def open_youtube(cls, driver):
        try:

            folder = "ressources"
            file_path = os.path.join(folder, "liks.txt")
            if not os.path.exists(file_path):
                print("Error: 'links.txt' is required in the 'ressources' folder.")
                return None
            else:
                with open(file_path, "r") as file:
                    links = [line.strip() for line in file if line.strip()]
                link=  random.choice(links) if links else None
                driver.get(link)
                sleep_time = random.uniform(180, 480)
                time.sleep(sleep_time)
        except:pass

    @classmethod
    def generate_7_digit_number(cls):
        return ''.join(random.choices('0123456789', k=7))

    @classmethod
    def activatetwoFactour(cls, IspUser, driver):
        try:
            driver.get('https://myaccount.google.com/signinoptions/twosv')
            time.sleep(2)
            cls.enter_password(driver,IspUser.password)
            otp = cls.handle_otp(driver,IspUser.email)
            if otp == "":
                save_to_files("otp_invalid", IspUser.showString())
                driver.quit()
                return True
            try:
                driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[1].click()
            except:
                driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[0].click()
            time.sleep(2)
            nb_elemet=""
            cr_code = "+1669"
            nb = cls.generate_7_digit_number()
            number = cr_code+ nb
            nb_elemet= driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
            if nb_elemet!="":
                nb_elemet.send_keys(number)
                try:
                    driver.find_elements(By.CSS_SELECTOR, "button[class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf']")[2].click()
                    time.sleep(2)
                    driver.find_elements(By.CSS_SELECTOR, "button[class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf']")[3].click()
                    time.sleep(2)
                    
                    for i in range(10):
                        try:
                            driver.get("https://myaccount.google.com/two-step-verification/phone-numbers")
                            time.sleep(2)
                            nb = driver.find_elements(By.CSS_SELECTOR, "button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")
                            if nb:
                                try:
                                    if len(nb)>1:
                                        nb[1].click()
                                    else:
                                        nb[0].click()
                                except:pass
                            
                            confirmbtn = driver.find_elements(By.CSS_SELECTOR, "button[class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf']")[1]
                            confirmbtn.click()
                            time.sleep(10)
                            save_to_files("phone_removed", IspUser.showString())    
                            save_to_files("otp_activated", IspUser.showString())
                            time.sleep(10)
                            break
                        except:pass
                    return
                except:
                    save_to_files("Failed_removed_phone", IspUser.showString())
            time.sleep(3)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='mUIrbf-LgbsSe']")[1].click()
            time.sleep(2)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']")[2].click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']").click()
            save_to_files("otp_activated", IspUser.showString())
            return
        except Exception as e: 
            save_to_files("otp_activation_failed", IspUser.showString())
            save_to_files("log",e.args[0]+"\n")
        

    @classmethod
    def RemoveTwoFactourAuth(cls, driver, IspUser):
        try:
            driver.get("https://myaccount.google.com/signinoptions/twosv")
            url = driver.current_url
            url, _ = url.split("?")
            cls.enter_password(driver, IspUser.password)
            cls.handle_otp(driver, IspUser)
            try:
                driver.find_element(By.CSS_SELECTOR, "button[class='AeBiU-LgbsSe AeBiU-LgbsSe-OWXEXe-dgl2Hf wMI9H']").click()
                time.sleep(2)
                try:
                    driver.find_elements(By.CSS_SELECTOR, "button[class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf']")[1].click()
                except:
                    save_to_files("Failed_ToRemove_Otp", IspUser.showString())
                    return True
            except:pass
            driver.get("https://myaccount.google.com/two-step-verification/authenticator")
            time.sleep(1)
            try:
                driver.find_elements(By.CSS_SELECTOR,"button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")[0].click()
            except:
                driver.find_elements(By.CSS_SELECTOR,"button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")[1].click()
            time.sleep(2)
            
            for i in range(10):
                try:
                    driver.execute_script("document.body.offsetHeight;")
                    btn = driver.find_elements(By.CSS_SELECTOR,"button[class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf']")
                    btn[1].click()
                    time.sleep(3)
                    save_to_files("otp_Removed", IspUser.showString())
                    break
                except:pass
        except Exception as e:
            save_to_files("Failed_ToRemove_Otp", IspUser.showString())

    @classmethod
    def AddFromEmails(cls, driver):
        try:
            folder = "ressources"
            file_path = os.path.join(folder, "from_emails.txt")
            if not os.path.exists(file_path):
                print("Error: 'from_emails.txt' is required in the 'ressources' folder.")
                return None
            else:
                with open(file_path, "r") as file:
                    emails = [line.strip() for line in file if line.strip()]
            for email in emails:
                cls.change_from(email, driver)
        except:pass

    @staticmethod
    def get_random_wikipedia_topic():
        try:
            url = "https://en.wikipedia.org/wiki/Special:Random"
            response = requests.get(url, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find("h1").text
            return title.strip()
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
            return None

    @staticmethod
    def get_random_reddit_topic():
        try:
            url = "https://www.reddit.com/r/todayilearned/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            titles = soup.find_all("h3")
            topics = [title.text.strip() for title in titles if title.text.strip()]
            return random.choice(topics) if topics else None
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
            return None

    @staticmethod
    def get_random_bbc_topic():
        try:
            url = "https://www.bbc.com/news"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            headlines = soup.find_all("h3")
            topics = [h.text.strip() for h in headlines if h.text.strip()]
            return random.choice(topics) if topics else None
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
            return None

    @staticmethod
    def get_random_topic():
        sources = [GmailActions.get_random_wikipedia_topic, GmailActions.get_random_reddit_topic, GmailActions.get_random_bbc_topic]
        random.shuffle(sources)
        for source in sources:
            topic = source()
            if topic:
                return topic
        return "Interesting topic"

    @classmethod
    def search_google(cls,driver):
        query = GmailActions.get_random_topic()
        driver.get("https://www.google.com")
        time.sleep(2)

        box = driver.find_element(By.NAME, "q")
        box.send_keys(query)
        box.send_keys(Keys.RETURN)
        time.sleep(3)  # Let it load results
        titles = driver.find_elements(By.CSS_SELECTOR, 'h3.LC20lb.MBeuO.DKV0Md')
        if titles:
            random_title = random.choice(titles)
        driver.execute_script("arguments[0].click();", random_title)
        time.sleep(5)
        scroll_pause_time = 1
        for _ in range(10):  # scroll 10 times
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(scroll_pause_time)
        time.sleep(random.uniform(20, 40))

    @classmethod
    def generate_tokens(cls,IspUser):
        try:
            # print(f"Auth from {IspUser.email} in process ...")
            directory_path= "ressources"
            json_files = [
                f for f in os.listdir(directory_path)
                if f.endswith('.json') and f != 'config.json'
            ]
            if not json_files:
                print('No JSON files found in the directory.')
            else:
                selected_json_file = json_files[0]
            try:
                CLIENT_SECRET_FILE = os.path.join(directory_path, selected_json_file)
            except:pass
            API_SERVICE_NAME = 'gmail'
            API_VERSION = 'v1'
            SCOPES = ['https://mail.google.com/']
            cred = None
            working_dir = os.getcwd()
            token_dir = 'token_files'
            pickle_file = f'{IspUser.email}.pickle'
            script_dir = os.path.dirname(os.path.abspath(__file__))
            token_access = os.path.join(script_dir + '/token_files', IspUser.email)
            profiel = os.path.join(script_dir + '/profiles', IspUser.email)

            if IspUser.host== None:
                IspUser.host=""
                IspUser.port =""
                IspUser.proxyUser=""
                IspUser.proxyPass =""
            elif IspUser.proxyUser ==None:
                IspUser.proxyUser=""
                IspUser.proxyPass=""


            if not os.path.exists(os.path.join(working_dir, token_dir)):
                os.mkdir(os.path.join(working_dir, token_dir))

            if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
                with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                    try:
                        cred = pickle.load(token)
                    except:
                        pass

            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    try:
                        cred.refresh(Request())
                    except:
                        port = random.randint(1024, 50999)
                        State = generate_random_string2(30)
                        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, state=State,
                                                                        redirect_uri=f"http://localhost:{port}/",
                                                                        autogenerate_code_verifier=False)
                        url, state = flow.authorization_url()
                        url = base64.b64encode(url.encode())
                        
                        subprocess.Popen([sys.executable, os.path.join(script_dir, 'allow_auth.py'), url,IspUser.email, IspUser.password, IspUser.recovery, IspUser.host, IspUser.port, IspUser.proxyUser, IspUser.proxyPass])
                        try:
                            cred = flow.run_local_server(port=port, open_browser=False, timeout_seconds=120)
                        except Exception as e:
                            pass
                elif not os.path.exists(token_access):
                    port = random.randint(1024, 50999)
                    State = generate_random_string2(30)
                    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, state=State,
                                                                    redirect_uri=f"http://localhost:{port}/",
                                                                    autogenerate_code_verifier=False)
                    url, state = flow.authorization_url()
                    url = base64.b64encode(url.encode())
                    try:
                        subprocess.Popen([sys.executable, os.path.join(script_dir, 'allow_auth.py'),  url,IspUser.email, IspUser.password, IspUser.recovery, IspUser.host, IspUser.port, IspUser.proxyUser, IspUser.proxyPass])
                    except Exception as e:
                        print(e)
                    try:
                        cred = flow.run_local_server(port=port, open_browser=False, timeout_seconds=120)
                    except Exception as e:
                        pass
                with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
                    pickle.dump(cred, token)

            try:
                service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
                print(API_SERVICE_NAME, API_VERSION, f'service created successfully for: {IspUser.email}')

            except Exception as e:
                save_to_files("log",e.args[0]+"\n")
                print(f'Failed to create service instance for {API_SERVICE_NAME} for {IspUser.email}')
                os.remove(os.path.join(working_dir, token_dir, pickle_file))
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
    
    @classmethod
    def api_call(cls):
        os.system("python manage.py runserver 0.0.0.0:8000")

    @classmethod
    def change_theme(cls, driver):
        try:
            driver.find_element(By.CSS_SELECTOR, "a[aria-label='Settings']").click()
            time.sleep(random.uniform(3, 5))
            target_element  = driver.find_element(By.CSS_SELECTOR, "img[src='//ssl.gstatic.com/ui/v1/icons/mail/quicksettings/inboxtype/Unreadfirst.png']")
            target_element.click()
            time.sleep(random.uniform(1, 3))
            driver.find_element(By.CSS_SELECTOR, "button[jsname='JFZqac']").click()
            time.sleep(random.uniform(4, 5))
            imgs = driver.find_elements(By.CSS_SELECTOR, "div[class='a7H']")
            clickable_imgs = []
            for img in imgs:
                try:
                    if img.is_displayed() and img.is_enabled():
                        clickable_imgs.append(img)
                except:
                    continue 
            if clickable_imgs:
                random.choice(clickable_imgs).click()

            time.sleep(random.uniform(1, 3))
            driver.find_element(By.CSS_SELECTOR, "button[class*='mUIrbf-I mUIrbf-I-ql-Uw eV8l8d']").click()
            time.sleep(10)
        except:pass
        

    @classmethod
    def check_emails_api(cls, IspUser):
        try:
            print(f"Auth from {IspUser.email} in process ...")
            cred = None
            working_dir = os.getcwd()
            token_dir = 'token_files'
            pickle_file = f'{IspUser.email}.pickle'
            script_dir = os.path.dirname(os.path.abspath(__file__))
            token_access = os.path.join(script_dir + '/token_files', IspUser.email)
            profiel = os.path.join(script_dir + '/profiles', IspUser.email)

            if IspUser.host== None:
                IspUser.host=""
                IspUser.port =""
                IspUser.proxyUser=""
                IspUser.proxyPass =""
            elif IspUser.proxyUser ==None:
                IspUser.proxyUser=""
                IspUser.proxyPass=""


            if not os.path.exists(os.path.join(working_dir, token_dir)):
                os.mkdir(os.path.join(working_dir, token_dir))

            if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
                with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                    try:
                        cred = pickle.load(token)
                    except:
                        pass

            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    try:
                        cred.refresh(Request())
                        save_to_files("ok", IspUser.showString())
                    except:
                        save_to_files("not_ok", IspUser.showString())
                elif not os.path.exists(token_access):
                    save_to_files("not_ok", IspUser.showString())
        except Exception as e:
            save_to_files("not_ok", IspUser.showString())

    @classmethod
    def confirm_from(cls,driver,nbmsgs):
            cls.search(driver)
            cls.openMsg(driver)
            for i in range(nbmsgs):
                try:
                    driver.find_elements(By.CSS_SELECTOR,"a[rel='noreferrer']")[0].click()
                    time.sleep(0.5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
                    time.sleep(0.5)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    cls.nextMsg(driver)
                except:pass
            driver.quit()
        
    @classmethod
    def remove_phone(cls,driver, ispUser):
        try:
            driver.get("https://myaccount.google.com/signinoptions/rescuephone")
            cls.enter_password(driver, ispUser.password)
            cls.handle_otp(driver, ispUser)
            nb = driver.find_elements(By.CSS_SELECTOR, "button[class='pYTkkf-Bz112c-LgbsSe wMI9H Qd9OXe']")
            if nb:
                try:
                    if len(nb)>2:
                        nb[2].click()
                    else:
                        nb[1].click()
                except:pass
            
                confirmbtn = driver.find_elements(By.CSS_SELECTOR, "div[class='U26fgb O0WRkf oG5Srb HQ8yf C0oVfc kHssdc HvOprf FsOtSd M9Bg4d']")
                if confirmbtn:
                    try:
                        if len(confirmbtn)>1:
                            confirmbtn[1].click()
                            save_to_files("phone_removed", ispUser.showString())
                            
                        else:
                            confirmbtn[0].click()
                            save_to_files("phone_removed", ispUser.showString())
                    except:pass
            time.sleep(3)

        except:pass

    @classmethod
    def prepareAccount(cls, IspUser, driver):
        cls.checkAccount(IspUser, driver)
        try:
            if driver.title:
                cls.changePasswordRecovry(IspUser, driver)
                cls.twoFactourAuth(IspUser, driver)
                cls.activatetwoFactour(IspUser, driver)
        except:return

    @classmethod
    def app_script(cls, driver, IspUser):
        try:
            driver.get("https://script.google.com/home")
            otp = cls.handle_otp(driver,IspUser.email)
            time.sleep(1)
            try:
                driver.find_element(By.CSS_SELECTOR,"div[class='U26fgb O0WRkf zZhnYe C0oVfc XBU8lb M9Bg4d']").click()
            except:pass
            driver.find_element(By.CSS_SELECTOR,"button[class='VfPpkd-BIzmGd VfPpkd-BIzmGd-OWXEXe-X9G3K bgpk6e gl6QPb']").click()
            editor = driver.find_element(By.CSS_SELECTOR, "div.view-lines")
            with open("ressources/appscript.txt", "r", encoding="utf-8") as file:
                script_content = file.readlines()

            script_content = ''.join(script_content)
            escaped_script = script_content.replace("\\", "\\\\").replace("`", "\\`")

            editor.click()
            js_script = f"""
                let editor = monaco.editor.getModels()[0];
                editor.setValue(`{escaped_script}`);
                """
            driver.execute_script(js_script)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"div[class='U26fgb c7fp5b JvtX2e rGMe1e Gn5yxe']").click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH,"/html/body/div[14]/div/div/span[1]").click()
            except:
                driver.find_element(By.XPATH,"/html/body/div[13]/div/div/span[1]").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"div[class='U26fgb JRtysb WzwrXb yKcM7c']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[@id='yDmH0d']/div[4]/div[2]/div/div/div[2]/div/div/span[1]").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[@id='c9']").send_keys(generate_random_string2(6))
            
            dropdown_toggle = driver.find_element(By.XPATH, "//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[4]/div/div/div[1]")
            dropdown_toggle.click()

            time.sleep(1)
            anyone_option = driver.find_element(By.XPATH, "//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[4]/div/div/div[2]/ul/li[3]")
            anyone_option.click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div[2]/div[4]/button").click()
            time.sleep(10)
            driver.find_element(By.XPATH,"//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div[1]/div/div/div/div[2]/button").click()
            original_window = driver.current_window_handle
            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break
            driver.find_element(By.XPATH,"//*[@id='yDmH0d']/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"a[class='xTI6Gf vh6Iad']").click()
            driver.find_elements(By.CSS_SELECTOR,"a[class='xTI6Gf vh6Iad']")[1].click()
            time.sleep(1)
            driver.find_elements(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf']")[1].click()
            driver.switch_to.window(original_window)
            time.sleep(5)
            element = driver.find_elements(By.CSS_SELECTOR, "div[jsaction='JIbuQc:jCCvxc']")[1]
            value = element.get_attribute("data-txt")
            file_path = "ressources/deployment_id.json"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            data[IspUser.email] = value

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            time.sleep(2)
            driver.quit()
        except Exception as e :
            driver.quit()
                

def generate_random_string2(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


class HotmailActions():
    
    def urls():
        LoginUrl = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1707744265&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26deeplink%3dowa%252f0%252f%253fstate%253d1%26redirectTo%3daHR0cHM6Ly9vdXRsb29rLmxpdmUuY29tL21haWwvMC8%26RpsCsrfState%3d09d06961-57fc-31bf-932b-46cd145a6aa3&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c"
        MainUrl = "https://outlook.live.com/mail/0/"
        SpamUrl = "https://outlook.live.com/mail/0/junkemail"
        ContactUrl = "https://outlook.live.com/people/0/"
        ArchiveUrl = "https://outlook.live.com/mail/0/archive"
        urlPro = "https://account.microsoft.com/"
        office = 'https://outlook.office365.com/mail/'
        url_list = [MainUrl, ContactUrl, SpamUrl, ArchiveUrl,urlPro,office]
        return url_list

    @classmethod
    def read_file(cls, filename):
        try:
            # Get the current working directory using os.getcwd()
            folder = "ressources"
            actsPath = os.path.join(folder, filename)
            # Concatenate the file name to the current working directory to form the absolute file path
            with open(actsPath, 'r') as file:
                data = file.read().splitlines()
                return data
        except:
            print(f"File {filename} not found.")
            return None

    @classmethod
    def close_secend_window(cls, driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    def checkAccount(IspUser, driver, close = False):
        print(IspUser.email+' on process...')
        logUrl = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708442704&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26deeplink%3dowa%252f%26RpsCsrfState%3d65d04c9c-21c5-309e-2c28-5482fe0bc4f6&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c"
        driver.get(logUrl)
        time.sleep(3)
        currentUrl = driver.current_url
        url_list = HotmailActions.urls()
        currentUrl = currentUrl.split('?')[0]
        if currentUrl in url_list:
            if close:
                save_to_files("ok", IspUser.showString())
                driver.quit()
            time.sleep(3)
            #baner choice
            try:
                driver.find_elements(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--primary E8L0k root']")[1].click()
            except:pass

            #acceptAll
            try:
                driver.find_elements(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--primary EpKAV root']")[1].click()
            except:pass
        else:
            createProfiles.login_to_hotmail(IspUser, driver , close)

    @classmethod
    def openMsg(cls, driver, i=0):
        try:
            driver.implicitly_wait(3)
            rows =driver.find_elements(By.CSS_SELECTOR,'div[class="ESO13 gy2aJ Ejrkd"],div[class*="IjzWp"]')[i]
            rows.click()
            time.sleep(random.randint(3, 6))
            driver.implicitly_wait(10)
        except:pass

    @classmethod
    def loginWait(cls, IspUser, driver):
        cls.checkAccount(IspUser, driver, False )
        while True:
            try:
                currentUrl = driver.current_url
            except:
                driver.quit()
                break
    
    @classmethod
    def goToJunk(cls, driver):
        try:
            spamUrl = "https://outlook.live.com/mail/0/junkemail"
            driver.get(spamUrl)
            driver.refresh()
            time.sleep(random.randint(5, 8))
        except:pass
    
    @classmethod  
    def NotJunk(cls, driver):
        driver.find_elements(By.CSS_SELECTOR,"button[class*='ms-Button splitMenuButton splitButtonMenuButton']")[2].click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.CSS_SELECTOR,"button[class*='root-'][tabindex='-1'][role='menuitem']").click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.CSS_SELECTOR,"button[class*='fui-Button r1alrhcs ___1akj6hk']").click()
        time.sleep(random.randint(3, 5))
    
    @classmethod  
    def moveToInbox(cls, driver):
        driver.find_element(By.CSS_SELECTOR,"button[aria-label='Déplacer vers'],button[aria-label='Move to']").click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.CSS_SELECTOR,"button[name='Inbox']").click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--primary jya0z root-']").click()
        time.sleep(random.randint(3, 5))

    @classmethod  
    def reportNotJunk(cls, driver):
        cls.goToJunk(driver)
        cls.search(driver)
        while True:
            try:
                cls.openMsg(driver)
                cls.NotJunk(driver)
            except:break
    
    @classmethod  
    def reportToInbox(cls, driver):
        cls.goToJunk(driver)
        cls.search(driver)
        while True:
            try:
                cls.openMsg(driver)
                cls.moveToInbox(driver)
            except:break
    
    @classmethod
    def selectPage(cls, driver):
        # Get scroll height
        lastMsg=''
        while True:
            selectMsg = driver.find_elements(By.CSS_SELECTOR,"div[role='checkbox'][tabindex='-1']")[-1]
            if lastMsg == selectMsg:
                break
            else:
                lastMsg = selectMsg
                selectMsg.location_once_scrolled_into_view
                time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--icon G9d_n']").click()
        time.sleep(random.randint(3, 5))
        selectAll = driver.find_element(By.CSS_SELECTOR,"div[class*='ms-Checkbox is-enabled JV_Om']")
        selectAll.click()
        time.sleep(random.randint(3, 5))

    @classmethod 
    def selectPage_notJunk(cls, driver):
        cls.goToJunk(driver)
        #cls.search(driver)
        while True:
            try:
                cls.selectPage(driver)
                cls.NotJunk(driver)
            except:break

    
    @classmethod
    def nextMsg(cls, driver):
        try:
            nextBtn = driver.find_elements(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--icon xoRaD']")
            if len(nextBtn)>1:
                nextBtn[1].click()
            else:
                nextBtn[0].click()
            time.sleep(random.randint(3, 6))
        except:pass

    @classmethod
    def click(cls, driver):
        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
            largest_image = None
            largest_area = 0
            for img in image_elements:
                width = int(img.get_attribute("width") or 0)
                height = int(img.get_attribute("height") or 0)
                area = width * height

                if area > largest_area:
                    largest_area = area
                    largest_image = img
            if largest_area != 1024:
                largest_image.click()
            time.sleep(2)
            if len(driver.window_handles)>1:
                time.sleep(random.randint(4, 6))
                cls.close_secend_window(driver)
                time.sleep(random.randint(1, 2))
            wrong_img=None
            wrong_img = driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-aPU-JX')
            if wrong_img:
                time.sleep(random.randint(1, 2))
                back_btn= driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-Jq-I.aLF-aPX-auO-I.J-J5-Ji.aLF-aPX-I')
                back_btn.click()

        except:pass
    
    @classmethod
    def archive(cls, driver):
        try:
            archiveBtn = driver.find_elements(By.CSS_SELECTOR, "Button[class*='ms-Button root']")[3]
            archiveBtn.click()
            time.sleep(random.randint(2, 5))
        except:pass
    @classmethod
    def removePin(cls, driver):
        while True:
            try:
                pinBtn = driver.find_element(By.CSS_SELECTOR, "i[data-icon-name='PinFilled']")
                pinBtn.click()
                time.sleep(random.randint(1, 3))
            except:break
    
    @classmethod
    def Categorize(cls, driver):
        try:
            CategoriBtn = driver.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label*='Cat']")
            CategoriBtn.click()
            time.sleep(random.randint(2, 5))
            BlueBtn = driver.find_elements(By.CSS_SELECTOR, "button[name*='Blue'], button[name*='Bleu']")
            GreenBtn = driver.find_elements(By.CSS_SELECTOR, "button[name*='Green'],button[name*='Vert']")
            random_color = random.choice([BlueBtn, GreenBtn])
            random_color[0].click()
            time.sleep(random.randint(2, 5))
        except:pass
    @classmethod
    def flag(cls, driver):
        try:
            flagBtn = driver.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label*='Flag']")
            flagBtn.click()
            time.sleep(random.randint(2, 5))
        except:pass

    @classmethod
    def inbox_openClick(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def inbox_openCategorize(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.Categorize(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openFlag(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.flag(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openArchive(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.archive(driver)
            except:break

    @classmethod
    def inbox_openReply(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.reply(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openClickCategorize(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.Categorize(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def inbox_openClickCategorizeFlag(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.Categorize(driver)
                cls.flag(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def inbox_openClickCategorizeArchive(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.Categorize(driver)
                cls.archive(driver)
            except:break
    
    @classmethod
    def reply(cls, driver):
        try:
            replys = cls.read_file("replys.txt")
            if replys:
                replyMsg = random.choice(replys)
            else:
                replyMsg = generate_random_string()
            replyBtn = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Répondre'],button[aria-label='Reply']")[0]
            replyBtn.click()
            time.sleep(random.randint(2, 5))
            reply_input = driver.find_element(By.CSS_SELECTOR, "div[role='textbox'][tabindex='0']")
            reply_input.clear()
            reply_input.send_keys(replyMsg)
            time.sleep(random.randint(2, 5))
            send_reply = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Envoyer'],button[aria-label='Send']")
            send_reply.click()
            time.sleep(random.randint(2, 5))
        except:pass

    @classmethod
    def inbox_openClickCategorizeReply(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.Categorize(driver)
                cls.reply(driver)
                cls.nextMsg(driver)
            except:pass
        
    @classmethod
    def inbox_openClickReplyArchive(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.reply(driver)
                cls.archive(driver)
            except:pass
    
    @classmethod
    def inbox_openClickReplyFlag(cls, driver, nbMsgs):
        cls.search(driver)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.reply(driver)
                cls.flag(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def archive_openFlag(cls, driver, nbMsgs):
        archiveUrl= "https://outlook.live.com/mail/0/archive"
        driver.get(archiveUrl)
        time.sleep(5)
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.flag(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def importContact(cls, IspUser, driver):
        try:
            current_project_path = os.getcwd()
            try:
                file_path = current_project_path+"\\ressources\\contacts.csv"
            except:pass
            while True:
                try:
                    contact_url='https://outlook.live.com/people/0/'
                    driver.get(contact_url)
                    time.sleep(3)
                except:pass
                while True:
                    try:
                        manageBtn = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Gérer les contacts'],Button[aria-label='Manage contacts']")
                        manageBtn.click()
                        time.sleep(1)
                        try:
                            importOpt = driver.find_element(By.CSS_SELECTOR,"button[name*='Import']")
                            importOpt.click()
                            time.sleep(random.randint(3, 5))
                            break
                        except:pass
                    except:pass
                try:
                    file_input = driver.find_element(By.XPATH,"//input[@type='file']")
                    file_input.send_keys(file_path)
                    time.sleep(random.randint(3, 5))
                except:pass
                try:
                    span = driver.find_element(By.XPATH,"//span[contains(text(), 'contacts.csv')]")
                    if span:
                        parent = driver.find_element(By.CSS_SELECTOR,"div[class='jtWOl']")
                        importBtn = parent.find_element(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--primary']")
                        importBtn.click()
                        save_to_files("add_contact_done", IspUser.showString())
                        time.sleep(random.randint(3, 5))
                        break
                except:pass
        except:
            save_to_files("add_contact_failed", IspUser.showString())
        
    @classmethod
    def changePassword(cls, IspUser, driver):
        try:
            cls.checkAccount(IspUser, driver)
            new_password = IspUser.newPassword
            old_password = IspUser.password
            if new_password == None:
                print("syntax incorrect: To change password pls follow this sayntax password:::newpassword")
            else:
                driver.get("https://account.live.com/password/Change?mkt=fr-FR&refd=account.microsoft.com&refp=profile")
                try:
                    time.sleep(random.randint(1, 3))
                    pwdInput = driver.find_element(By.CSS_SELECTOR,"input[name='passwd']")
                    pwdInput.send_keys(Keys.CONTROL + "a")
                    # Use DELETE to delete the selected text uz clear nt clear saved Cookies
                    pwdInput.send_keys(Keys.DELETE)
                    pwdInput.send_keys(old_password)
                    time.sleep(random.randint(1, 3))
                    nextBtn = driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='submit']")
                    nextBtn.click()
                except:pass
                try:
                    mailPart = getFirstPart(IspUser.email)
                    time.sleep(random.randint(1, 3))
                    EmailBtn = driver.find_element(By.CSS_SELECTOR,"div[role='button']")
                    time.sleep(1)
                    EmailBtn.click()
                    email= driver.find_element(By.CSS_SELECTOR, 'input[id*="idTxtBx"]')
                    email.send_keys(Keys.CONTROL + "a")
                    # Use DELETE to delete the selected text uz clear nt clear saved Cookies
                    email.send_keys(Keys.DELETE)
                    secendpart = getFirstPart(IspUser.recovery, True)
                    email.send_keys(f"{mailPart}@{secendpart}")
                    time.sleep(random.randint(1, 3))
                    sendBtn = driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='submit']")
                    sendBtn.click()
                    if secendpart == "mailforspam.com":
                        fact = mailforspam(driver, mailPart)
                    else:
                        fact = mainlnesia(driver, mailPart)
                    if not fact:
                        save_to_files("recovery-wrong",IspUser.showString())
                        driver.quit()
                    
                    try:
                        continueBtn = driver.find_element(By.CSS_SELECTOR,"button[type='button']")
                        continueBtn.click()
                        time.sleep(random.randint(1, 3))
                    except:pass
                    try:
                        notNow = driver.find_element(By.CSS_SELECTOR,"a[id='iCancel']")
                        notNow.click()
                        time.sleep(random.randint(1, 3))
                    except:pass
                except:pass
                time.sleep(random.randint(1, 3))
                password_fields = driver.find_elements(By.CSS_SELECTOR,"input[type='password']")
                time.sleep(random.randint(2, 3))
                password_fields[0].send_keys(old_password)
                time.sleep(random.randint(2, 3))
                password_fields[1].send_keys(new_password)
                time.sleep(random.randint(2, 3))
                password_fields[2].send_keys(new_password)
                time.sleep(random.randint(2, 3))
                submitBtn = driver.find_element(By.CSS_SELECTOR,"input[type='submit']")
                submitBtn.click()
                time.sleep(random.randint(3, 5))
                save_to_files("password_changed",IspUser.showString())
        except:
            save_to_files("password_NotChanged",IspUser.showString())
    
    @classmethod
    def createFilter(cls, driver):
        pass

    @classmethod
    def cleanAll(cls, driver):
        while True:
            try:
                cls.selectPage(driver)
                deletBtn = driver.find_elements(By.CSS_SELECTOR,"button[class*='splitPrimaryButton root']")[1]
                deletBtn.click()
                time.sleep(1)
                okBtn = driver.find_element(By.CSS_SELECTOR,"button[class*='ms-Button ms-Button--primary jya0z root-']")
                okBtn.click()
            except:
                break
    
    @classmethod
    def search(cls, driver):
        try:
            seachkey = cls.read_file("search.txt")
            if seachkey:
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR,"input[class*='uz227']")
                    search_input.send_keys(seachkey)
                    search_input.send_keys(Keys.RETURN)
                    time.sleep(random.randint(1, 4))
                except:pass
        except:
            print("search.txt not exist")
    
    @classmethod
    def actionByChoice(cls, IspUser, driver, nbMsgs):
        acts_filename="actions.txt"
        acts_list = cls.read_file(acts_filename)
        cat, acts_func = acts_list[0].split(":")
        acts_func = acts_func.split(";")

        if acts_func =="changePassword":
            cls.changePassword(IspUser, driver)
        elif acts_func =="importContact":
            cls.importContact(IspUser, driver)
        elif acts_func =="clean":
            cls.cleanAll(IspUser, driver)
        elif acts_func =="checkAccount" or acts_func =="createProfiles":
            cls.checkAccount(IspUser, driver)
        else:
            if acts_func:
                instance = HotmailActions()
                if cat =="spam":
                    cls.goToJunk(driver)
                    driver.refresh()
                for i in range(nbMsgs):
                    for act in acts_func:
                        method  = getattr(HotmailActions, act, None)

                        # Check if the function exists
                        if method and callable(method) and hasattr(method, '__self__') and method.__self__ is HotmailActions:
                            # Call the class method with the driver parameter
                            method(driver)
                        else:
                            save_to_files('log',f"Function '{act}' not found or not callable.")
    
    @classmethod
    def randomActions(cls, driver, nbMsgs):
        function_data = [
            (cls.click, [driver]),
            (cls.Categorize, [driver]),
            (cls.flag, [driver]),
            (cls.reply, [driver]),
            (cls.archive, [driver])
        ]

        for _ in range(nbMsgs):
            cls.openMsg(driver)
            
            # Randomly determine the number of functions to select (between 1 and the total number of functions)
            num_functions_to_select = random.randint(1, len(function_data))

            # Randomly select the specified number of UNIQUE functions with their respective arguments
            selected_functions = random.sample(function_data, k=num_functions_to_select)

            # Execute the selected functions
            for selected_function, args in selected_functions:
                selected_function(*args)

            cls.nextMsg(driver)
    


class YahooActions():
    def urls():



        LoginUrl = "https://login.yahoo.com/"
        MainUrl = "https://mail.yahoo.com/"
        url_list = [MainUrl]
        return url_list

    @classmethod
    def read_file(cls, filename):
        try:
            # Get the current working directory using os.getcwd() 
            folder = "ressources"
            actsPath = os.path.join(folder, filename)
            # Concatenate the file name to the current working directory to form the absolute file path
            with open(actsPath, 'r') as file:
                data = file.read().splitlines()
                return data
        except:
            print(f"File {filename} not found.")
            return None

    @classmethod
    def close_secend_window(cls, driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    
    @classmethod
    def checkAccount(cls,IspUser, driver, close = False):
        print(IspUser.email+' on process...')
        driver.get("https://mail.yahoo.com/")
        time.sleep(3)
        currentUrl = driver.current_url
        
        separators = ['d/folders']
        if 'd/folders' in currentUrl:
            save_to_files("ok", IspUser.showString())
            if close:
                driver.quit()
            else:
                return
        else:
            createProfiles.login_to_yahoo(IspUser, driver)

    @classmethod
    def openMsg(cls, driver, i=0):
        driver.implicitly_wait(3)
        rows =driver.find_elements(By.CSS_SELECTOR,'div[class*="D_F r_P a"]')[i]
        rows.click()
        time.sleep(0.5)
        driver.implicitly_wait(10)

    @classmethod
    def loginWait(cls, driver):
        while True:
            try:
                currentUrl = driver.current_url
            except:
                driver.quit()
                break
    
    @classmethod
    def goToSpam(cls, driver):
        spamUrl = "https://mail.yahoo.com/d/folders/6"
        driver.get(spamUrl)
        driver.refresh()
        time.sleep(random.randint(2, 4))
    
    @classmethod  
    def NotSpam(cls, driver):
        driver.find_element(By.CSS_SELECTOR,"button[aria-label*='spam'], button[aria-label*='légitime']").click()
        time.sleep(random.randint(3, 5))
    
    @classmethod  
    def reportNotSpam(cls, driver):
        cls.goToSpam(driver)
        while True:
            try:
                cls.openMsg(driver)
                cls.NotSpam(driver)
            except:break
    
    @classmethod
    def selectPage(cls, driver):
        driver.find_element(By.CSS_SELECTOR,"button[tabindex='30']").click()
        time.sleep(random.randint(3, 5))

    @classmethod 
    def selectPage_notSpam(cls, driver):
        cls.goToSpam(driver)
        while True:
            try:
                cls.selectPage(driver)
                cls.NotSpam(driver)
            except:break
        
    @classmethod
    def click(cls, driver):
        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
            largest_image = None
            largest_area = 0
            for img in image_elements:
                width = int(img.get_attribute("width") or 0)
                height = int(img.get_attribute("height") or 0)
                if width >32:
                    area = width * height

                if area > largest_area:
                    largest_area = area
                    largest_image = img
            largest_image.click()
            if len(driver.window_handles)>1:
                time.sleep(random.randint(5, 8))
                cls.close_secend_window(driver)
                time.sleep(random.randint(1, 2))
            wrong_img=None
            wrong_img = driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-aPU-JX')
            if wrong_img:
                time.sleep(random.randint(1, 2))
                back_btn= driver.find_element(By.CSS_SELECTOR, '.aLF-aPX-Jq-I.aLF-aPX-auO-I.J-J5-Ji.aLF-aPX-I')
                back_btn.click()

        except:pass
    
    @classmethod
    def archive(cls, driver):
        try:
            archiveBtn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Archiv' i]").click()
            time.sleep(random.randint(2, 5))
        except:pass
    
    @classmethod
    def star(cls, driver):
        try:
            driver.find_element(By.CSS_SELECTOR, "button[data-test-id*='star'],button[data-test-id*='étoile']").click()
            time.sleep(random.randint(2, 5))
        except:pass
    
    @classmethod
    def nextMsg(cls, driver):
        try:
            driver.find_element(By.CSS_SELECTOR, "button[data-test-id*='next'],button[data-test-id*='suivante']").click()
            time.sleep(0.5)
        except:pass

    @classmethod
    def inbox_openClick(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def inbox_openClickStar(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.star(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def inbox_openClickArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:break
    
    @classmethod
    def reply(cls, driver):
        try:
            replys = cls.read_file("replys.txt")
            if replys:
                replyMsg = random.choice(replys)
            else:
                replyMsg = generate_random_string()
            replyBtn = driver.find_elements(By.CSS_SELECTOR, "button[data-kind*='reply']")[0]
            replyBtn.click()
            time.sleep(random.randint(2, 5))
            reply_input = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
            reply_input.clear()
            reply_input.send_keys(replyMsg)
            time.sleep(random.randint(2, 5))
            send_reply = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='compose-send-button']")
            send_reply.click()
            time.sleep(random.randint(2, 5))
        except:pass

    @classmethod
    def inbox_openReply(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.reply(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openStar(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.star(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:break

    @classmethod
    def inbox_openClickReply(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.reply(driver)
                cls.nextMsg(driver)
            except:break
        
    @classmethod
    def inbox_openClickReplyArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver)
                cls.click(driver)
                cls.reply(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:break
            
    @classmethod
    def inbox_openClickStarReply(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.star(driver)
                cls.reply(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_openClickStarArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.star(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_openClickStarReplyArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.click(driver)
                cls.star(driver)
                cls.reply(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_openStarReplyArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.star(driver)
                cls.reply(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_openReplyArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.reply(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_openStarArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.star(driver)
                cls.archive(driver)
                cls.nextMsg(driver)
            except:pass

    @classmethod
    def inbox_allArchive(cls, driver, nbMsgs):
        for i in range(nbMsgs):
            try:
                cls.openMsg(driver, i)
                cls.selectPage(driver)
                cls.archive(driver)
            except:pass


    @classmethod
    def importContact(cls, IspUser, driver):
        try:
            current_project_path = os.getcwd()
            file_path = current_project_path+"\\ressources\\contacts.csv"
            try:
                time.sleep(3)
                ContatsBtn = driver.find_element(By.CSS_SELECTOR,"button[title*='Contact' i]")
                ContatsBtn.click()
                time.sleep(1)
                file_input = driver.find_element(By.XPATH,"//input[@type='file']")
                file_input.send_keys(file_path)
                time.sleep(random.randint(5, 8))
                save_to_files("add_contact_done", IspUser.showString())
            except:pass
        except:
            save_to_files("add_contact_failed", IspUser.showString())
        
    @classmethod
    def changePassword(cls, IspUser, driver):
        try:
            cls.checkAccount(IspUser, driver)
            new_password = IspUser.newPassword
            old_password = IspUser.password
            if new_password == None:
                print("syntax incorrect: To change password pls follow this sayntax password:::newpassword")
            else:
                driver.get("https://login.yahoo.com/account/security?.intl=us&.lang=en-US&.done=https%3A%2F%2Fwww.yahoo.com%2F")
                try:
                    time.sleep(random.randint(1, 3))
                    email= driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
                    email.clear()
                    email.send_keys(IspUser.email)
                    time.sleep(2)
                    nextBtn= driver.find_element(By.CSS_SELECTOR, "input[type='submit'],button[type='submit']")
                    nextBtn.click()
                    time.sleep(random.randint(3, 5))
                    pwd = driver.find_element(By.CSS_SELECTOR, 'input[class="password"]')
                    pwd.send_keys(Keys.CONTROL + "a")
                    # delete the selected text uz clear nt clear saved Cookies
                    pwd.send_keys(Keys.DELETE)
                    pwd.send_keys(old_password)
                    time.sleep(2)
                    time.sleep(random.randint(1, 3))
                    nextBtn = driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='submit']")
                    nextBtn.click()
                except:pass
                time.sleep(random.randint(1, 3))
                driver.find_elements(By.CSS_SELECTOR,"a[class='idc-action']")[0].click()
                pwdInput = driver.find_element(By.CSS_SELECTOR,"input[id='createNPwdTxtField']")
                pwdInput.send_keys(Keys.CONTROL + "a")
                # Use DELETE to delete the selected text uz clear nt clear saved Cookies
                pwdInput.send_keys(Keys.DELETE)
                pwdInput.send_keys(new_password)
                time.sleep(random.randint(1, 3))
                nextBtn = driver.find_element(By.CSS_SELECTOR,"button[class*='btn btn-primary']")
                nextBtn.click()
                save_to_files("password_changed",IspUser.showString())   
        except:
            save_to_files("password_NotChanged",IspUser.showString())
    
    @classmethod
    def cleanAll(cls, driver):
        while True:
            try:
                cls.selectPage(driver)
                deletBtn = driver.find_element(By.CSS_SELECTOR,"button[data-test-id='toolbar-delete']")
                deletBtn.click()
                time.sleep(5)
            except:
                break

    @classmethod
    def actionByChoice(cls, IspUser, driver, nbMsgs):
        acts_filename="actions.txt"
        acts_list = cls.read_file(acts_filename)
        cat, acts_func = acts_list[0].split(":")
        acts_func = acts_func.split(";")

        if acts_func =="changePassword":
            cls.changePassword(IspUser, driver)
        elif acts_func =="changeRecovry":
            cls.changeRecovery(IspUser, driver)
        elif acts_func =="changePasswordRecovry":
            cls.changePasswordRecovery(IspUser, driver)
        elif acts_func =="importContact":
            cls.importContact(IspUser, driver)
        elif acts_func =="clean":
            cls.cleanAll(IspUser, driver)
        elif acts_func =="checkAccount" or acts_func =="createProfiles":
            cls.checkAccount(IspUser, driver)
        else:
            if acts_func:
                instance = YahooActions()
                if cat =="spam":
                    cls.goToSpam(driver)
                for i in range(nbMsgs):
                    for act in acts_func:
                        method  = getattr(YahooActions, act, None)

                        # Check if the function exists
                        if method and callable(method) and hasattr(method, '__self__') and method.__self__ is YahooActions:
                            # Call the class method with the driver parameter
                            method(driver)
                        else:
                            save_to_files('log',f"Function '{act}' not found or not callable.")

    @classmethod
    def randomActions(cls, driver, nbMsgs):
        function_data = [
            (cls.click, [driver]),
            (cls.star, [driver]),
            (cls.reply, [driver]),
            (cls.archive, [driver])
        ]

        for _ in range(nbMsgs):
            cls.openMsg(driver)
            
            # Randomly determine the number of functions to select (between 1 and the total number of functions)
            num_functions_to_select = random.randint(1, len(function_data))

            # Randomly select the specified number of UNIQUE functions with their respective arguments
            selected_functions = random.sample(function_data, k=num_functions_to_select)

            # Execute the selected functions
            for selected_function, args in selected_functions:
                selected_function(*args)

            cls.nextMsg(driver)