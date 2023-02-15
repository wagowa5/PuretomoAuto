# selenium-webdriver
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service
# ↓Windowsのとき(もしかしたらなくても動くかも)
#import chromedriver_binary
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# GUI
import PySimpleGUI as sg

# general
import time


#
# puretomo操作クラス
#
class Puretomo():
    def __init__(self):
        # chromeだと「このページの最新の通知なんとか」の
        # ダイアログが表示されることがあるのでシークレットモードで起動する
        # ↑変わらなかった
        #option = ChromeOptions()
        #option.add_argument('--incognito')  

        # Mac
        self.driver = webdriver.Chrome()
        # Windows(Windowsも↑で動きそう)
        #self.driver = webdriver.Chrome('chromedriver.exe')
        
        print('Chrome init end')

    def __del__(self):
        self.driver.quit()
        print('Chrome quit')


    def quit(self):
        self.driver.quit()
        print('Chrome quit')


    # hangeログイン
    def hange_login(self, inputId, inputPass):
        print('ログイン開始')
        self.driver.get('https://top.hange.jp/login/?nexturl=https%3A%2F%2Fwww.hange.jp%2F')

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginform > a.loginBtn')))

        loginId = self.driver.find_element(By.CSS_SELECTOR, '#strmemberid')
        loginPass = self.driver.find_element(By.CSS_SELECTOR, '#strpassword')
        loginButton = self.driver.find_element(By.CSS_SELECTOR, '#loginform > a.loginBtn')

        loginId.send_keys(inputId)
        loginPass.send_keys(inputPass)

        loginButton.click()
        print('ログイン完了')

        # puretomo着替えページに遷移
        print('puretomo着替えページへ遷移開始')
        self.driver.get('https://puretomo.hange.jp/closet/')
        # マイページに遷移することがあるため1秒待機してリトライ
        time.sleep(1)
        self.driver.get('https://puretomo.hange.jp/closet/')

        # 新規driverではアラートが表示されるため4秒待機して表示させた後に拒否する
        # ↓アラートのセレクタもXPATHもclass_nameもno such elementで取得できなかった
        #time.sleep(4)
        #self.driver.find_element(By.CSS_SELECTOR, 'div > div > div.buttons > button.deny').click()
        #self.driver.find_element(by=By.CLASS_NAME, value="deny")
        #wait.until(EC.alert_is_present())
        #Alert(self.driver).deny()

        print('着替えページを表示, マネキン一覧へ遷移します')
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_mainTab__1fA0U > div:nth-child(6) > button')))
        mannequinBtn = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_mainTab__1fA0U > div:nth-child(6) > button')
        mannequinBtn.click()
        print('マネキン一覧への遷移完了')


    # puretomo 着替え画面に遷移
    def transition_puretomo_mannequin(self):
        self.driver.get('https://puretomo.hange.jp/closet/')

        # マネキンをクリック
        mannequinBtn = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_mainTab__1fA0U > div:nth-child(6) > button')
        mannequinBtn.click()


    # マネキン名一覧取得
    def get_mannequins(self):
        print('マネキン取得開始')
        # ページ数を取得
        page = self.driver.find_elements(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li')
        pageNum = len(page)

        mannequinNames = []
        for i in range(pageNum-2):
            # マネキン2ページ目から遷移が必要なため遷移する
            if i != 0 :
                pageSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(' + str(i+2) + ') > button'
                pageButton = self.driver.find_element(By.CSS_SELECTOR, pageSelector)
                pageButton.click()
                time.sleep(0.5)

            # 1ページあたりのマネキン数を取得
            mannequins = self.driver.find_elements(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div > div')
            mannequinNum = len(mannequins)

            for j in range(mannequinNum):
                # マネキン名を取得
                mannequinSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div:nth-child(' + str(j+1) + ') > p'
                self.driver.implicitly_wait(5)
                mannequinName = self.driver.find_element(By.CSS_SELECTOR, mannequinSelector).text
                if mannequinName != '':
                    mannequinNames.append(mannequinName)

        print('マネキン名取得完了')

        # 着替え時に前から検索できるように先頭ページに遷移しておく
        firstPageButton = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(2) > button')
        firstPageButton.click()

        print(mannequinNames)
        return mannequinNames
    
    # マネキン着替え保存
    def change_mannequin(self, changeMannequinName, inputId):
        print('マネキン着替え開始')
        # ページ数を取得
        page = self.driver.find_elements(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li')
        pageNum = len(page)

        saveFlag = False
        currentPage = 1
        for i in range(pageNum-2):
            # マネキン2ページ目から遷移が必要なため遷移する
            if i != 0 :
                pageSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(' + str(i+2) + ') > button'
                pageButton = self.driver.find_element(By.CSS_SELECTOR, pageSelector)
                pageButton.click()
                currentPage += 1
                time.sleep(0.5)

            # 1ページあたりのマネキン数を取得
            # ↓でも15固定だったので定数にした
            #mannequins = self.driver.find_elements(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div > div')
            mannequinNum = 15

            for j in range(mannequinNum):
                self.driver.implicitly_wait(5)
                # マネキン名を取得
                mannequinSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div:nth-child(' + str(j+1) + ') > p'
                mannequinName = self.driver.find_element(By.CSS_SELECTOR, mannequinSelector).text
                if mannequinName == changeMannequinName:
                    # マネキン画像をクリック
                    mannequinImageSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div:nth-child(' + str(j+1) + ') > div > div'
                    mannequinImage = self.driver.find_element(By.CSS_SELECTOR, mannequinImageSelector)
                    mannequinImage.click()

                    time.sleep(0.5)

                    # 着替え保存をクリック
                    saveButtonSelector = '#gtm_closet_save_' + str(inputId)
                    saveButton = self.driver.find_element(By.CSS_SELECTOR, saveButtonSelector)
                    saveButton.click()
                    saveFlag = True
                    time.sleep(0.5)

                    # 着替え完了でbreak
                    break
            if saveFlag == True:
                break

        # 着替え時に前から検索できるように先頭ページに遷移しておく
        if currentPage != 1:
            # ページ移動したときは早すぎて落ちるので追加で待機
            time.sleep(0.5)
            firstPageButton = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(2) > button')
            firstPageButton.click()


# マネキンを選択して着替えられるウィンドウを表示
def mannequinChangeWindow(chrome, mannequinNames, inputId):
    # ログインフラグ
    isLogin = True

    sg.theme('Purple')   # デザインテーマの設定

    # ウィンドウに配置するコンポーネント
    layout = [[sg.Text('login_id: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Text('login_pass: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Button('ログイン'), sg.Button('マネキン取得'), sg.Button('終了')],
            [sg.Text('ーーーーーーーーーーーーーー')],
            [sg.Text('マネキン一覧')]
            ]
  
    # マネキンボタンを追加
    addLayout = []
    print(mannequinNames)
    for buttonName in mannequinNames:
        addLayout.append(sg.Button(buttonName, size=(10,1)))
        if len(addLayout) == 5:
            layout.append(addLayout)
            addLayout = []
    if addLayout != []:
        layout.append(addLayout)

    print(layout)

    # ウィンドウの生成
    changeWindow = sg.Window('puretomoマネキン自動着替え(非公式)', layout)

    # イベントループ
    while True:
        event, values = changeWindow.read()
        if event == sg.WIN_CLOSED or event == '終了':
            chrome.quit()
            break
        elif event == 'ログイン':
            if isLogin:
                # TODO 画面に表示
                print('既にログインしています')
            else:
                chrome.hange_login(str(values[0]), str(values[1]))
                isLogin = True
        elif event == 'マネキン取得':
            if isLogin:
                # TODO たたけないようにする
                print('tukawanai')
            else:
                # TODO 画面に表示
                print('ログインしてください')
        elif event in mannequinNames:
            print('「' + str(event) + '」に着替えます')
            chrome.change_mannequin(str(event), inputId)
            # 連続して着替えすぎると失敗するためスリープ
            time.sleep(1)
    changeWindow.close()



def main():
    sg.theme('Purple')   # デザインテーマの設定

    # ブラウザ作成
    chrome = Puretomo()

    # ログインフラグ
    isLogin = False
    # マネキン一覧
    mannequinNames = []

    # ウィンドウに配置するコンポーネント
    layout = [[sg.Text('login_id: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Text('login_pass: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Button('ログイン'), sg.Button('マネキン取得'), sg.Button('終了')]
            ]

    # ウィンドウの生成
    window = sg.Window('puretomoマネキン自動着替え(非公式)', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '終了':
            chrome.quit()
            break
        elif event == 'ログイン':
            if isLogin:
                # TODO 画面に表示
                print('既にログインしています')
            else:
                chrome.hange_login(str(values[0]), str(values[1]))
                isLogin = True
        elif event == 'マネキン取得':
            if isLogin:
                mannequinNames = chrome.get_mannequins()
                if len(mannequinNames) != 0:
                    window.Hide()
                    # マネキン着替え用画面を表示
                    mannequinChangeWindow(chrome, mannequinNames, str(values[0]))
                    window.UnHide()
                    break
            else:
                # TODO 画面に表示
                print('ログインしてください')

    window.close()

if __name__ == '__main__':
    main()

