import threading



choice = [None]

input_event = threading.Event()

def GmailMenu():
    print("╔═════════════════════════════════════════════════════════╗")
    print(" ▌║█║▌║▌▌ █║ WELCOME TO GMAIL REPORTING TOOLS ▌│║▌║║▌█║▌║█     ")
    print("╚═════════════════════════════════════════════════════════╝")
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ MENU ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
    print("[1] CREATE PROFILES || CHECK")
    print("[2] PREPARE ACCOUNTS")
    print("[3] LOGIN AND WAIT FOR MANUAL ACTIONS")
    print("[4] SPAM: OPEN MESSAGE + REPORT NOT SPAM : SEARCH")
    print("[5] SPAM: SELECT PAGE + NOT SPAM")
    print("[6] INBOX: OPEN FIRST MESSAGE + CLICK")
    print("[7] INBOX: OPEN FIRST MESSAGE + CLICK + MARK AS IMPORTANT")
    print("[8] INBOX: OPEN FIRST MESSAGE + CLICK + STAR")
    print("[9] INBOX: OPEN FIRST MESSAGE + CLICK + MARK AS IMPORTANT + STAR")
    print("[10] INBOX: OPEN FIRST MESSAGE + CLICK + REPLY")
    print("[11] INBOX: OPEN FIRST MESSAGE + CLICK + ARCHIVE")
    print("[12] SPAM: SELECT PAGE + NOT SPAM && INBOX: OPEN FIRST MESSAGE + CLICK + MARK AS IMPORTANT + STAR : SEARCH.TXT REQUIRED")
    print("[13] SPAM: SELECT PAGE + NOT SPAM && INBOX: OPEN FIRST MESSAGE + CLICK + REPLY")
    print("[14] IMPORT CONTACT: CONTACT.CSV REQUIRED")
    print("[15] CHANGE PASSWORD")
    print("[16] CHANGE RECOVERY")
    print("[17] CHANGE PASSWORD AND RECOVERY")
    print("[18] CLEAN ALL")
    print("[19] INBOX: SELECT PAGE + READ + IMPORTANT + STAR: BY SEARCH, SEARCH.TXT REQUIRED")
    print("[20] ACTIONS BY CHOICE: ACTIONS.TXT REQUIRED")
    print("[21] SPAM: SELECT PAGE + NOT SPAM && INBOX: SELECT PAGE + READ + IMPORTANT + STAR + ARCHIVE")
    print("[22] INBOX: OPEN FIRST MESSAGE + STAR + REPLY")
    print("[23] PROMOTIONS: SELECT PAGE + NOT PROMOTIONS")
    print("[24] INBOX: RANDOM ACTIONS")
    print("[25] INBOX: DISABLE FORWARDING")
    print("[26] SUPPORT: AUTO")
    print("[27] SUPPORT: MANUAL")
    print("[28] ADD 2 FACTOUR AUTH")
    print("[29] ACTIVATE 2 FACTOUR AUTH")
    print("[30] REMOVE 2 FACTOUR AUTH")
    print("[31] GENERATE APP PASSWORD")
    print("[32] CONFIRM DEVICE")
    print("[33] LESS SECURE APP:ON")
    print("[34] WATCH RANDOM VIDEOS ON YOUTUBE , LINKS.TXT REQUIRED")
    print("[35] ADD FROM EMAILS")
    print("[36] RANDOM GOOGLE SEARCH")
    print("[37] GENERATE API TOCKENS")
    print("[38] CHECK EMAIL VIA API")
    print("[39] RUN API CALL PORT:8000")
    print("[40] CHANGE THEME && UNREAD FIRST")
    print("[41] CONFIRM REPLY FROMS")
    print("[42] REMOVE PHONE NUMBER")
    print("[43] app script")
    print("[0] EXIT")

    actions = input("Enter the number of action that you want to perform: ")
    while True:
        try:
            if 0 <= int(actions) <= 43 :
                choice[0] = actions
                input_event.set()
                break
            else:
                actions = input("Invalid action. Please try again , choose an action number : ")
        except ValueError:
            actions = input("Invalid action. Please try again , choose an action number : ")
        return choice[0]


