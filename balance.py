# -*- coding: utf-8 -*-
import requests
import threading

url = "https://api.etherscan.io/api?module=account&action=balance&address="
hd_address = "0xcf398a8363fDa31eF003CcbBb9Ff66f9533F279f"  #hd_balance
my_address = "0x7E7a5181FA32F99De6938a8537e3F95Ec69fAfCF"  #my_balance
kb_address = "0xb9954de4d4d49dfc5856dcaca8f70d6939e2e407"  #kb_balance
chain_word = "&tag=latest&apikey="
api_key = "P8T6BGCW24W1JKIYB4VVYNHB3D3MUQ1FVI"
messages = 'Now Start!!'
tele_url = "https://api.telegram.org/bot863557793:AAE6wt7bTQMBI9YmsaThFydMf2ChQBB5IIY/sendMessage"


class BalanceCheckTask:
    CurrentBalance = 0
    DiffBalance = 0
    def __init__(self):
        pass

    def BalanceChk(self,Address):
        global CurrentBalance
        CurrentBalance = round(int(requests.get(url + Address + chain_word + api_key).json().get("result")) * 0.000000000000000001,4)

    def AnotherPeriodBalanceChk(self,Address):
        global DiffBalance
        DiffBalance = round(int(requests.get(url + Address + chain_word + api_key).json().get("result")) * 0.000000000000000001,4)

    def send_teleMsg(self,messages):
        text = messages
        params = {'chat_id': '-374074806', 'text': messages}
        res = requests.get(tele_url, params=params)


    def Balance(self):
        self.BalanceChk(kb_address)
        #print("KBCard Current Balance is " + str(CurrentBalance))
        if CurrentBalance < 1 :
            messages = "KBCard current wallet balance is " + str(CurrentBalance)
            self.send_teleMsg(messages)
            print("KBCard current wallet balance is " + str(CurrentBalance))

        threading.Timer(3600,self.Balance).start()

    def KeepAlive(self):

        # BeforeKbBalance = CurrentBalance
        if DiffBalance == CurrentBalance :
            messages = 'Check anchoring service!! \n current balance is ' + str(CurrentBalance)
            self.send_teleMsg(messages)
            print('Check anchoring service!! \n current balance is ' + str(CurrentBalance))
        self.AnotherPeriodBalanceChk(kb_address)

        threading.Timer(7200,self.KeepAlive).start()

    # def TaskB(self):
    #     print ("Process B")
    #     threading.Timer(3, self.TaskB).start()

def main():
    print ('Anchoring Wallet Balance Chech Function')
    at = BalanceCheckTask()
    at.BalanceChk(kb_address)
    at.AnotherPeriodBalanceChk(kb_address)
    at.send_teleMsg(messages)
    at.Balance()
    at.KeepAlive()
    # at.TaskB()

if __name__ == '__main__':
    main()

