# -*- coding: utf-8 -*-
import requests
import threading
import smtplib
from email.mime.text import MIMEText

class BalanceCheckTask:
    def __init__(self):
        pass

    def SendEmail(self):
        # e-Mail Server Setting
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용
        smtp.login('kildongra@gmail.com', 'NjdoC6%9&2')

        # Balance Check URL Setting
        url = "http://api.etherscan.io/api?module=account&action=balance&address="
        #hd_address = "0xcf398a8363fDa31eF003CcbBb9Ff66f9533F279f"
        kb_address = "0xb9954de4d4d49dfc5856dcaca8f70d6939e2e407"
        #hd_balance = round(int(requests.get(url + hd_address).json().get("result")) * 0.000000000000000001,4)
        kb_balance = round(int(requests.get(url + kb_address).json().get("result")) * 0.000000000000000001,4)

        #if hd_balance < 1 :
        #    msg = MIMEText('')
        #    msg['Subject'] = '[warning] HD wallet balance is ' + str(hd_balance)
        #    smtp.sendmail('kildongra@gmail.com', 'rsi@coinplug.com', msg.as_string())
        #    print("Send e-Mail HDCard Balance = " + str(hd_balance))

        if kb_balance < 1 :
            msg = MIMEText('')
            msg['Subject'] = '[warning] KB wallet balance is ' + str(kb_balance)
            smtp.sendmail('kildongra@gmail.com', 'rsi@coinplug.com', msg.as_string())
            print("Send e-Mail KBCard Balance = " + str(kb_balance))

        smtp.quit()

        threading.Timer(3600,self.SendEmail).start()


    # def TaskB(self):
    #     print ("Process B")
    #     threading.Timer(3, self.TaskB).start()

def main():
    print ('Anchoring Wallet Balance Chech Function')
    at = BalanceCheckTask()
    at.SendEmail()
    # at.TaskB()

if __name__ == '__main__':
    main()
