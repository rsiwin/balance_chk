# -*- coding: utf-8 -*-
import requests
import threading
import smtplib
from email.mime.text import MIMEText

url = "http://api.etherscan.io/api?module=account&action=balance&address="
hd_address = "0xcf398a8363fDa31eF003CcbBb9Ff66f9533F279f"  #hd_balance
my_address = "0x7E7a5181FA32F99De6938a8537e3F95Ec69fAfCF"  #my_balance
kb_address = "0xb9954de4d4d49dfc5856dcaca8f70d6939e2e407"  #kb_balance
messages = ''


class BalanceCheckTask:
    CurrentBalance = 0
    DiffBalance = 0
    def __init__(self):
        pass

    def BalanceChk(self,Address):
        global CurrentBalance
        url = "http://api.etherscan.io/api?module=account&action=balance&address="
        CurrentBalance = round(int(requests.get(url + Address).json().get("result")) * 0.000000000000000001,4)

    def AnotherPeriodBalanceChk(self,Address):
        global DiffBalance
        url = "http://api.etherscan.io/api?module=account&action=balance&address="
        DiffBalance = round(int(requests.get(url + Address).json().get("result")) * 0.000000000000000001,4)
    def send_mail(self,messages):
        # e-Mail Server Setting
        global smtp
        text = messages
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kildongra@gmail.com', 'NjdoC6%9&2')
        message = MIMEText(text)
        message['Subject'] = 'Anchoring service report'
        message['From'] = 'kildongra@gmail.com'
        message['To'] = 'rsi@coinplug.com'
        smtp.sendmail('kildongra@gmail.com', 'rsi@coinplug.com', message.as_string())
        smtp.quit()

    def Balance(self):
        self.BalanceChk(kb_address)
        #print("KBCard Current Balance is " + str(CurrentBalance))
        if CurrentBalance < 1 :
            messages = "KBCard current wallet balance is " + str(CurrentBalance)
            self.send_mail(messages)
            print("KBCard current wallet balance is " + str(CurrentBalance))

        threading.Timer(60,self.Balance).start()

    def KeepAlive(self):

        # BeforeKbBalance = CurrentBalance
        if DiffBalance == CurrentBalance :
            messages = 'Check anchoring service!! \n current balance is ' + str(CurrentBalance)
            self.send_mail(messages)
            print('Check anchoring service!! \n current balance is ' + str(CurrentBalance))
        self.AnotherPeriodBalanceChk(kb_address)

        threading.Timer(120,self.KeepAlive).start()
    # def TaskB(self):
    #     print ("Process B")
    #     threading.Timer(3, self.TaskB).start()

def main():
    print ('Anchoring Wallet Balance Chech Function')
    at = BalanceCheckTask()
    at.BalanceChk(kb_address)
    at.AnotherPeriodBalanceChk(kb_address)
    at.send_mail(messages)
    at.Balance()
    at.KeepAlive()
    # at.TaskB()

if __name__ == '__main__':
    main()

