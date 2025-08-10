import random, time
from EmailClient import save_to_files
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
import requests, os
from EmailClient import get_config
import re
from datetime import datetime
import json
import time
import pyotp, string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


sms_api_key, sms_activate_url, crt_code,_,_,_,captcha_api_key = get_config()

def save_data_to_list(login_data):
    try:
        data=""
        if login_data["newpassword"] !=None and login_data["newrecovery"] !=None:
            data = f'{login_data["email"]};{login_data["password"]}###{login_data["newpassword"]};{login_data["ip"]};{login_data["port"]};{login_data["recovery"]}###{login_data["newrecovery"]}\n'
            return data
    except:pass
    try:
        if login_data["newpassword"] !=None:
            data = f'{login_data["email"]};{login_data["password"]}###{login_data["newpassword"]};{login_data["ip"]};{login_data["port"]};{login_data["recovery"]}\n'
            return data
    except:pass
    try:
        if login_data["newrecovery"] !=None:
            data = f'{login_data["email"]};{login_data["password"]};{login_data["ip"]};{login_data["port"]};{login_data["recovery"]}###{login_data["newrecovery"]}\n'
            return data
    except:pass
    try:
        data = f'{login_data["email"]};{login_data["password"]};{login_data["ip"]};{login_data["port"]};{login_data["recovery"]}\n'
        return data
    except:pass

def solve_captcha(driver,url,isp='', IspUser =''):
    try:
        api_key = captcha_api_key
        #api_key = '5a023e6086a61a3a7c35acf295ac713f'
        # driver.execute_script("window.open('');")
        if url =="check":
            solver = TwoCaptcha(api_key)
            i=0
            while i<15:
                try:
                    i+=1
                    img = driver.find_element(By.CSS_SELECTOR,'img[src*="Captcha"]')
                    img_src = img.get_attribute('src')
                    result = solver.normal(img_src)
                    code =result['code']
                    driver.find_element(By.CSS_SELECTOR,'input[type="text"]').send_keys(code)
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ ']").click()
                    time.sleep(3)
                    check_url = driver.current_url
                    check_url = check_url.split('?')[0]
                    if check_url =='https://accounts.google.com/v3/signin/challenge/pwd' or check_url=='https://accounts.google.com/signin/v2/challenge/pwd':
                        break
                    if check_url !='https://accounts.google.com/signin/v2/identifier':
                        url ="pass"
                except:
                    break
            if url =="pass":
                result_check_gmail(IspUser, driver,False,True,False,False)
            if url=="check":
                while True:
                    try:
                        pwd = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
                        break
                    except:
                        try:
                            pwd = driver.find_element("xpath", '//input[@type="password" and @name="Passwd"]')
                            break
                        except:
                            pass
                            
        if url !="check":
            #iframe1 = driver.find_element(By.CSS_SELECTOR,"iframe[title='reCAPTCHA']")
            # driver.switch_to.frame(iframe1)
            solved = False
            # driver.find_element(By.CSS_SELECTOR,"span[class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']").click()
            # time.sleep(5)
            # driver.switch_to.default_content()
            # iframe2 = driver.find_element(By.CSS_SELECTOR,"iframe[title*='recaptcha challenge']")
            # driver.switch_to.frame(iframe2)
            # time.sleep(2)
            # driver.find_element(By.CSS_SELECTOR,"div[class='button-holder help-button-holder']").click()
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"div[class='captcha-solver captcha-solver_inner']").click()
            try:
                iframe2 = driver.find_element(By.CSS_SELECTOR,"iframe[title*='recaptcha challenge']")
                driver.switch_to.frame(iframe2)
                driver.find_element(By.CSS_SELECTOR,"div[class='rc-doscaptcha-header-text']")
                save_to_files("recaptcha_try_again_later", IspUser.showString())
                driver.quit()
                return
            except:pass
            
            maxtry=0
            #driver.switch_to.default_content()
            #driver.switch_to.frame(iframe1)
            while True:
                for i in range(30):
                    try:
                        # div = driver.find_element(By.CSS_SELECTOR,"div[id='rc-anchor-container']")
                        # divchild = div.find_element(By.CSS_SELECTOR,"div[id='recaptcha-accessible-status']")
                        # status = divchild.get_attribute("textContent").strip()
                        # if status == "You are verified":
                        #     driver.switch_to.default_content()
                        #     solved= True
                        #     break
                        # time.sleep(10)
                        driver.switch_to.default_content()
                        div = driver.find_element(By.CSS_SELECTOR,"div[class='captcha-solver-info']")
                        if div.text == "Captcha solved!":
                            solved= True
                            break
                        time.sleep(10)
                    except:
                        pass
                if solved:
                    break
                
                elif maxtry==5:
                    driver.quit()
                    save_to_files("recaptcha", IspUser.showString())
                    break
                else:
                    driver.refresh()
                    maxtry =maxtry +1
            time.sleep(1)
            try:
                submit_btn = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"],button[type="button"]')[0]
                submit_btn.click()
                time.sleep(2)
                captchaV2= "https://accounts.google.com/signin/v2/challenge/recaptcha"
                captchaV3= "https://accounts.google.com/v3/signin/challenge/recaptcha"
                current_url = driver.current_url      
                current_url = current_url.split('?', 1)[0]
                if current_url == captchaV2 or current_url == captchaV3:
                    driver.refresh()
            except:pass
            time.sleep(2)
        if isp =='gmail':
            try:
                pwd = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
            except:
                try:
                    pwd = driver.find_element("xpath", '//input[@type="password" and @name="Passwd"]')
                except:
                    pass
            try:
                if pwd:
                    pwd.send_keys(IspUser.password)
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
            except:pass
            try:
                time.sleep(3)
                driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[0].send_keys(IspUser.password+"1")
                time.sleep(1)
                driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[1].send_keys(IspUser.password+"1")
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='button']").click()
                save_to_files("forced_tochangePwd", IspUser.showString())
            except:pass


            try:
                #checking if Password wrong
                pwd_wrong = driver.find_element(By.CSS_SELECTOR,"div[jsname='B34EJ'] span[jsslot='']")
                if pwd_wrong and pwd:
                    save_to_files("wrong_password", IspUser.showString())
                    try:
                        driver.quit()
                    except:pass
                    return True
            except:pass

            #Handling Recovery input
            try:
                otp = False
                recov = driver.find_elements(By.CSS_SELECTOR, "div[role='link'][data-accountrecovery='false']")
                try:
                    for element  in recov:
                        div = element.find_element(By.CSS_SELECTOR, "div[class='l5PPKe']")
                        if "Get a verification code from the" in div.txt or "Confirm your recovery email" in div.txt:
                            otp= True
                            recov.click()
                except:
                    try:
                        secendpart = getFirstPart(IspUser.recovery, True)
                        current_url = driver.current_url
                        current_url = current_url.split('?', 1)[0]
                        if secendpart =="mailforspam.com" and url =='https://accounts.google.com/v3/signin/challenge/ipe/collect' or secendpart =="mailforspam.com" and url =='https://accounts.google.com/v3/signin/challenge/selection':
                            recov[0].click()
                            mailPart = getFirstPart(IspUser.recovery)
                            mailforspam(driver, mailPart)
                        if secendpart !="mailforspam.com" and current_url =='https://accounts.google.com/signin/v2/challenge/selection':
                            driver.quit()
                            save_to_files("recovery_problem", IspUser.showString())
                    except:pass
                if not otp:
                    recoveryInput = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                    recoveryInput.send_keys(IspUser.recovery)
                    time.sleep(1)
                    nextBtn= driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']")
                    nextBtn.click()

                    try:
                        try:
                            # Recov Wrong
                            recov_wrong = driver.find_element(By.CSS_SELECTOR,"div.o6cuMc.Jj6Lae")
                        except:
                            try:
                                # Too many Reterys
                                recov_wrong = driver.find_element(By.CSS_SELECTOR,"div[jsname='TMYUoe']")
                            except:pass
                        if recov_wrong:
                            save_to_files("wrong_recovery", IspUser.showString())
                            driver.quit()
                    except:pass
                else:
                    try:
                        otp = request_otp(IspUser.email)
                        if otp == "":
                            save_to_files("otp_app", IspUser.showString())
                            driver.quit()
                            return True
                        else:
                            driver.find_element(By.CSS_SELECTOR,"input[type='tel']").send_keys(otp)
                            driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ ']").click()
                            time.sleep(2)
                    except:pass
                

            except:pass
            solving:True
            try:
                driver.find_element(By.CSS_SELECTOR,"div[class='captcha-solver captcha-solver_inner']").click()
            except:solving=False
            time.sleep(10)
            # url = driver.current_url
            # url = url.split('?')[0]
            # if url =='https://accounts.google.com/signin/v2/disabled/explanation':
            #     support_disabled(IspUser,driver,False)


    except Exception as e:
                pass
            
