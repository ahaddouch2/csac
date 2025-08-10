import os
from selenium import webdriver
import zipfile
from menu import choice
import requests, json
import shutil, random, re
from fake_useragent import UserAgent
import zipfile,tempfile, string
from selenium.webdriver.chrome.service import Service



def get_local_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()["ip"]
        return public_ip
    except Exception as e:
        pass


        
def save_to_files(file_name,data, folder_name="result"):
    try:
        current_dir = os.getcwd()

        result_folder_path = os.path.join(current_dir, folder_name)
        if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)

        file_path = os.path.join(result_folder_path, f"{file_name}.txt")

        with open(file_path, 'a') as file:
            file.write(data)

    except Exception as e:
        save_to_files("log", e.args[0]+"\n")

def close_secend_window(driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

def get_config():
    try:
        config = "config.json"
        folder = "ressources"
        config_path = os.path.join(folder, config)
        with open(config_path, 'r') as file:
            data = json.load(file)
            # Your SMS-Activate API key
            sms_api_key = data.get('sms_api_key') #9b6b9eb50d0A30---------d9b7495b
            sms_activate_url = data.get('sms_end_point')
            COUNTRY_CODE =  data.get('country_code') #i.e, Austrailian country code, See country table in sms-activate. I often use Australian phone number and it works almost always.
            nbprocess =  int(data.get('threads'))
            nbmsgs = int(data.get('nbmsgs'))
            nbLoops = int(data.get('nbloops'))
            captcha_api_key = data.get('captcha_api_key')

        return sms_api_key,sms_activate_url, COUNTRY_CODE, nbprocess,nbmsgs, nbLoops,captcha_api_key
    except Exception as e:
        save_to_files("log.txt",e.args[0]+"\n")

sms_api_key, sms_activate_url, crt_code,_,_,_,captcha_api_key = get_config()
def get_timezone_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        return data.get("timezone")  # e.g., "Asia/Tokyo"
    except Exception as e:
        save_to_files("log",e.args[0]+"\n")
        return None

LATEST_VERSIONS = {
    "Chrome": "135",
    "Firefox": "137",
    "Edge": "135",
    "Opera": "117"
}

def get_valid_ua():
    # Initialize UserAgent to get a valid user agent template
    ua = UserAgent()
    
    # Get a valid user agent string from UserAgent
    valid_agents ="""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/137.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/117.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"""
    valid_agents_list = valid_agents.strip().split('\n')
    # Pick a random user agent from the valid list
    user_agent = random.choice(valid_agents_list) 
    return user_agent
                

# Function to delete cache directories
def delete_cache(deault_path):
    worker = "Service Worker\\CacheStorage"
    cash = "Cache"
    code = "Code Cache\\js"

    worker = os.path.join(deault_path, worker)
    cash = os.path.join(deault_path, cash)
    code = os.path.join(deault_path, code)
    if os.path.exists(worker):
        try:
            shutil.rmtree(worker)
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
    if os.path.exists(cash):
        try:
            shutil.rmtree(cash)
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")
    if os.path.exists(code):
        try:
            shutil.rmtree(code)
        except Exception as e:
            save_to_files("log",e.args[0]+"\n")

def CreateDriver(IspUser, profile=True):
    try:
        profile_folder_name = IspUser.email
        profiles_name = "ChromesProfiles"
        default_user_path = os.path.expanduser("~")
        profiles_container_path = os.path.join(default_user_path, profiles_name)
        profile_folder_path = os.path.join(default_user_path, profiles_name, profile_folder_name)
        options = webdriver.ChromeOptions()
        if not os.path.exists(profiles_container_path):
            os.makedirs(profiles_container_path)

        if not os.path.exists(profile_folder_path):
            os.makedirs(profile_folder_path)
        else:
            deault_path = os.path.join(profile_folder_path, "Default")
            delete_cache(deault_path)
        
        #if choice[0]!="26":
        options.add_argument(f"--user-data-dir={profile_folder_path}")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=" + f"{1200},{800}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--profile-directory=Default')
        options.add_argument('--no-sandbox')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        options.add_argument("--lang=en-us")
        options.add_argument("--allow-running-insecure-content")
        
        # options.add_argument("--enable-javascript")
        

        
        
        #options.add_extension('canvas-fingerprint-defender.crx')
        #options.add_experimental_option('useAutomationExtension', False)
        # agent_file_path = os.path.join(profile_folder_path, 'agent_user.txt')
        # if not os.path.exists(agent_file_path):
            
            
        #     user_agent = get_valid_ua()
        #     # user_agent = random.choice(user_agents)
        #     profile_folder_path
        #     with open(agent_file_path, 'w') as file:
        #         file.write(user_agent)
        #     options.add_argument(f'user-agent={user_agent}')
        # else:
            
        #     with open(agent_file_path, 'r') as file:
        #         user_agent = file.read().strip()
        #     if user_agent:
        #         options.add_argument(f'user-agent={user_agent}')
            
        cwd = os.getcwd()
        extension_dir = os.path.join(cwd, 'captcha_solver')
        browsersec = os.path.join(cwd, 'browsersec')
        load_captcha =False
        if choice[0]=="26" or choice[0]=="27":
            # with open("captcha_solver/common/config.js", "r", encoding="utf-8") as file:
            #     content = file.read()
            # content = re.sub(r'(apiKey:\s*)([^,\n]+)', fr'\1"{captcha_api_key}"', content)
            # with open("captcha_solver/common/config.js", "w", encoding="utf-8") as file:
            #     file.write(content)
            load_captcha = True

        if choice[0]=="32":
            try:
                cwd = os.getcwd()
                extension_path = os.path.join(cwd, 'noads.crx')
                options.add_extension(extension_path)
            except Exception as e: pass

       
        
        PROXY_HOST = IspUser.host  # rotating proxy or host
        PROXY_PORT = IspUser.port # port
        PROXY_USER = IspUser.proxyUser # username
        PROXY_PASS = IspUser.proxyPass # password
        
        if PROXY_USER and PROXY_PASS:
            os.makedirs(profile_folder_path, exist_ok=True)
            extension_directory = tempfile.mkdtemp(dir=profile_folder_path)
            # options.add_argument(f"--disable-extensions-except={extension_directory}")
            if not os.path.isdir(extension_directory):
                os.makedirs(extension_directory)

            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 3,
                "name": "Proxy Authentication",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "webRequest",
                    "webRequestAuthProvider"
                ],
                "host_permissions": [
                    "<all_urls>"
                ],
                "background": {
                    "service_worker": "background.js"
                },
                "minimum_chrome_version": "108"
            }
            """

            background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: %s
                    },
                    bypassList: ["localhost"]
                }
            };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                { urls: ["<all_urls>"] },
                ['blocking']
            );
            """ % (
            PROXY_HOST,
            PROXY_PORT,
            PROXY_USER,
            PROXY_PASS,
        )



            

            # Write the files to the extension directory
            with open(os.path.join(extension_directory, "manifest.json"), 'w') as f:
                f.write(manifest_json)

            with open(os.path.join(extension_directory, "background.js"), 'w') as f:
                f.write(background_js)

            

            if load_captcha:
                combined_dir = f"{extension_dir},{extension_directory}"
                options.add_argument(f"--disable-extensions-except={combined_dir}")
                options.add_argument(f"--load-extension={combined_dir}")
                
            else:
                options.add_argument(f"--disable-extensions-except={extension_directory}")
                options.add_argument(f"--load-extension={extension_directory}")
            

        elif PROXY_HOST!="127.0.0.1" and PROXY_HOST!=None and PROXY_HOST!="":
            if load_captcha:
                options.add_argument(f"--disable-extensions-except={extension_dir}")
                options.add_argument(f'--proxy-server=http://{PROXY_HOST}:{PROXY_PORT}')
                options.add_argument(f"--load-extension={extension_dir}")
            else:
                options.add_argument(f'--proxy-server=http://{PROXY_HOST}:{PROXY_PORT}')
                options.add_argument("--disable-extensions-except=null")
        else:
            if load_captcha:
                options.add_argument(f"--disable-extensions-except={extension_dir}")
                options.add_argument(f"--load-extension={extension_dir}")
        try:
            browser = webdriver.Chrome(
    service=Service('C:/chromedriver/chromedriver.exe'),
    options=options
)

            
        except Exception as e: 
            save_to_files("log.txt",e.args[0])

        browser.implicitly_wait(10)
        if PROXY_USER:
            shutil.rmtree(extension_directory)
        return browser


    except Exception as e:
        save_to_files("log.txt",e.args[0])