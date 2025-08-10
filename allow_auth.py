from selenium import webdriver as uc
import os
import time,random
import sys
import base64
from selenium.webdriver.common.by import By
from EmailClient import CreateDriver, save_to_files
from actions import GmailActions
from IspManager import ISPUser
from selenium.webdriver.remote.webdriver import WebDriver
import pyotp, json

def load_secrets():
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
            save_to_files("log",e.args[0]+"\n")

def handle_otp(driver, IspUser):
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
    except Exception as e :pass

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
    except:pass

def allow_auth(driver,url_auth,ispUser):

        # driver = CreateDriver(ispUser)
        url_auth= base64.b64decode(url_auth).decode()
        count=0
        while count <1:
            count +=1
            try:
                driver.get(url_auth)
            except:pass
           
            try:
                select_email = driver.find_element(By.CSS_SELECTOR, 'div[class*="VV3oRb YZVTmd SmR8"]')
                select_email.click()
            except:pass
            
            try:
                time.sleep(5)
                url = driver.current_url
                url, _ = url.split("?")
                if url == 'https://accounts.google.com/v3/signin/challenge/pwd' or url == 'https://accounts.google.com/signin/v2/challenge/pwd':
                    password(driver, ispUser)
                if url == "https://accounts.google.com/v3/signin/challenge/totp" or url == "https://accounts.google.com/signin/v2/challenge/totp":
                    handle_otp(driver,ispUser)
            except:pass
            try:
                advance = driver.find_element(By.CSS_SELECTOR, "a[href='#']")
                advance.click()
            except:pass
            try:
                app = driver.find_elements(By.CSS_SELECTOR, "a[href='#']")[1]
                app.click()
            except:pass
            try:
                allow = driver.find_element(By.ID,"submit_approve_access")
                allow.click()
                time.sleep(3)
                try:
                    element = driver.find_element(By.XPATH, '//pre[contains(text(), "The authentication flow has completed. You may close this window.")]')
                    if element:
                        driver.close()
                        break
                except:
                    pass
            except:pass
            try:
                element = driver.find_element(By.XPATH, '//pre[contains(text(), "The authentication flow has completed. You may close this window.")]')
                if element:
                    driver.close()
                    break
            except:
                pass
            try:
                RestrictedUrl = "https://accounts.google.com/signin/oauth/error/v2"
                api2step ='https://accounts.google.com/signin/v2/challenge/ipp'
                current_url = driver.current_url

                current_url = current_url.split('?', 1)[0]
                if current_url == RestrictedUrl:
                    save_to_files("Restricted", ispUser.showString())
                    driver.close()
                    break


                elif current_url == api2step :
                    save_to_files("api2step", ispUser.showString())
                    driver.close()
                    break                  
            except:pass

def attach_to_session(session_id):
    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        if command != "newSession":
            return original_execute(self, command, params)
        else:
            return {'status': 0, 'value': None, 'sessionId': session_id}

    WebDriver.execute = new_command_execute

    driver.session_id = session_id
    WebDriver.execute = original_execute
    return driver        


if __name__ == "__main__":

    if len(sys.argv) >= 4:
        url = sys.argv[1]
        user_data = {
        "email": sys.argv[2],
        "recovery": sys.argv[3],
        "password": sys.argv[4],
        "host": sys.argv[5],
        "port": sys.argv[6],
        "proxyUser": sys.argv[7],
        "proxyPwd": sys.argv[8]
    }
        ispUser = ISPUser(user_data)
        driver = CreateDriver(ispUser)
        GmailActions.checkAccount(ispUser, driver)
        allow_auth(driver,url,ispUser)