def sms_recieve(driver, IspUser, flag):
    SELECTORS = {
    "next":[
            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']",
            "//input[@type='submit']",
            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
            "//button[contains(text(),'Next')]",
        ],
    "code":['idvAnyPhonePin',
            'smsUserPin',
        ],
    }
    WAIT = 4
    AUTO_GENERATE_NUMBER = 10
    # Your SMS-Activate API key
    API_KEY = sms_api_key
    #API_KEY = "14fc3e42011cBBe708f53e30e2Bd2c21"
    COUNTRY_CODE = crt_code
    REQUEST_MAX_TRY = 10
    #sms_activate_url = sms_activate_url
    #sms_activate_url = "https://sms-activation-service.com/stubs/handler_api"
    phone_request_params = {
    "api_key":API_KEY,
    "action":"getNumber",
    "country":COUNTRY_CODE, 
    "service":"go",
    }

    status_param = {
        "api_key":API_KEY,
        "action":"getStatus"
    }
    try:
        phone_number_input = driver.find_element(By.XPATH,"//*[@type='tel']")
        if phone_number_input:
            count= 0
            count1= 0
            
            while (count1 < 4):
                count1 += 1
                if count1==4:
                    save_to_files("verification", IspUser.showString())
                    driver.quit()
                    return
                while(count < 50):
                    count += 1
                    res = requests.get(url=sms_activate_url,params = phone_request_params)
                    data = res.text
                    #print(data)
                    if "ACCESS_NUMBER" in data:
                        activationId = data.split(':')[1]
                        number = data.split(':')[2]
                        
                        number = '+'+ number
                        #print(number)
                        break
                    elif "NO_BALANCE" in data:
                        save_to_files("verification", IspUser.showString())
                        driver.quit()
                        print("NO_BALANCE")
                        return
                    elif count == 49:
                        save_to_files("verification", IspUser.showString())
                        driver.quit()
                        return
                    # if "NO_NUMBER" in data:
                    #     print("there is no number in this coiuntry code, pls change the country code in sms-activate.")
                    #     exit()
                    
                    time.sleep(WAIT)
                if number == '':
                    break
                    #print("################ Cannot get phone number: ", REQUEST_MAX_TRY, " times retrial. ################")
                    #raise Exception("Go to next account.")
                try:
                    phone_number_input = driver.find_element(By.XPATH,"//*[@type='tel']")

                    phone_number_input.clear()
                    phone_number_input.send_keys(number)
                except:pass
                
                #click next button
                #print('################ Click "Next" Buton ################')
                
                for selector in SELECTORS['next']:
                    try:
                        driver.find_element(By.XPATH, selector).click()
                        break
                    except:
                        pass
                try:
                    time.sleep(10)
                    inputcode=""
                    for selector in SELECTORS['code']:
                        try:
                            inputcode= driver.find_element(By.ID, selector)
                            break
                        except:pass
                    try:
                        if inputcode!="":
                            break
                    except:pass
                    else:
                        try:
                            driver.find_element(By.CSS_SELECTOR, "button[name='action']").click()
                        except:pass
                except:pass
                time.sleep(2)
            #print('################ Get SMS Code from SMS_Activate ################')
            time.sleep(WAIT)

            count_status = 0
            code = ''
            
            while(count_status < REQUEST_MAX_TRY):
                status_param['id'] = activationId
                #print(status_param)
                res_code = requests.get(url=sms_activate_url,params = status_param)
                data_code = res_code.text
                #print(data_code)
                if "STATUS_OK" in data_code:
                    code = data_code.split(':')[1]
                    break

                count_status = count_status + 1
                time.sleep(WAIT*5)

            if code == '':
                driver.get('https://accounts.google.com/v3/signin/challenge/pwd?')
                save_to_files("verification", IspUser.showString())
                driver.quit()
                return
                #print('Cannot receive code from sms_activate: ',REQUEST_MAX_TRY, " times retrial")
                #raise Exception("Go to next account.")
            #print('################ Verify Phone Code ################')
            else:
                for selector in SELECTORS['code']:
                    try:
                        driver.find_element(By.ID, selector).send_keys(code)
                        break
                    except:pass

                #click next button
                #print('################ Click "Verify" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        driver.find_element(By.XPATH, selector).click()
                        time.sleep(5)
                        current_url = driver.current_url
                        verification ='https://accounts.google.com/speedbump/idvreenable'
                        verification2 ='https://accounts.google.com/speedbump/idvreenable/sendidv'
                        current_url = current_url.split("?")[0]
                        if current_url == "https://mail.google.com/mail/u/0/#inbox":
                            time.sleep(2)
                            save_to_files("ok", IspUser.showString())
                            driver.quit()
                            return
                        else:
                            result = result_check_gmail(IspUser, driver,True,True,False,False)
                        if result:
                            try:
                                driver.quit()
                                return
                            except:pass
                            return
                    except:
                        pass

                
                    
                
    except:pass
