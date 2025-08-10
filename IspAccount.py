from EmailClient import CreateDriver, get_config, save_to_files
from actions import GmailActions, HotmailActions, YahooActions
from threading import Semaphore


_, _,_,nbProcess,nbMsgs,nbLoops,_ = get_config()

def close_secend_window(driver):
        if len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

semaphore = Semaphore(nbProcess)
def GmailChoices(IspUser, choice, i):
    try:
        print(f"[{i + 1}] Processing: {IspUser.email}...")
        # semaphore.acquire()
        while True:
            dontCheck = ["1","2","3","15","16","17","27","26","37","38","39", 0]
            if choice[0] !=0 and choice[0] !="15" and choice[0] !="16" and choice[0] !="37"  and choice[0] !="38" and choice[0] !="39":
                driver = CreateDriver(IspUser)
                # close_secend_window(driver)
            elif choice[0] !=0 and choice[0] !="37"  and choice[0] !="38" and choice[0] !="39":
                driver = CreateDriver(IspUser,False)
                # close_secend_window(driver)
            if choice[0] not in dontCheck:
                result = GmailActions.checkAccount(IspUser, driver)
                # if result=='kill' and choice[0]=="26":
                #     break

            if choice[0] == "1":
                GmailActions.checkAccount(IspUser, driver, True)
                break

            elif choice[0] == "2":
                GmailActions.prepareAccount(IspUser, driver)
                break

            elif choice[0] == "3":
                GmailActions.checkAccount(IspUser, driver, False,False,False,True)
                GmailActions.loginWait(driver)
                break
            
            elif choice[0] == "4":
                GmailActions.ReporNotSpam(driver)
                break

            elif choice[0] == "5":
                GmailActions.selectPage_notSpam(driver)
                break

            elif choice[0] == "6":
                GmailActions.inbox_openClick(driver, nbMsgs)
                break

            elif choice[0] == "7":
                GmailActions.inbox_openClickImportant(driver, nbMsgs)
                break
            
            elif choice[0] == "8":
                GmailActions.inbox_openClickStart(driver, nbMsgs)
                break

            elif choice[0] == "9":
                GmailActions.inbox_openClickImportantStart(driver, nbMsgs)
                break
            
            elif choice[0] == "10":
                GmailActions.inbox_openClickReply(driver, nbMsgs)
                break

            elif choice[0] == "11":
                GmailActions.inbox_openClickArchive(driver, nbMsgs)
                break

            elif choice[0] == "12":
                GmailActions.selectPage_notSpam_inbox_OpenClickImportantStar(driver, nbMsgs)
                break

            elif choice[0] == "13":
                GmailActions.selectPage_notSpam_inbox_OpenClickReply(driver, nbMsgs)
                break

            elif choice[0] == "14":
                GmailActions.importContact(IspUser, driver)
                break
            
            elif choice[0] == "15":
                GmailActions.changePassword(IspUser, driver)
                break

            elif choice[0] == "16":
                GmailActions.changeRecovry(IspUser, driver)
                break

            elif choice[0] == "17":
                GmailActions.changePasswordRecovry(IspUser, driver)
                break

            elif choice[0] == "18":
                GmailActions.cleanAll(driver)
                break

            elif choice[0] == "19":
                GmailActions.inbox_selectpageReadImportantStart_bySearch(driver,nbMsgs)
                break

            elif choice[0] == "20":
                GmailActions.actionByChoice(IspUser, driver, nbMsgs)

            elif choice[0] == "21":
                GmailActions.selectPage_notSpam_inbox_selectpageReadImportantStartArchive(driver,nbMsgs)
                break

            elif choice[0] == "22":
                GmailActions.inbox_openStartReply(driver,nbMsgs)
                break

            elif choice[0] == "23":
                GmailActions.notPromotions(driver,nbMsgs)
                break

            elif choice[0] =="24":
                GmailActions.randomActions(driver, nbMsgs)
                break
            elif choice[0] =="25":
                GmailActions.disable_forwarding(driver)
                break
            if choice[0] == "26":
                GmailActions.checkAccount(IspUser, driver, True, True)
                break
            if choice[0] == "27":
                GmailActions.checkAccount(IspUser, driver, True, True, True)
                break
            if choice[0] == "28":
                GmailActions.twoFactourAuth(IspUser, driver)
                break
            if choice[0] == "29":
                GmailActions.activatetwoFactour(IspUser , driver)
                break
            if choice[0] == "30":
                GmailActions.RemoveTwoFactourAuth(driver,IspUser)
                break
            if choice[0] == "31":
                GmailActions.app_password(IspUser, driver)
                break
            if choice[0] == "32":
                GmailActions.confirm_device(IspUser, driver)
                break
            if choice[0] == "33":
                GmailActions.less_secure(IspUser, driver)
                break
            if choice[0] == "34":
                GmailActions.open_youtube(driver)
                break
            if choice[0] == "35":
                GmailActions.AddFromEmails(driver)
                break
            if choice[0] == "36":
                GmailActions.search_google(driver)
                break
            if choice[0] == "37":
                GmailActions.generate_tokens(IspUser)
                break
            if choice[0] == "38":
                GmailActions.check_emails_api(IspUser)
                break
            if choice[0] == "39":
                GmailActions.api_call()
                break
            if choice[0] == "40":
                GmailActions.change_theme(driver)
                break
            if choice[0] == "41":
                GmailActions.confirm_from(driver,nbMsgs)
                break
            if choice[0] == "42":
                GmailActions.remove_phone(driver, IspUser)
                break
            if choice[0] == "43":
                GmailActions.app_script(driver, IspUser)
                break

            elif choice[0] == "0":
                break
    except:
        save_to_files("manualy_closed", IspUser.showString())
    finally:
        try:
            if driver and driver.session_id:
                driver.quit()
        except:pass