def HotmailMenu():
    print("╔═════════════════════════════════════════════════════════╗")
    print(" ▌║█║▌║▌▌ █║ WELCOME TO HOTMAIL REPORTING TOOLS ▌│║▌║║▌█║▌║█     ")
    print("╚═════════════════════════════════════════════════════════╝")
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ MENU ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
    print("[1] CREATE PROFILES")
    print("[2] CHECK ACCOUNT")
    print("[3] LOGIN AND WAIT FOR MANUAL ACTIONS")
    print("[4] SPAM: OPEN MESSAGE + NOT JUNK")
    print("[5] SPAM: OPEN MESSAGE + MOVE TO INBOX")
    print("[6] SPAM: SELECT PAGE + NOT SPAM")
    print("[7] INBOX: OPEN MESSAGE + CLICK")
    print("[8] INBOX: OPEN MESSAGE + CATEGORIZE")
    print("[9] INBOX: OPEN MESSAGE + FLAG")
    print("[10] INBOX: OPEN MESSAGE + ARCHIVE")
    print("[11] INBOX: OPEN MESSAGE + REPLY")
    print("[12] INBOX: OPEN MESSAGE + CLICK + CATEGORIZE")
    print("[13] INBOX: OPEN MESSAGE + CLICK + CATEGORIZE + FLAG")
    print("[14] INBOX: OPEN MESSAGE + CLICK + CATEGORIZE + ARCHIVE")
    print("[15] INBOX: OPEN MESSAGE + CLICK + CATEGORIZE + REPLY")
    print("[16] INBOX: OPEN MESSAGE + CLICK + REPLY + ARCHIVE")
    print("[17] INBOX: OPEN MESSAGE + CLICK + REPLY + FLAG")
    print("[18] ARCHIVE: OPEN MESSAGE + FLAG")
    print("[19] IMPORT CONTACT: CONTACT.CSV REQUIRED")
    print("[20] CHANGE PASSWORD")
    print("[21] CLEAN INBOX")
    print("[22] ACTIONS BY CHOICE: ACTIONS.TXT REQUIRED")
    print("[23] INBOX: RANDOM ACTIONS")
    print("[24] INBOX: REMOVE PINED MSGS")
    print("[0] EXIT")

    actions = input("Enter the number of action that you want to perform: ")
    while True:
        try:
            if 0 <= int(actions) <= 24 :
                choice[0] = actions
                input_event.set()
                break
            else:
                actions = input("Invalid action. Please try again , choose an action number : ")
        except ValueError:
            actions = input("Invalid action. Please try again , choose an action number : ")
        return choice[0]


def YahooMenu():
    print("╔═════════════════════════════════════════════════════════╗")
    print(" ▌║█║▌║▌▌ █║ WELCOME TO YAHOO REPORTING TOOLS ▌│║▌║║▌█║▌║█     ")
    print("╚═════════════════════════════════════════════════════════╝")
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ MENU ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
    print("[1] CREATE PROFILES")
    print("[2] CHECK ACCOUNT")
    print("[3] LOGIN AND WAIT FOR MANUAL ACTIONS")
    print("[4] SPAM: SELECT PAGE + NOT SPAM")
    print("[5] SPAM: OPEN MESSAGE + REPORT NOT SPAM")
    print("[6] INBOX: OPEN FIRST MESSAGE + CLICK")
    print("[7] INBOX: OPEN FIRST MESSAGE + REPLY")
    print("[8] INBOX: OPEN FIRST MESSAGE + START")
    print("[9] INBOX: OPEN FIRST MESSAGE + ARCHIVE")
    print("[10] INBOX: OPEN FIRST MESSAGE + CLICK + STAR")
    print("[11] INBOX: OPEN FIRST MESSAGE + CLICK + REPLY")
    print("[12] INBOX: OPEN FIRST MESSAGE + CLICK + ARCHIVE")
    print("[13] INBOX: OPEN FIRST MESSAGE + CLICK + REPLY + ARCHIVE")
    print("[14] INBOX: OPEN FIRST MESSAGE + CLICK + STAR + REPLY")
    print("[15] INBOX: OPEN FIRST MESSAGE + CLICK + STAR + ARCHIVE")
    print("[16] INBOX: OPEN FIRST MESSAGE + CLICK + STAR + REPLY + ARCHIVE")
    print("[17] INBOX: OPEN FIRST MESSAGE + STAR + REPLY + ARCHIVE")
    print("[18] INBOX: OPEN FIRST MESSAGE + REPLY + ARCHIVE")
    print("[19] INBOX: OPEN FIRST MESSAGE + START + ARCHIVE")
    print("[20] INBOX: SELECTALL + ARCHIVE")
    print("[21] IMPORT CONTACT: CONTACT.CSV REQUIRED")
    print("[22] CHANGE PASSWORD")
    print("[23] CLEAN ALL")
    print("[24] ACTIONS BY CHOICE: ACTIONS.TXT REQUIRED")
    print("[25] INBOX: RANDOM ACTIONS")
    print("[0] EXIT")

    actions = input("Enter the number of action that you want to perform: ")
    while True:
        try:
            if 0 <= int(actions) <= 25 :
                choice[0] = actions
                input_event.set()
                break
            else:
                actions = input("Invalid action. Please try again , choose an action number : ")
        except ValueError:
            actions = input("Invalid action. Please try again , choose an action number : ")
        return choice[0]