def support_verfication(IspUser,driver, isp,manual, flag=False):
    url= driver.current_url
    try:
            if driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"):
                res = solve_captcha(driver,url, isp, IspUser)
                if res:
                    return True
    except:pass
    if not manual:
        try:
            try:
                driver.find_element(By.CSS_SELECTOR,"input[aria-label='Enter code']")
            except:
                if driver.find_element(By.XPATH,"//*[@type='tel']"):
                    sms_recieve(driver, IspUser, flag)
        except:pass
        try:
            driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[0].send_keys(IspUser.password+"1")
            time.sleep(1)
            driver.find_elements(By.XPATH,'input[id="Password"]')[1].send_keys(IspUser.password+"1")
            time.sleep(1)
            driver.find_element(By.XPATH,"input[type='submit']").click()
            save_to_files("forced_tochangePwd", IspUser.showString())
        except:pass
        return True
    else:
        while True:
            try:
                driver.current_url
            except:
                break

def read_restrivted_msg(file='restricted_msgs.txt'):
    path = os.path.join("ressources",file)
    with open(path, 'r') as file:
        lines = file.readlines()

    extracted_messages = []
    current_message = ""

    for line in lines:
        if line.strip():
            current_message += line.strip() + "\n"
        else:
            if current_message:
                extracted_messages.append(current_message.strip())
                current_message = ""  # Reset the current message

    # Append the last message if there are any remaining lines
    if current_message:
        extracted_messages.append(current_message.strip())

    # Select one message randomly
    message = random.choice(extracted_messages)

    return message


def generate_message(file='request_msgs.txt'):
    path = os.path.join("ressources",file)
    with open(path, 'r') as file:
        lines = file.readlines()

    # extracted_messages = []
    # current_message = ""

    # for line in lines:
    #     if line.strip():
    #         current_message += line.strip() + "\n"
    #     else:
    #         if current_message:
    #             extracted_messages.append(current_message.strip())
    #             current_message = ""  # Reset the current message

    # # Append the last message if there are any remaining lines
    # if current_message:
    #     extracted_messages.append(current_message.strip())

    # # Select one message randomly
    # message = random.choice(extracted_messages)
    message = ''.join(line for line in lines)

    return message

def generate_email(file='request_emails.txt'):
    path = os.path.join("ressources",file)
    with open(path, 'r') as file:
        lines = file.readlines()

    # Select one message randomly
    message = random.choice(lines)
    return message
def support_disable2(IspUser,driver,manual):
    try:
        if not manual:
            try:
                driver.find_element(By.CSS_SELECTOR, "div[class*='VfPpkd-LgbsSe']").click()
            except:
                driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe']").click()
            solving = True
            try:
                driver.find_element(By.CSS_SELECTOR,"div[class='captcha-solver captcha-solver_inner']").click()
            except:solving=False
            time.sleep(3)
            while solving:
                try:
                    driver.find_element(By.CSS_SELECTOR,"div[data-state='solved']")
                    break
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR,"div[class='captcha-solver captcha-solver_inner']").click()
                    except:pass
            time.sleep(1)
            try:
                submit_btn = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"],button[type="button"]')[0]
                submit_btn.click()
            except:pass
            try:
                email= driver.find_element(By.CSS_SELECTOR, "input[name*='identifier']")
                email.clear()
                email.send_keys(IspUser.email)
                driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 ']").click()
            except:pass
            status = password(driver, IspUser)
            if status:
                return
            status = password(driver, IspUser)
            if status:
                return
            url = driver.current_url
            url = url.split('?')[0]
            if url == "https://accounts.google.com/v3/signin/rejected":
                save_to_files("disable_specious", IspUser.showString()) 
                return

            secendpart = getFirstPart(IspUser.recovery, True)
            if url == 'https://accounts.google.com/v3/signin/challenge/iap':
                support_verfication(IspUser,driver,'gmail',manual, True)
            
            if secendpart =="mailforspam.com" and url =='https://accounts.google.com/v3/signin/challenge/ipe/collect' or secendpart =="mailforspam.com" and url =='https://accounts.google.com/v3/signin/challenge/selection':
                email_input= driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                email_input.send_keys(IspUser.recovery)
                driver.find_elements(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe']")[0].click()
                mailPart = getFirstPart(IspUser.recovery)
                mailforspam(driver, mailPart)
            if url == 'https://accounts.google.com/signin/v2/speedbump/changepassword/changepasswordform' or url == 'https://accounts.google.com/speedbump/changepassword':
                try:
                    time.sleep(3)
                    driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[0].send_keys(IspUser.password+"1")
                    time.sleep(1)
                    driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[1].send_keys(IspUser.password+"1")
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='button']").click()
                    save_to_files("forced_tochangePwd", IspUser.showString())
                    driver.quit()
                    return True
                except:pass
            if secendpart !="mailforspam.com":
                driver.quit()
                save_to_files("recovery_problem", IspUser.showString())
                return
    except:
        pass
def support_disabled(IspUser,driver,manual):
    try:
        if not manual:
            url = driver.current_url
            url = url.split('?')[0]
            if url == 'https://accounts.google.com/signin/v2/disabled/appeal/received':
                save_to_files("requested_disable", IspUser.showString())
                driver.quit()
                return True
            else:
                element = driver.find_elements(By.CSS_SELECTOR, "div[class='dMNVAe']")[1]
                text = element.text
                match = re.search(r'on\s([A-Za-z]+\s\d{1,2},\s\d{4})\.', text)
                if match:
                    date_disabled = match.group(1)
                    #print(f"Date disabled: {date_disabled}")
                else:
                    date_disabled = datetime.now().strftime("%B %d, %Y")
                time.sleep(5)
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                url = driver.current_url
                url = url.split('?')[0]
                if url == 'https://accounts.google.com/signin/v2/disabled/appeal/received':
                    save_to_files("requested_disable", IspUser.showString())
                    driver.quit()
                    return True
                time.sleep(5)
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                msg= generate_message()
                time.sleep(1)
                input = driver.find_elements(By.CSS_SELECTOR,"textarea[class='KHxj8b tL9Q4c']")[0]
                time.sleep(1)
                
                
                msg = msg.replace("date_replace", date_disabled)
                msg += f"\n{IspUser.email}"
                #print(msg)
                driver.execute_script("arguments[0].value = arguments[1];", input, msg)
                time.sleep(5)
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                #input.send_keys(msg)

                time.sleep(3)
                inpt = driver.find_element(By.CSS_SELECTOR,"input[type='email']")
                time.sleep(1)
                email = generate_email()
                inpt.send_keys(email)
                time.sleep(5)
                try:
                    driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
                    time.sleep(5)
                except Exception as e:
                    time.sleep(5)
                    save_to_files("requested_disable", IspUser.showString())
                    driver.quit()
                    return True

                save_to_files("requested_disable", IspUser.showString())
                driver.quit()
                return True
               
        else:
            url = driver.current_url
            url = url.split('?')[0]
            if url == 'https://accounts.google.com/signin/v2/disabled/appeal/received':
                save_to_files("requested_disable", IspUser.showString())
                driver.quit()
                return True
            else:
                element = driver.find_elements(By.CSS_SELECTOR, "div[class='dMNVAe']")[1]
                text = element.text
                match = re.search(r'on\s([A-Za-z]+\s\d{1,2},\s\d{4})\.', text)
                if match:
                    date_disabled = match.group(1)
                    #print(f"Date disabled: {date_disabled}")
                else:
                    date_disabled = datetime.now().strftime("%B %d, %Y")
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ").click()
                url = driver.current_url
                url = url.split('?')[0]
                if url == 'https://accounts.google.com/signin/v2/disabled/appeal/received':
                    save_to_files("requested_disable", IspUser.showString())
                    driver.quit()
                    return True
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe']").click()
                msg= generate_message()
                time.sleep(1)
                input = driver.find_elements(By.CSS_SELECTOR,"textarea[class='KHxj8b tL9Q4c']")[0]
                time.sleep(1)
                msg = msg.replace("date_replace", date_disabled)
                msg += f"\n{IspUser.email}"
                #print(msg)
                driver.execute_script("arguments[0].value = arguments[1];", input, msg)
                time.sleep(3)
                try:
                    driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd']").click()
                except:pass
                #input.send_keys(msg)
                time.sleep(3)
                inpt = driver.find_element(By.CSS_SELECTOR,"input[type='email']")
                time.sleep(1)
                file_path = os.path.join("ressources",'request_emails.txt')
                email = generate_email()
                inpt.send_keys(email)
                time.sleep(1)
                try:
                    try:
                        driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd']").click()
                    except:pass
                    time.sleep(8)
                    save_to_files("requested_disable", IspUser.showString())
                    driver.quit()
                    return True
                except:
                    save_to_files("requested_disable", IspUser.showString())
                    driver.quit()
                    return True
    except Exception as e:
        driver.quit()
        return True


