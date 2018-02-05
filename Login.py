#!/usr/bin/env python2.7
import requests
import re
import json
from Tkinter import *

import socket

class AlertBox(Frame):

    def __init__(self, master=None, text='', button=''):
        self.text = text
        self.master = master
        self.button = button

    def show(self):
        Frame.__init__(self, self.master)
        self.pack()
        Label(self, text=self.text).pack()
        quit = Button(self)
        quit["text"] = self.button
        quit["command"] =  self.quit
        quit.pack()

class Application(Frame):

    def login(self):
        self.email = self.emailBox.get()
        self.password = self.passwordBox.get()
        if self.customTuning.get() == 1:
            self.das = self.dasBox.get()
            self.arr = self.arrBox.get()
        self.quit()

    def toggleTuning(self):
        if self.customTuning.get() == 1:
            tempRow = self.row + 1
            self.dasLabel = Label(self, text='DAS')
            self.dasLabel.grid(row=tempRow, column=0)
            self.dasBox = Entry(self, width=5)
            self.dasBox.grid(row=tempRow + 1, column=0)

            self.arrLabel = Label(self, text='ARR')
            self.arrLabel.grid(row=tempRow, column=1)
            self.arrBox = Entry(self, width=5)
            self.arrBox.grid(row=tempRow + 1, column=1)

            self.irs = IntVar()
            self.irsButton = Checkbutton(
                self,
                text='IRS',
                variable=self.irs)
            self.irsButton.grid(row=tempRow - 1, column=2)

            self.ihs = IntVar()
            self.ihsButton = Checkbutton(
                self,
                text='IHS',
                variable=self.ihs)
            self.ihsButton.grid(row=tempRow, column=2)
        else:
            self.dasLabel.grid_remove()
            self.dasBox.grid_remove()
            self.arrLabel.grid_remove()
            self.arrBox.grid_remove()
            self.ihsButton.grid_remove()
            self.irsButton.grid_remove()
            
        
    def createWidgets(self):
        
        self.row = 0
        Label(self, text='Email').grid(row=self.row, column=1)
        self.row +=1
        self.emailBox = Entry(self, width=20)
        self.emailBox.grid(row=self.row, column=1)
        self.row +=1

        Label(self, text='Password').grid(row=self.row, column=1)
        self.row += 1
        self.passwordBox = Entry(self, show="*", width=20)
        self.passwordBox.grid(row=self.row, column=1)
        self.row += 1

        self.loginButton = Button(self)
        self.loginButton["text"] = "Login",
        self.loginButton["command"] = self.login
        self.loginButton.grid(row=self.row, column=1)

        self.row += 2
        self.customTuning = IntVar()
        self.customTuningButton = Checkbutton(self, text='Custom Tuning', variable=self.customTuning)
        self.customTuningButton.grid(row=self.row, column=1)
        self.customTuningButton['command'] = self.toggleTuning



    def __init__(self, master=None):
        self.username = ''
        self.password = ''
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

readyToMoveOn = False
while readyToMoveOn == False:
    root = Tk()
    root.title('Login')
    app = Application(master=root)
    app.mainloop()
    root.destroy()

    host = 'https://www.tetrisfriends.com'
    tfSession = requests.session()
    tfLoginRequest = tfSession.get(host + '/users/login.php')

    loginToken = re.search('name="token" value="(.*?)"', tfLoginRequest.content, re.MULTILINE | re.DOTALL).group(1)

    tfResponse = tfSession.post(host + '/users/process.php',
                   data={'email': app.email, 'password': app.password, 'login': '1', 'remember_me': '1', 'token': loginToken})
    if tfResponse.url == host + '/users/login.php':
        root = Tk()
        root.title('Error')
        alertBox = AlertBox(master=root, text='Something went wrong. Please try to login again.', button='Try again')
        alertBox.show()
        alertBox.mainloop()
        root.destroy()
    else:
        readyToMoveOn = True

tfLiveRequest = tfSession.get(host + '/games/Live/game.php')

loginVars = {}

loginVars['sessionId'] = re.search("sessionId.*?:.*?encodeURIComponent\('(.*?)'\)", tfLiveRequest.content,
                                   re.MULTILINE | re.DOTALL).group(1)
loginVars['sessionToken'] = re.search("sessionToken.*?:.*?encodeURIComponent\('(.*?)'\)", tfLiveRequest.content,
                                      re.MULTILINE | re.DOTALL).group(1)
loginVars['timestamp'] = re.search("timestamp.*?:.*?(\d+)", tfLiveRequest.content, re.MULTILINE | re.DOTALL).group(1)
loginVars['friendUserIds'] = re.search("friendUserIds.*?:.*?'(.*?)'", tfLiveRequest.content, re.MULTILINE | re.DOTALL).group(1)
loginVars['blockedToByUserIds'] = re.search("blockedToByUserIds.*?:.*?'(.*?)'", tfLiveRequest.content, re.MULTILINE | re.DOTALL).group(1)
loginVars['PHPSESSID'] = tfLoginRequest.cookies['PHPSESSID']
if app.customTuning.get() == 1:
    loginVars['das'] = app.das
    loginVars['ar'] = app.arr
    if app.irs.get() == 1:
        loginVars['irs'] = 'true'
    if app.ihs.get() == 1:
        loginVars['ihs'] = 'true'
credentials = json.dumps(loginVars)
credentials = str.replace(
    str.replace(
        str.replace(credentials, '", "', "\",\r\n\""),
        '{', "{\r\n"
    ),
    '}', "\r\n}"
)
fh = open("../credentials.ini", "w")
fh.writelines(credentials)
fh.close()

root = Tk()
root.title('Success')
alertBox = AlertBox(master=root, text='You have successfully logged in. You can open up Arena.exe now.', button='Close')
alertBox.show()
alertBox.mainloop()
root.destroy()
