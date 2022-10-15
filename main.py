# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
# pip install selenium
# http://chromedriver.storage.googleapis.com/index.html


import webbrowser
import os,sys
import platform
import pyperclip
# 多线程
import _thread
import csv
#from operator import imod
#from sre_parse import FLAGS
from time import sleep
import time
#from tkinter import getdouble
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import datetime
import sys
import tkinter.messagebox as msgbox
# 导入/GUI 和模块和小工具
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from SD_Code import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# 设置为全局小部件
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        # 判断语言
        self.LanguageID = 0
        # 定义双语
        self.Language_Double = bool
        # 日志文本
        self.logTextEdit = ''

        # INFO_CVS信息列表
        self.info_Data = {}
        # 加入QQ群
        self.ui.JoinQQGroup_Button.clicked.connect(self.JoinQQGroup)
        # 复制邮箱
        self.ui.CopyEmail_Button.clicked.connect(self.CopyEmail)
        # 开始运行按钮
        self.ui.Run_Button.clicked.connect(self.run)

        # 读取csv文件
        self.read_info_csv()

        # 监听按钮动态
        self.ui.SelectLanguage.valueChanged.connect(self.SelectLanguage)
        self.SelectLanguage()

        # 使用自定义标题栏 | 在 MAC 或 LINUX 中用作“假”
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True


        # 切换菜单
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # 设置 UI 定义
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget 参数
        # ///////////////////////////////////////////////////////////////
        #widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 按钮点击
        # ///////////////////////////////////////////////////////////////

        # 左侧菜单
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)

        # 额外的左框
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # 额外的右框
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseLeftBox)

        # 显示应用
        # ///////////////////////////////////////////////////////////////
        self.show()

        # 设置自定义主题
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # 设置主题和技巧
        if useCustomTheme:
            # 加载和应用样式
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # 设置主页并选择菜单
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        self.ui.Bug_Button.clicked.connect(self.Bug_Button_Click)
        self.ui.JuanZengButton.clicked.connect(self.JuanZengButton_click)
    # 监听语言选择按钮动态
    def SelectLanguage(self):
        LanguageValue=self.ui.SelectLanguage.value() + 1
        #print(self.info_Data.get('Info')[LanguageValue])
        # 如果不是中文模式切换标签
        if LanguageValue == 1:
            self.ui.QQGroup.show()
            self.ui.QQGroup_Label.show()
            self.ui.JoinQQGroup_Button.show()
        else:
            self.ui.QQGroup.hide()
            self.ui.QQGroup_Label.hide()
            self.ui.JoinQQGroup_Button.hide()
            # GET BUTTON CLICKED
            #btn = self.sender()
            #btnName = btn.objectName()
            # SHOW NEW PAGE
            #if btnName == "btn_save":
            #widgets.stackedWidget.setCurrentWidget(widgets.JuanZeng) # SET PAGE
            #UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            #btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        self.printlog(self.info_Data.get('GetInfo')[LanguageValue])
        # 设置版本信息
        self.ui.Version_Label.setText(self.info_Data.get('Version')[LanguageValue])
        self.ui.version.setText(self.info_Data.get('Version')[LanguageValue])
        # 设置更新信息
        self.ui.UPDataTime_Label.setText(self.info_Data.get('UPDataTime')[LanguageValue])
        # 设置Github信息
        self.ui.GitHub_Label.setText(self.info_Data.get('GitHub')[LanguageValue])
        # 设置QQ群信息
        self.ui.QQGroup_Label.setText(self.info_Data.get('JoinQQGroupURL')[LanguageValue])
        # 设置邮箱信息
        self.ui.Email_Label.setText(self.info_Data.get('Email')[LanguageValue])
        # 版本信息更新完毕
        self.printlog(self.info_Data.get('InfodateUpOK')[LanguageValue])
        
        # 作者名字
        #print (self.info_Data.get('Credits')[LanguageValue])
        self.ui.creditsLabel.setText(self.info_Data.get('Credits')[LanguageValue])
        self.ui.toggleButton.setText(self.info_Data.get('Hide')[LanguageValue])
        self.ui.btn_home.setText(self.info_Data.get('Home')[LanguageValue])
        self.ui.btn_widgets.setText(self.info_Data.get('Help')[LanguageValue])
        self.ui.btn_new.setText(self.info_Data.get('Feedback')[LanguageValue])
        self.ui.btn_save.setText(self.info_Data.get('About')[LanguageValue])
        self.ui.btn_exit.setText(self.info_Data.get('Donate')[LanguageValue])
        self.ui.toggleLeftBox.setText(self.info_Data.get('other')[LanguageValue])
        self.ui.Run_Button.setText(self.info_Data.get('Start')[LanguageValue])
        self.ui.Double_Language.setText(self.info_Data.get('Bilingual')[LanguageValue])
        self.ui.Log_Lable.setText(self.info_Data.get('Log')[LanguageValue])

        # 应用名称
        self.setWindowTitle(self.info_Data.get('WindowTitle')[LanguageValue])
        widgets.titleRightInfo.setText(self.info_Data.get('AppName')[LanguageValue])
        widgets.titleLeftApp.setText(self.info_Data.get('L_Name')[LanguageValue])
        widgets.titleLeftDescription.setText(self.info_Data.get('WEBGUINAME')[LanguageValue])
        self.ui.abouts.setText(self.info_Data.get('About')[LanguageValue])
        self.ui.feature.setText(self.info_Data.get('feature')[LanguageValue])
        self.ui.UsingHelp.setText(self.info_Data.get('UsingHelp')[LanguageValue])
        self.ui.statement.setText(self.info_Data.get('statement')[LanguageValue])
        self.ui.planning.setText(self.info_Data.get('planning')[LanguageValue])
        self.ui.RelatedStatements.setText(self.info_Data.get('RelatedStatements')[LanguageValue])
        self.ui.RelatedStatementsTEXT.setText(self.info_Data.get('RelatedStatementsTEXT')[LanguageValue])
        self.ui.Web.setText(self.info_Data.get('Web')[LanguageValue])
        self.ui.WebTEXT.setText(self.info_Data.get('WebTEXT')[LanguageValue])
        self.ui.updateinfo.setText(self.info_Data.get('updateinfo')[LanguageValue])
        self.ui.updateinfoTEXT.setText(self.info_Data.get('updateinfoTEXT')[LanguageValue])
        self.ui.Bug_Button.setText(self.info_Data.get('Bug_Button')[LanguageValue])
        self.ui.BUGTextEdit.setText(self.info_Data.get('BUGTextEdit')[LanguageValue])
        self.ui.Version_Label_2.setText(self.info_Data.get('Version_Label_2')[LanguageValue])
        self.ui.UPDataTime_Label_2.setText(self.info_Data.get('UPDataTime_Label_2')[LanguageValue])
        self.ui.Github_Label.setText(self.info_Data.get('Github_Label')[LanguageValue])
        self.ui.QQGroup.setText(self.info_Data.get('QQGroup')[LanguageValue])
        self.ui.JoinQQGroup_Button.setText(self.info_Data.get('JoinQQGroup_Button')[LanguageValue])
        self.ui.Email_Label_2.setText(self.info_Data.get('Email_Label_2')[LanguageValue])
        self.ui.CopyEmail_Button.setText(self.info_Data.get('CopyEmail_Button')[LanguageValue])
        self.ui.JuanZeng_Label.setText(self.info_Data.get('JuanZeng_Label')[LanguageValue])
        self.ui.JuanZengButton.setText(self.info_Data.get('JuanZengButton')[LanguageValue])


    # BUG反馈
    def Bug_Button_Click(self):
        webbrowser.open(self.info_Data.get('BUGURL')[self.ui.SelectLanguage.value()+1])

    # 捐赠
    def JuanZengButton_click(self):
        webbrowser.open(self.info_Data.get('JuanZengButtonURL')[self.ui.SelectLanguage.value()+1])
    
    # 加入QQ群
    def JoinQQGroup(self):
        webbrowser.open(self.JoinQQGroupURL)

    # 复制邮箱
    def CopyEmail(self):
        pyperclip.copy(self.info_Data.get('Email')[self.ui.SelectLanguage.value()+1])
        self.ui.CopyEmail_Button.setText(self.info_Data.get('copied')[self.ui.SelectLanguage.value()+1])
    # 按钮点击
    # 在此处发布您单击按钮的功能
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.bugFK) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # SHOW NEW PAGE
        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.Aubou_Page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        # SHOW NEW PAGE
        if btnName == "btn_exit":
            if self.ui.SelectLanguage.value() == 0:
                widgets.stackedWidget.setCurrentWidget(widgets.Love_Page) # SET PAGE
                UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            else:
                widgets.stackedWidget.setCurrentWidget(widgets.JuanZeng) # SET PAGE
                UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        #if btnName == "btn_save":
        #    print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # 读取翻译csv文件
    def read_info_csv(self):
        self.info_Data.clear()
        with open('info.csv', mode='r',encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            #print(reader)
            for line in reader:
                self.info_Data[line[0]] = [line[1],line[2],line[3],line[4]]
        #print (self.info_Data)


    # 程序开始运行
    def run(self):
        # 时间验证
        #verification()
        # 获取当前所选择的语言
        #GetLanguage = self.ui.SelectLanguage.value()
        #print (GetLanguage)
        # 获取双语状态栏 True为双语 False为单语
        #GetLanguage_Double = self.ui.Double_Language.isChecked()
        # -1英文 0中文 1日文 2韩文
        if self.ui.SelectLanguage.value() == -1:
            _thread.start_new_thread( openAI, () )
        else:
            _thread.start_new_thread( localization, (self.ui.SelectLanguage.value(),self.ui.Double_Language.isChecked()) )

    # 日志输出
    def printlog(self,text):
        #currentTimeTemp = self.currentTime()
        self.ui.log.addItem('%s：%s'%(self.currentTime(),text))
        # 自动滚动到最后一行
        self.ui.log.setCurrentRow(self.ui.log.count() - 1)
        # 更改文字颜色
        self.ui.log.item(self.ui.log.count()-1).setForeground(QBrush(QColor(255, 255, 255))) 

    #获取时间
    def currentTime(self):
        return time.strftime("%H:%M:%S",time.localtime(time.time()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())