def support_restracted(IspUser,driver,manual):
    driver.get('https://myaccount.google.com/restrictions/54')
    try:
        driver.find_element(By.CSS_SELECTOR,"div[class='VfPpkd-ksKsZd-XxIAqe i3FRte']").click()
        if not manual:
            msg= read_restrivted_msg()
            try:
                msg = msg.replace("[your email address]", IspUser.email)
            except:pass
            time.sleep(2)
            input = driver.find_elements(By.CSS_SELECTOR,"textarea[class*='VfPpkd']")[0]
            time.sleep(2)
            input.send_keys(msg)
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"button[class*='UywwFc-LgbsSe']").click()
            time.sleep(3)
            save_to_files("requested", IspUser.showString())
        else:
            while True:
                try:
                    driver.current_url
                except:
                    break
    except:save_to_files("restricted_2step", IspUser.showString())


def load_secrets():
    secret_path = os.path.join("result", "secrets.json")
    with open(secret_path, 'r') as f:
        return json.load(f)
        
def request_otp(email):
    try:
        # Load existing secrets
        secrets = load_secrets()
        secrets = {k.strip().lower(): v.strip() for k, v in secrets.items()}
        if email in secrets: 
            secret = secrets[email]
            totp = pyotp.TOTP(secret)
            new_otp = totp.now()
            return new_otp
        return ""
        
    except Exception as e :
        pass