def HotmailChoices(IspUser, choice):
    try: 
        semaphore.acquire()
        while True:
            dontCheck = ["1","2","3","16", 0]
            if choice[0] !=0:
                driver = CreateDriver(IspUser)
            if choice[0] not in dontCheck:
                HotmailActions.checkAccount(IspUser, driver)

            if choice[0] == "1":
                HotmailActions.checkAccount(IspUser, driver, True)
                break

            elif choice[0] == "2":
                HotmailActions.checPAccount(IspUser, driver, True)
                break

            elif choice[0] == "3":
                HotmailActions.loginWait(IspUser, driver)
                break
            
            elif choice[0] == "4":
                HotmailActions.reportNotJunk(driver)
                break

            elif choice[0] == "5":
                HotmailActions.reportToInbox(driver)
                break

            elif choice[0] == "6":
                HotmailActions.selectPage_notJunk(driver)
                break

            elif choice[0] == "7":
                HotmailActions.inbox_openClick(driver, nbMsgs)
                break

            elif choice[0] == "8":
                HotmailActions.inbox_openCategorize(driver, nbMsgs)
                break
            
            elif choice[0] == "9":
                HotmailActions.inbox_openFlag(driver, nbMsgs)
                break

            elif choice[0] == "10":
                HotmailActions.inbox_openArchive(driver, nbMsgs)
                break
            
            elif choice[0] == "11":
                HotmailActions.inbox_openReply(driver, nbMsgs)
                break

            elif choice[0] == "12":
                HotmailActions.inbox_openClickCategorize(driver, nbMsgs)
                break

            elif choice[0] == "13":
                HotmailActions.inbox_openClickCategorizeFlag(driver, nbMsgs)
                break

            elif choice[0] == "14":
                HotmailActions.inbox_openClickCategorizeArchive(driver, nbMsgs)
                break

            elif choice[0] == "15":
                HotmailActions.inbox_openClickCategorizeReply(driver, nbMsgs)
                break
            
            elif choice[0] == "16":
                HotmailActions.inbox_openClickReplyArchive(driver, nbMsgs)
                break

            elif choice[0] == "17":
                HotmailActions.inbox_openClickReplyFlag(driver, nbMsgs)
                break
                
            elif choice[0] == "18":
                HotmailActions.archive_openFlag(driver, nbMsgs)
                break
            
            elif choice[0] == "19":
                HotmailActions.importContact(IspUser, driver)
                break
            
            elif choice[0] == "20":
                HotmailActions.changePassword(IspUser, driver)
                break
                
            elif choice[0] == "21":
                HotmailActions.cleanAll(driver)
                break
            
            elif choice[0] == "22":
                HotmailActions.actionByChoice(IspUser, driver, nbMsgs)
                break
            
            elif choice[0] == "23":
                HotmailActions.randomActions(driver, nbMsgs)
                break
            elif choice[0] == "24":
                HotmailActions.removePin(driver)
                break

            elif choice[0] == "0":
                break
    
    except:
            pass
    finally:
        # Release the semaphore permit when the task is done (driver is closed)
        semaphore.release()
        # Close driver
        driver.close()




