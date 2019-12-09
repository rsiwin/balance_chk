# -*- coding: utf-8 -*-
#ver 2.3
import requests
import threading
from datetime import datetime
import time
# import telebot

urlPath = "api.etherscan.io/api?module=account&action=balance&address="
# walletAddress = "0xcf398a8363fDa31eF003CcbBb9Ff66f9533F279f"  #hd_balance
# walletAddress = "0x7E7a5181FA32F99De6938a8537e3F95Ec69fAfCF"  #my_balance
walletAddress = "0xb9954de4d4d49dfc5856dcaca8f70d6939e2e407"  #kb_balance
chainWord = "&tag=latest&apikey="
apiKey = "P8T6BGCW24W1JKIYB4VVYNHB3D3MUQ1FVI"  # Etherscan api key
messages = 'Now Start!!'
telegramUrl = "api.telegram.org/bot863557793:AAE6wt7bTQMBI9YmsaThFydMf2ChQBB5IIY/sendMessage"  # KBCard_bot
chatId = '-374074806'  # KBCard_bot
# telegramUrl = "api.telegram.org/bot714038713:AAFboAudydMIE1IqEMvkSIeSwWhK8M17uPA/sendMessage"  # HDDisplay_bot
# chatId = '-1001406704890'  # HDDisplay_bot

CheckPeriod = 3600 # unit = sec
CountInList = 5    # unit = ea
LowBalance = 0.5   # unit = Eth

balanceInList = list()
messages = 'Now Start!!'


def CurTime():
    global disCurrentTime
    disCurrentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(disCurrentTime)
    return (disCurrentTime)

print (CurTime())

class BalanceCheckTask:
    CurrentBalance = 0
    def __init__(self):
        pass

    def BalanceChk(self,Address):
        global CurrentBalance
        CurrentBalance = round(int(requests.get(b'https://' + urlPath + Address + chainWord + apiKey).json().get('result')) * 0.000000000000000001,4)
        global balanceInList
        # balanceInList.insert(0,CurrentBalance)
        if len(balanceInList) == 5 :
                balanceInList.pop() # List내마지막 요소 삭제

    def send_teleMsg(self,messages):
        text = messages
        params = {'chat_id': chatId, 'text': messages}
        res = requests.get(b'https://' + telegramUrl, params=params)

    def Balance(self):
        self.BalanceChk(walletAddress)

        if len(balanceInList) < CountInList-1 and CurrentBalance > LowBalance:
            balanceInList.insert(0,CurrentBalance)
        elif len(balanceInList) < CountInList-1 and CurrentBalance < LowBalance:
            messages = "KBCard current wallet balance is too low : " + str(CurrentBalance)
            self.send_teleMsg(messages)
            print(str(CurTime()) + '  KBCard current wallet balance is too low ' + str(CurrentBalance))
            balanceInList.insert(0,CurrentBalance)
        elif len(balanceInList) >= CountInList-1 and CurrentBalance > LowBalance:
            balanceInList.insert(0,CurrentBalance)
            balanceInList.pop()
            if balanceInList[0] == balanceInList[-1] :
                messages = 'Check anchoring service!! \n current balance is ' + str(CurrentBalance)
                self.send_teleMsg(messages)
                print(str(CurTime()) +'  Check anchoring service!! \n current balance is ' + str(CurrentBalance))
        else:
            messages = "KBCard current wallet balance is too low : " + str(CurrentBalance)
            self.send_teleMsg(messages)
            print(str(CurTime()) +'  KBCard current wallet balance is too low ' + str(CurrentBalance))
            balanceInList.insert(0,CurrentBalance)
            balanceInList.pop()
            if balanceInList[0] == balanceInList[-1] :
                messages = 'Check anchoring service!! \n current balance is ' + str(CurrentBalance)
                self.send_teleMsg(messages)
                print(str(CurTime()) +'  Check anchoring service!! \n current balance is ' + str(CurrentBalance))

        threading.Timer(CheckPeriod,self.Balance).start()   #매 주기마다 Balance Check

def main():
    print ('Anchoring Wallet Balance Chech Function')
    at = BalanceCheckTask()
    at.BalanceChk(walletAddress)
    at.send_teleMsg(messages)
    at.Balance()

if __name__ == '__main__':
    main()