def result_check_gmail(IspUser, driver,close,support,manual,stay):
    try:
        MainUrl = "https://mail.google.com/mail/u/0/"
        AccountUrl = "https://myaccount.google.com/"
        pliUrl = "https://myaccount.google.com/?pli=1"
        pliUrlMail = "https://mail.google.com/mail/u/0/?pli=1"
        SpamUrl = "https://mail.google.com/mail/u/0/#spam"
        okurl = 'https://mail.google.com/mail/u/0/#inbox'
        url_list = [MainUrl, AccountUrl, pliUrl, pliUrlMail, SpamUrl,okurl]
        # link for gmail err states
        RestrictedUrl = "https://accounts.google.com/v3/signin/productaccess/landing"
        RestrictedUrl2 = 'https://support.google.com/accounts/answer/40039'
        RestrictedUrl3 = 'https://myaccount.google.com/restrictions/54'
        disable ='https://accounts.google.com/signin/v2/deniedsigninrejected'
        disable2 = "https://accounts.google.com/v3/signin/rejected"
        disable3 ='https://accounts.google.com/signin/v2/disabled/explanation'
        captchaV2= "https://accounts.google.com/signin/v2/challenge/recaptcha"
        captchaV3= "https://accounts.google.com/v3/signin/challenge/recaptcha"
        insecure = "https://accounts.google.com/v3/signin/confirmidentifier"
        easy_captcha= "https://accounts.google.com/speedbump/captchareenable"
        undertandsuit ='https://accounts.google.com/speedbump/gaplustos'
        not_now = "https://gds.google.com/web/chip"
        not_now2 ="https://accounts.google.com/signin/v2/passkeyenrollment"
        not_now3 = "https://accounts.google.com/v3/signin/speedbump/passkeyenrollment"
        phonenumber = 'https://accounts.google.com/v3/signin/challenge/iap'
        verification ='https://accounts.google.com/speedbump/idvreenable'
        verification2 ='https://accounts.google.com/speedbump/idvreenable/sendidv'
        vrf3 = 'https://accounts.google.com/signin/v2/challenge/iap'
        twostep = [
            "https://accounts.google.com/signin/v2/challenge/ipp",
            "https://accounts.google.com/v3/signin/challenge/ipp/collect",
            "https://accounts.google.com/v3/signin/challenge/bc",
                "https://accounts.google.com/v3/signin/challenge/wa",
                "https://accounts.google.com/v3/signin/challenge/ootp",
                "https://accounts.google.com/v3/signin/challenge/sq",
                "https://accounts.google.com/v3/signin/challenge/ipe/verify",
                "https://accounts.google.com/v3/signin/challenge/ipe",
                "https://accounts.google.com/v2/signin/challenge/ipe",
                "https://accounts.google.com/signin/v2/challenge/ipe",
                "https://accounts.google.com/v3/signin/challenge/dp",
                "https://accounts.google.com/v3/signin/challenge/ipp/consent",
                "https://accounts.google.com/signin/v2/challenge/bc",
                "https://accounts.google.com/signin/v2/challenge/ootp",
                'https://accounts.google.com/signin/v2/challenge/dp',
                "https://accounts.google.com/signin/v2/challenge/wa",
                "https://accounts.google.com/v3/signin/challenge/ipp/qrcode?"
            ]
        otp = "https://accounts.google.com/signin/v2/challenge/totp"
        otpV3 ="https://accounts.google.com/v3/signin/challenge/totp"
        date ='https://myaccount.google.com/interstitials/birthday'
        time.sleep(2)
        try:
            current_url = driver.current_url
            unique_url = current_url
        except:
            try:
                driver.refresh()
            except:pass

        current_url = current_url.split('?')[0]

        if current_url =='https://accounts.google.com/v3/signin/identifier' or current_url =='https://accounts.google.com/signin/v2/identifier':
            try:
                email= driver.find_element(By.CSS_SELECTOR, "input[name*='identifier']")
                email.send_keys(IspUser.email)
                driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 ']").click()
            except:pass
        try:
            time.sleep(2)
            if current_url == 'https://accounts.google.com/v3/signin/challenge/pwd' or current_url == 'https://accounts.google.com/signin/v2/challenge/pwd':
                status = password(driver, IspUser)
                if status:
                    return
            time.sleep(2)
            url = driver.current_url
            url = url.split('?')[0]
            if url == 'https://accounts.google.com/signin/v2/challenge/selection' or url == 'https://accounts.google.com/v3/signin/challenge/selection':
                recovery(driver, IspUser)
        except:pass
        try:
            url = driver.current_url
            url = url.split('?')[0]
            time.sleep(2)
            if url == 'https://accounts.google.com/signin/v2/speedbump/changepassword/changepasswordform' or url == 'https://accounts.google.com/speedbump/changepassword':
                try:
                    time.sleep(3)
                    driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[0].send_keys(IspUser.password+"1")
                    time.sleep(1)
                    driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[1].send_keys(IspUser.password+"1")
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='button']").click()
                    save_to_files("forced_tochangePwd", IspUser.showString())
                    driver.quit()
                    return True
                except:pass
        except:pass
        if url in url_list:
            try:
                if close and not stay:
                    save_to_files("ok", IspUser.showString())
                    driver.quit()
                    return True
                elif not close and not stay:
                    save_to_files("ok", IspUser.showString())
                    return True
            except Exception as e : print(e)
        elif current_url == RestrictedUrl or current_url == RestrictedUrl2 or current_url == RestrictedUrl3:
            if support==False and not stay:
                save_to_files("Restricted", IspUser.showString())
                driver.quit()
                return True
            elif support:
                support_restracted(IspUser,driver,manual)
                driver.quit()
                return True 
            elif stay:
                while True:
                    try:
                        driver.current_url
                    except:break
            
        elif current_url == disable or current_url == disable2 or current_url == disable3:
            if not stay and support==False:
                element = driver.find_element(By.CSS_SELECTOR, "span.VfPpkd-vQzf8d")
                text = element.text
                if disable2 or disable:
                    save_to_files("VerifyItsYou", IspUser.showString())
                    driver.quit()
                    return True
            elif support and current_url != disable3:
                if current_url == disable2 or current_url ==disable :
                    support_disable2(IspUser,driver,manual)
                    return True
            elif current_url == disable3 and support:
                result = support_disabled(IspUser,driver,manual)
                return True
            elif not stay and not support:
                save_to_files("disabled", IspUser.showString())
                driver.quit()
                return True
            else:
                while True:
                    try:
                        driver.current_url
                    except:break
        elif current_url == captchaV2 or current_url == captchaV3 :
            if not stay and support == False:
                save_to_files("recaptcha", IspUser.showString())
                driver.quit()
                return True
            if support:
                url = driver.current_url
                if not manual:
                    res = solve_captcha(driver,url, 'gmail', IspUser)
                    if res:
                        return True
                else:
                    result = False
                    try:
                        url = driver.current_url
                        url = url.split('?')[0]
                        if url == 'https://accounts.google.com/v3/signin/challenge/pwd' or url == 'https://accounts.google.com/signin/v2/challenge/pwd':
                            password(driver, IspUser)
                            status = password(driver, IspUser)
                            if status:
                                return
                            time.sleep(2)
                        url = driver.current_url
                        url = url.split('?')[0]
                        if url == 'https://accounts.google.com/signin/v2/challenge/selection' or url == 'https://accounts.google.com/v3/signin/challenge/selection':
                            recovery(driver, IspUser)
                    except:pass

                result = result_check_gmail(IspUser, driver,close,support,manual,stay)
                if result and close and not stay:
                    try:
                        driver.quit()
                    except:pass
                elif result and not close and not stay:
                    return

            elif stay:
                while True:
                    try:
                        driver.current_url
                    except:break
                    
        elif current_url ==phonenumber or current_url ==vrf3:
            if not stay and support == False:
                save_to_files("phonenumber", IspUser.showString())
                driver.quit()
                return True
            elif support:
                result = support_verfication(IspUser,driver,'gmail',manual, True)
                if result:
                    return True
        elif current_url ==verification or current_url ==verification2:
            if not stay and support == False:
                    save_to_files("verification", IspUser.showString())
                    driver.quit()
                    return True
            elif support:
                result = support_verfication(IspUser,driver,'gmail',manual)
                if result:
                    return True
            elif stay:
                while True:
                    try:
                        driver.current_url
                    except:break
        elif current_url ==insecure:
            if not stay:
                    save_to_files("confirmidentifier", IspUser.showString())
                    driver.quit()
                    return True
            else:
                while True:
                    try:
                        driver.current_url
                    except:break

        elif current_url in twostep:
            if not stay:
                    save_to_files("2tep_vrf", IspUser.showString())
                    driver.quit()
                    return True
            else:
                while True:
                    try:
                        driver.current_url
                    except:break
        elif current_url ==easy_captcha:
            if not stay:
                    save_to_files("easy_captcha", IspUser.showString())
                    driver.quit()
                    return True
            else:
                while True:
                    try:
                        driver.current_url
                    except:break
        elif current_url ==undertandsuit:
            #understand gsuit
            try:
                driver.find_element(By.CSS_SELECTOR,"input[class='MK9CEd MVpUfe']").click()
            except:pass
            time.sleep(2)
            try:
                driver.find_element(By.CSS_SELECTOR,"div[class='T-P-aut-UR T-P-aut']").click()
            except:pass
        elif current_url ==not_now  or current_url ==not_now3 or current_url ==not_now2 or current_url =='https://gds.google.com/web/recoveryoptions' or current_url ==date:
                if current_url ==not_now2:
                    driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf']").click()
                    time.sleep(2)
                else:
                    driver.get(MainUrl)
                if not stay and close:
                    save_to_files("ok", IspUser.showString())
                    driver.quit()
                    return True
        elif current_url == otp or current_url == otpV3:
            try:
                otp = request_otp(IspUser.email)
                if otp == "":
                    save_to_files("otp_app", IspUser.showString())
                    driver.quit()
                    return True
                else:
                    driver.find_element(By.CSS_SELECTOR,"input[type='tel']").send_keys(otp)
                    driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ ']").click()
                    time.sleep(2)
            except:pass
        if driver.current_url!=unique_url:
            result = result_check_gmail(IspUser, driver,close,support,manual,stay)
            if result and close and not stay:
                try:
                    driver.quit()
                except:pass
            elif result and not close and not stay:
                return
        driver.refresh()
                    
    except Exception as e :
        pass