def YahooChoices(IspUser, choice):
    try: 
        semaphore.acquire()
        while True:
            dontCheck = ["1","2","22", 0]
            if choice[0] !=0:
                driver = CreateDriver(IspUser, True)
            if choice[0] not in dontCheck:
                YahooActions.checkAccount(IspUser, driver)


            if choice[0] == "1":
                YahooActions.checkAccount(IspUser, driver, True)
                break

            elif choice[0] == "2":
                YahooActions.checkAccount(IspUser, driver, True)
                break

            elif choice[0] == "3":
                YahooActions.loginWait(driver)
                break
            
            elif choice[0] == "4":
                YahooActions.selectPage_notSpam(driver)
                break

            elif choice[0] == "5":
                YahooActions.reportNotSpam(driver)
                break

            elif choice[0] == "6":
                YahooActions.inbox_openClick(driver)
                break

            elif choice[0] == "7":
                YahooActions.inbox_openReply(driver, nbMsgs)
                break

            elif choice[0] == "8":
                YahooActions.inbox_openStar(driver, nbMsgs)
                break
            
            elif choice[0] == "9":
                YahooActions.inbox_openArchive(driver, nbMsgs)
                break

            elif choice[0] == "10":
                YahooActions.inbox_openClickStar(driver, nbMsgs)
                break
            
            elif choice[0] == "11":
                YahooActions.inbox_openClickReply(driver, nbMsgs)
                break

            elif choice[0] == "12":
                YahooActions.inbox_openClickArchive(driver, nbMsgs)
                break

            elif choice[0] == "13":
                YahooActions.inbox_openClickReplyArchive(driver, nbMsgs)
                break

            elif choice[0] == "14":
                YahooActions.inbox_openClickStarReply(driver, nbMsgs)
                break

            elif choice[0] == "15":
                YahooActions.inbox_openClickStarArchive(driver, nbMsgs)
                break
            
            elif choice[0] == "16":
                YahooActions.inbox_openClickStarReplyArchive(driver, nbMsgs)
                break

            elif choice[0] == "17":
                YahooActions.inbox_openStarReplyArchive(driver, nbMsgs)
                break

            elif choice[0] == "18":
                YahooActions.inbox_openReplyArchive(driver, nbMsgs)
                break

            elif choice[0] == "19":
                YahooActions.inbox_openStarArchive(driver, nbMsgs)
                break

            elif choice[0] == "20":
                YahooActions.inbox_allArchive(driver, nbMsgs)
                break

            elif choice[0] == "21":
                YahooActions.importContact(IspUser , driver)
                break

            elif choice[0] == "22":
                YahooActions.changePassword(IspUser , driver)
                break

            elif choice[0] == "23":
                YahooActions.cleanAll(driver)
                break
            
            elif choice[0] == "24":
                YahooActions.actionByChoice(IspUser , driver, nbMsgs)
                break

            elif choice[0] == "25":
                YahooActions.randomActions(driver, nbMsgs)
                break

            elif choice[0] == "0":
                break
    
    except:
            pass
    finally:
        # Release the semaphore permit when the task is done (driver is closed)
        semaphore.release()
        # Close driver
        driver.close()