import sys
import pyttsx3
# import pywhatkit      #for opening Youtube
import speech_recognition as sr
from googlesearch import search
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowIcon(QtGui.QIcon('IMG\www.png'))
        # browser.setUrl(QUrl('http://google.com'))
        # self.setCentralWidget(browser)
        # self.showMaximized()
        self.setGeometry(200,150,1500,800)

        #Tab Bar
        self.TabBar = QTabWidget() 
        self.TabBar.setDocumentMode(True)
        self.TabBar.tabBarDoubleClicked.connect(self.Open_New_Tab) 
        self.TabBar.currentChanged.connect(self.Change_Tab) 
        self.TabBar.setTabsClosable(True) 
        self.TabBar.tabCloseRequested.connect(self.Close_tab)
        self.setCentralWidget(self.TabBar)
      
        #StatusBar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        # self.statusBar().setStyleSheet("background-color : blue")

        #Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        BackBtn = QAction("←",self)
        BackBtn.triggered.connect(lambda:self.TabBar.currentWidget().back())
        BackBtn.setStatusTip("Go Back...")
        navbar.addAction(BackBtn)

        FwdBtn = QAction("→",self)
        FwdBtn.triggered.connect(lambda:self.TabBar.currentWidget().forward())
        FwdBtn.setStatusTip("Go Forward...")
        navbar.addAction(FwdBtn)

        ReloadBtn = QAction("  ↻  ",self)
        ReloadBtn.triggered.connect(lambda:self.TabBar.currentWidget().reload())
        ReloadBtn.setStatusTip("Reload Page...")
        navbar.addAction(ReloadBtn)
        HomeBtn = QAction("Home",self)
        
        HomeBtn.triggered.connect(self.navigate_home)
        HomeBtn.setStatusTip("Go to Home...")
        navbar.addAction(HomeBtn)

        AssistBtn = QAction("Alexa",self)
        AssistBtn.triggered.connect(self.Assistant)
        AssistBtn.setStatusTip("Alexa Assistant...")
        navbar.addAction(AssistBtn)

        AddTab = QAction("+",self)
        AddTab.triggered.connect(self.Add_New_Tab)
        AddTab.setStatusTip("Add New Tab... OR Double tap on Tab Bar")
        navbar.addAction(AddTab)

        #URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStatusTip("Enter url...")
        navbar.addWidget(self.url_bar)

        navbar.setStyleSheet("QToolBar{spacing:5px;}")


        # Creating First tab---------
        self.Add_New_Tab(QUrl('http://www.google.com'), 'New Tab')
        self.show()
        # Creating First tab---------

   
    # Add New Tab
    def Add_New_Tab(self,qurl = None,label = "New Tab"):
        if qurl == None:
            qurl = 'http://www.googl.com'

        browser = QWebEngineView()
        browser.setUrl(QUrl('http://www.googl.com'))

        i = self.TabBar.addTab(browser, label) 
        self.TabBar.setCurrentIndex(i)
        browser.urlChanged.connect(lambda browser=browser:self.url_update(browser))
        browser.loadProgress.connect(lambda _, i = i ,browser = browser:self.TabBar.setTabText(i,browser.page().title()))
        browser.loadStarted.connect(self.LoadingStrt)
        browser.loadFinished.connect(self.LoadingFin)
    
    #Loding Color Start
    def LoadingStrt(self):
        self.statusBar().setStyleSheet("background-color : blue")

    #Loding Color End
    def LoadingFin(self):
        self.statusBar().setStyleSheet("background-color : white")

    # Open Tab //Double click
    def Open_New_Tab(self,i):
        if i == -1: 
            self.Add_New_Tab("New Tab") 
        
    # Change Tab
    def Change_Tab(self,i):
        qurl = self.TabBar.currentWidget().url()
        self.url_update(qurl)

    # Close Tab
    def Close_tab(self,i):
        # if self.tabs.count() < 2:
        #     return
        
    	self.TabBar.removeTab(i)
 
    def navigate_home(self):
        self.TabBar.currentWidget().setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        print(len(url))
        if url == "":
            self.TabBar.currentWidget().setUrl(QUrl(f"http://pyycoders.unaux.com/"))
        elif (url.endswith(".com")  or url.endswith(".com/") or "www." in url):
            self.TabBar.currentWidget().setUrl(QUrl(url))
        elif len(url)>10:
            for i in search(url, tld="co.in", num=10, stop=10, pause=2):
                try:
                    self.TabBar.currentWidget().setUrl(QUrl(i))
                    print(i)
                    break
                except:
                    self.TabBar.currentWidget().setUrl(QUrl(f"http://{url}.com/"))
        else:
            self.TabBar.currentWidget().setUrl(QUrl(f"http://{url}.com/"))
    
    def url_update(self,q):
        self.url_bar.setText(q.toString())

    def Assistant(self):
        #speech_Recognization
        self.statusBar().setStyleSheet("background-color : red")
        def talk(sentence):
            engine =pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice',voices[1].id)
            engine.say(sentence)
            engine.runAndWait()

        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                talk("Hii my self Alexa What can i help you")
                voice = listener.listen(source)
                command = listener.recognize_google(voice)                
           
                if "Alexa search" in command:
                    voicetext = command.replace("Alexa search",'')
                    talk(f"searching {voicetext}")
                    print(f"searching {voicetext}")
                    voiceURL = ("http://",voicetext,".com")
                    voiceURL = ''.join(voiceURL)
                    voiceURL = voiceURL.replace(" ",'')
                    self.TabBar.currentWidget().setUrl(QUrl(voiceURL))
                    print(voiceURL)
                elif 'what is your name' in command:
                    talk("My name is Alexa")  
                elif 'who are you' in command:
                    talk("I am Alexa")  
                # elif "play" in command:
                #     voicetext = command.replace("play",'')
                #     talk(f"playing {voicetext}")
                #     pywhatkit.playonyt(voicetext)
                # elif 'love' in command:
                #     talk("i love you too")  
                # elif 'you doing' in command:
                #     talk("I am Busy for searching your command")  
                else:
                    talk("Something is missing in your input")   
                          
        except :
             print("Error")
        self.statusBar().setStyleSheet("background-color : white")


app = QApplication(sys.argv)
QApplication.setApplicationName('Py_Browser')
window = MainWindow()
    
app.exec_()    