def close_secend_window(driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

def password(driver, IspUser):
    try:
        pwd = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
    except:
        try:
            pwd = driver.find_element("xpath", '//input[@type="password" and @name="Passwd"]')
        except:
            pass
    try:
        if pwd:
            pwd.send_keys(IspUser.password)
            time.sleep(1)
            try:
                driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ']").click()
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, "button[id='passwordNext']").click()
                except:pass


            #checking if Password wrong
            pwd_wrong = driver.find_element(By.CSS_SELECTOR,"div[jsname='B34EJ'] span[jsslot='']")
            if pwd_wrong:
                save_to_files("wrong_password", IspUser.showString())
                driver.quit()
                return True
    except:pass
    try:
        try:
            driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
        except:pass
        driver.find_element(By.CSS_SELECTOR,"input[name='ConfirmPassword']")
        #actions.first_login_changePassword(IspUser, driver)
    except:pass
    try:
        url = driver.current_url
        url = url.split('?')[0]
        if url == "https://accounts.google.com/v3/signin/challenge/totp" or url == "https://accounts.google.com/signin/v2/challenge/totp":
            otp = request_otp(IspUser.email)
            if otp == "":
                save_to_files("otp_app", IspUser.showString())
                driver.quit()
                return True
            else:
                driver.find_element(By.CSS_SELECTOR,"input[type='tel']").send_keys(otp)
                driver.find_element(By.CSS_SELECTOR,"button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ ']").click()
                time.sleep(2)
    except:pass
    try:
        url = driver.current_url
        url = url.split('?')[0]
        if url =='https://accounts.google.com/signin/v2/speedbump/changepassword/changepasswordform' or url =='https://accounts.google.com/speedbump/changepassword':
            time.sleep(3)
            driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[0].send_keys(IspUser.password+"1")
            time.sleep(1)
            driver.find_elements(By.CSS_SELECTOR,'input[type="password"]')[1].send_keys(IspUser.password+"1")
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='button']").click()
            save_to_files("forced_tochangePwd", IspUser.showString())
            return True
    except:pass

def recovery(driver, IspUser):
    # Handling Recovery input
    try:
        recov = driver.find_elements(By.CSS_SELECTOR, "div[role='link'][data-accountrecovery='false']")
        try:
            if not IspUser.recovery.endswith("@mailforspam.com"):
                try:
                    recov[2].click()
                except:recov[1].click()
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
                if secendpart =="mailforspam.com" and current_url =='https://accounts.google.com/signin/v2/challenge/selection' or secendpart =="mailforspam.com"and current_url =='https://accounts.google.com/v3/signin/challenge/selection':
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

def login_to_gmail(IspUser, driver,close,support,manual,stay):
    while True:
        try:
            LoginUrl = "https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession"
            MainUrl = "https://mail.google.com/mail/u/0/"
            AccountUrl = "https://myaccount.google.com/"
            pliUrl = "https://myaccount.google.com/?pli=1"
            pliUrlMail = "https://mail.google.com/mail/u/0/?pli=1"
            SpamUrl = "https://mail.google.com/mail/u/0/#spam"
            okurl = 'https://mail.google.com/mail/u/0/#inbox'

            url_list = [LoginUrl, MainUrl, AccountUrl, pliUrl, pliUrlMail, SpamUrl,okurl]
            url_list2 = [MainUrl, AccountUrl, pliUrl, pliUrlMail, SpamUrl,okurl]
            driver.get(LoginUrl)
            close_secend_window(driver)
            # Handling email support
            try:
                driver.find_elements(By.CSS_SELECTOR, "div[class='VV3oRb YZVTmd SmR8']")[0].click()
            except:pass
            try:
                email= driver.find_element(By.CSS_SELECTOR, "input[name*='identifier']")
                email.send_keys(IspUser.email)
                driver.find_element(By.CSS_SELECTOR, "button[class*='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 ']").click()
            except:pass
            try:
                try:
                    driver.find_element("id", "identifierNext").click()
                except:pass
                keywrds_captcha = driver.find_element(By.CSS_SELECTOR, 'input[type="text"].whsOnd.zHQkBf')
                keywrds_captcha.send_keys()
                if keywrds_captcha and not support and not stay:
                    save_to_files("captcha", IspUser.showString())
                    driver.quit()
                    break
                else:
                    for i in range(5):
                        result = solve_captcha(driver,"check", 'gmail', IspUser)
                        if result:
                            break
            except:pass

            try:
                url = driver.current_url
                url = url.split('?')[0]
                time.sleep(2)
                if url == 'https://accounts.google.com/v3/signin/challenge/pwd' or url == 'https://accounts.google.com/signin/v2/challenge/pwd':
                    status = password(driver, IspUser)
                    if status:
                        return
                time.sleep(2)
                url = driver.current_url
                url = url.split('?')[0]
                if url == 'https://accounts.google.com/signin/v2/challenge/selection' or url == 'https://accounts.google.com/v3/signin/challenge/selection':
                    recovery(driver, IspUser)
            except:pass

            try:
                current_url = driver.current_url
                current_url = current_url.split('?')[0]
                if current_url in url_list2 and close and support ==False:
                    driver.get(MainUrl)
                    time.sleep(5)
                    try:
                        driver.find_element(By.CSS_SELECTOR,"div[class='T-P-aut-UR T-P-aut']").click()
                    except:pass
                    save_to_files("ok", IspUser.showString())
                    driver.quit()
                    break
            except: 
                break

            driver.implicitly_wait(2)

            result = result_check_gmail(IspUser, driver,close,support,manual,stay)
            if result and close and not stay:
                try:
                    driver.quit()
                except:pass
                break
            elif result and not close and not stay or not driver:
                return "kill"
            try:
                    email_value= IspUser.email
                    mail = driver.find_element(By.CSS_SELECTOR, f"div[data-identifier='{email_value}']")
                    mail.click()
            except:pass

            try:
                    try:
                        current_url = driver.current_url
                    except:
                        break

                    separators = ['#inbox', '#spam']
                    for separator in separators:
                        try:
                            current_url = current_url.split(separator, 1)[0]
                        except:pass
                    if current_url in url_list and not stay:
                        #driver.get(MainUrl)
                        time.sleep(5)
                        save_to_files("ok", IspUser.showString())
                        break
                    else:
                        driver.refresh()
            except:pass


        except Exception as e :
            save_to_files("log",e.args[0]+"\n")
            driver.quit()
            break

def mainlnesia(driver,mailPart, value =False):
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    # retrive security code from mailnesia
    for i in range(3):
        try:
            driver.get(f"https://mailnesia.com/mailbox/{mailPart}")
            time.sleep(1)
            if value:
                driver.find_element(By.CSS_SELECTOR, "a[href*='mail/']").click()
            else:
                driver.find_element(By.XPATH, "//a[contains(text(), 'Microsoft account security code')]").click()
            data = driver.find_elements(By.CSS_SELECTOR, "[style*='Segoe UI Bold']")[1]
            data = data.text
            if data:
                break
        except:
            driver.refresh()
    try:
        # delete all emails
        driver.find_element(By.CSS_SELECTOR,"img[alt='Delete all mail']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,"input[type='button']").click()
        time.sleep(1)
    except:pass
    driver.close()
    #switch to default window
    driver.switch_to.window(driver.window_handles[0])
    try:
        if data:
            #send code
            tel = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
            tel.clear()
            tel.send_keys(data)
            driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
            return True
        else:
            return False
    except:
        return False

def mailforspam(driver,mailPart, value= False):
    time.sleep(8)
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    # retrive security code from mailnesia
    for i in range(3):
        try:
            driver.get(f"http://www.mailforspam.com/mail/{mailPart}")
            time.sleep(1)
            try:
                driver.find_element(By.CSS_SELECTOR, "button[id='details-button']").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "a[id='proceed-link']").click()
            except:pass

            
            if value:
                try:
                    driver.find_element(By.CSS_SELECTOR, "a[href*='mail/']").click()
                except:pass
            else:
                try:
                    driver.find_element(By.XPATH, "//a[contains(text(), 'Google Verification Code')]").click()
                except:
                    driver.find_element(By.XPATH, "//a[contains(text(), 'Code de vérification Google')]").click()
                
            time.sleep(1)
            body_element = driver.find_element(By.ID, 'messagebody')
            lines = body_element.text.split('\n')
            # Check each line for the presence of "Security code:"
            if value:
                for line in lines:
                    patterns = ['Your single-use code is: ', 'Your single-use code is : ', 'Votre code à usage unique est: ', 'Votre code à usage unique est : ']
                    data = next((line.split(pattern)[1] for pattern in patterns if pattern in line), None)  
                    if data:
                        break
            else:
                if len(lines)>16:
                    data = lines[16]
                    if data == '':
                        data = lines[17]
                    break
                else:
                    data =None
                    break
        except Exception as e:
            driver.refresh()
    driver.close()
    #switch to default window
    driver.switch_to.window(driver.window_handles[0])

    try:
        if data:
            #send code
            tel = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
            tel.clear()
            tel.send_keys(data)
            driver.find_element(By.CSS_SELECTOR,"button[type='button']").click()
            time.sleep(5)
            return True
        else:
            return False
    except:
        return False
    
def mailforspam_hotmail(driver,mailPart, value= False):
    time.sleep(8)
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    # retrive security code from mailnesia
    for i in range(3):
        try:
            driver.get(f"https://www.mailforspam.com/mail/{mailPart}")
            time.sleep(1)
            if value:
                try:
                    driver.find_element(By.CSS_SELECTOR, "a[href*='mail/']").click()
                except:pass
            else:
                try:
                    driver.find_element(By.XPATH, "//a[contains(text(), 'Google Verification Code')]").click()
                except:
                    driver.find_element(By.XPATH, "//a[contains(text(), 'Code de vérification Google')]").click()
                
            time.sleep(1)
            body_element = driver.find_element(By.ID, 'messagebody')
            lines = body_element.text.split('\n')
            # Check each line for the presence of "Security code:"
            if value:
                for line in lines:
                    patterns = ['Your single-use code is: ', 'Your single-use code is : ', 'Votre code à usage unique est: ', 'Votre code à usage unique est : ']
                    data = next((line.split(pattern)[1] for pattern in patterns if pattern in line), None)  
                    if data:
                        break
            else:
                for line in lines:
                    patterns = ['Code de sécurité : ', 'Code de sécurité: ', 'Security code : ', 'Security code: ']
                    data = next((line.split(pattern)[1] for pattern in patterns if pattern in line), None)  
                    if data:
                        break
            if data:
                break
        except:
            driver.refresh()
    driver.close()
    #switch to default window
    driver.switch_to.window(driver.window_handles[0])

    try:
        if data:
            #send code
            tel = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
            tel.clear()
            tel.send_keys(data)
            driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
            return True
        else:
            return False
    except:
        return False

def getFirstPart(email, secend=False):
        try:
            if '@' in email:
                username, domain = email.split('@', 1)
                if secend:
                    return domain
                else:
                    return username
        except:
            pass


def login_to_hotmail(IspUser, driver,close=False, wait=False):
    try:
        LoginUrl = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708442704&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26deeplink%3dowa%252f%26RpsCsrfState%3d65d04c9c-21c5-309e-2c28-5482fe0bc4f6&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c"
        MainUrl = "https://outlook.live.com/mail/0/"
        SpamUrl = "https://outlook.live.com/mail/0/junkemail"
        ContactUrl = "https://outlook.live.com/people/0/"
        ArchiveUrl = "https://outlook.live.com/mail/0/archive"
        url_list = [MainUrl, ContactUrl, SpamUrl, ArchiveUrl]
        driver.get(LoginUrl)
        
        driver.implicitly_wait(5)
        while True:
            # Handling email input
            try:
                time.sleep(1)
                email= driver.find_element(By.CSS_SELECTOR, 'input[type="email"][id="usernameEntry"]')
                email.send_keys(Keys.CONTROL + "a")
                # Use DELETE to delete the selected text uz clear nt clear saved Cookies
                email.send_keys(Keys.DELETE)
                email.send_keys(IspUser.email)
                time.sleep(1)
                nextBtn= driver.find_element(By.CSS_SELECTOR, "input[type='submit'],button[type='submit']")
                nextBtn.click()
                time.sleep(random.randint(1, 2))
            except:pass

            # Hasndling Password input
            try:
                pwd = driver.find_element("xpath", '//input[@type="password" and @name="passwd"]')
                pwd.send_keys(Keys.CONTROL + "a")
                # Use DELETE to delete the selected text uz clear nt clear saved Cookies
                pwd.send_keys(Keys.DELETE)
                pwd.send_keys(IspUser.password)
                time.sleep(1)
                nextBtn= driver.find_element(By.CSS_SELECTOR,"input[type='submit'],button[type='submit']")
                nextBtn.click()
            except:
                pass
            #looks good
            try:
                driver.find_element(By.CSS_SELECTOR,"input[id='iLooksGood']").click()
            except:pass

            # stay sign in button
            try:
                driver.find_element(By.CSS_SELECTOR,"button[type='button'][data-testid='secondaryButton']").click()
            except:pass
            
            try:
                driver.find_element(By.CSS_SELECTOR,"button[type='submit'][data-testid='primaryButton']").click()
            except:pass

            try:
                driver.get("https://outlook.live.com/mail/0/")
            except:pass

            try:
                current_url = driver.current_url
                try:
                    current_url = current_url.split('?')[0]
                except:pass
                if current_url in url_list:
                    driver.get(MainUrl)
                    save_to_files("ok", IspUser.showString())
                    if close:
                        driver.close()
                    break
            except: break

            try:
                secendpart = getFirstPart(IspUser.recovery, True)
                mailPart = getFirstPart(IspUser.recovery)
                recovery = driver.find_element(By.CSS_SELECTOR,"input[type='email'][aria-label='Alternate email address']")
                recovery.clear()
                if secendpart =="mailforspam.com":
                    recovery.send_keys(f"{mailPart}@{secendpart}")
                    driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
                    check = mailforspam(driver, mailPart)
                elif secendpart =="mainlnesia.com":
                    recovery.send_keys(f"{mailPart}@{secendpart}")
                    driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
                    check = mainlnesia(driver, mailPart)
                if not check and not wait:
                    save_to_files("failed_add_recovery", IspUser.showString())
                    driver.close()
                    break
                # waiting to handel recovery manual
                elif wait:
                    while True:
                        try:
                            currentUrl = driver.current_url
                        except:
                            driver.close()
                            break
            except:pass
            try:
                driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")[0].click()
                driver.find_element(By.CSS_SELECTOR,"input[id='iProofEmail']").send_keys(mailPart)
                driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
                if secendpart == "mailforspam.com":
                    fact = mailforspam(driver, mailPart)
                elif secendpart == "mainlnesia.com":
                    fact = mainlnesia(driver, mailPart)
                if not fact and not wait:
                    save_to_files("recovery_wrong",IspUser.showString())
                    driver.close()
                    break
                # waiting to handel recovery manual
                elif wait:
                    while True:
                        try:
                            currentUrl = driver.current_url
                        except:
                            driver.close()
                            break
            except:pass
            
            try:
                driver.find_element(By.ID,"idTxtBx_OTC_Password")
                if secendpart == "mailforspam.com":
                    fact = mailforspam(driver, mailPart, True)
                elif secendpart == "mainlnesia.com":
                    fact = mainlnesia(driver, mailPart, True)
                if not fact and not wait:
                    save_to_files("recovery_wrong",IspUser.showString())
                    driver.close()
                    break
            except:pass
            try:
                driver.find_element(By.ID,"acceptButton").click()
            except:pass
            try:
                driver.find_element(By.CSS_SELECTOR,'a[id="iCancel"]').click()
            except:pass
            try:
                try:
                    element = driver.find_element(By.ID, "iVerifyCodeError")
                except:
                    try:
                        element = driver.find_element(By.ID, "iVerificationErr")
                    except:
                        pass
                if element:
                    driver.get(LoginUrl)

            except:pass
            try:
            #checking if Password wrong
                pwd_wrong = driver.find_element(By.ID,"i0118Error")
                if pwd_wrong:
                    save_to_files("wrong_password", IspUser.showString())
                    driver.close()
                    break
            except:pass
            try:
                driver.find_element(By.CSS_SELECTOR,"a[data-bi-cn='SignIn']")
                driver.get(LoginUrl)
            except:pass
            # check if Recovery wrong
            try:
                vrf = driver.find_element(By.CSS_SELECTOR,"input[id='StartAction' i]")
                if vrf:
                    save_to_files("verification", IspUser.showString())
                    driver.close()
                    break
            except:pass
            driver.refresh()
            time.sleep(1)
            try:
                current_url = driver.current_url
                current_url = current_url.split('?')[0]
                if current_url in url_list:
                    driver.get(MainUrl)
                    save_to_files("ok", IspUser.showString())
                    if close:
                        driver.close()
                    break
            except: break
            

    except Exception as e :
        save_to_files("log",e.args[0]+"\n")


    
def login_to_yahoo(IspUser, driver,close=False):
    try:
        MainUrl = "https://login.yahoo.com/"
        url_list = [MainUrl]
        while True:
            driver.implicitly_wait(5)

            try:
                driver.find_element(By.CSS_SELECTOR, "a[name='username']").click()
            except:pass
            
            # Handling email input
            try:
                email= driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
                email.clear()
                email.send_keys(IspUser.email)
                time.sleep(2)
                nextBtn= driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                nextBtn.click()
                time.sleep(random.randint(3, 5))
            except:pass
            try:
                driver.find_element(By.CSS_SELECTOR, "p[id='wait-desc'][class='challenge-desc']")
                save_to_files('blocked_for_now',IspUser.showString())
                break
            except:pass
            #url= "https://login.yahoo.net/account/challenge/recaptcha/recaptcha-script?display=login&.lang=en-US&src=homepage&activity=ybar-signin&pspid=2023538075&add=1&done=https%3A%2F%2Fwww.yahoo.com%2F&prefill=0&prompt=login&chllngnm=fail&sessionIndex=QQ--&acrumb=lKC0qfal&authMechanism=primary&lang=en-US&siteKey=6LcbmroaAAAAANQ34XOxul9o_UgaJ6dkdq62Xey6&recaptchaLang=en&recaptchaDomain=www.google.com"
           #solve_captcha(driver,url)
            try:
                iframe = driver.find_element(By.CSS_SELECTOR,"iframe[id='recaptcha-iframe']")
                driver.switch_to.frame(iframe)
                for i in range(10):
                    try:
                        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
                        driver.switch_to.default_content()
                        break
                    except:
                        time.sleep(5)
                time.sleep(2)
                pwd = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
                pwd.send_keys(Keys.CONTROL + "a")
                # delete the selected text uz clear nt clear saved Cookies
                pwd.send_keys(Keys.DELETE)
                pwd.send_keys(IspUser.password)
                time.sleep(2)
                nextBtn= driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
                nextBtn.click()
                # pwd Wrong check
                driver.find_element(By.CSS_SELECTOR,"p[class='error-msg']")
                save_to_files('wrong_password',IspUser.showString())
                break
            except:
                pass

            

            try:
                driver.find_element(By.CSS_SELECTOR,"button[class*='validate-btn']")
                save_to_files('2step_vrf',IspUser.showString())
                break
            except:pass

            try:
                # accept all cookies
                driver.find_element(By.ID,"scroll-down-btn").click()
                driver.find_element(By.CSS_SELECTOR,"button[class='btn secondary accept-all ']").click()
            except:pass
            try:
                # declineAll
                driver.find_element(By.CSS_SELECTOR,"button[type='button'][id*='decline']").click()
            except:pass
            try:
                # save choices
                driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
            except:pass

            try:
                # finish later
                driver.find_element(By.CSS_SELECTOR,"button[class*='P_1Eu6qC']").click()
            except:pass

            try:
                #interfaced choice
                driver.find_element(By.CSS_SELECTOR,"button[class*='P_0 C_Z29WjXl']").click()
            except:pass


            
            time.sleep(1)
            try:
                current_url = driver.current_url
                separators = ['d/folders']
                for separator in separators:
                    try:
                        current_url = current_url.split(separator, 1)[0]
                    except:pass

                
                if current_url in url_list:
                    driver.get(MainUrl)
                    time.sleep(5)
                    save_to_files("ok", IspUser.showString())
                    if close:
                        driver.close()
                    break
            except: break
    except Exception as e :
        save_to_files("log",e.args[0]+"\n")