# selenium-webdriver
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service

# seleniumエラー関係
#from selenium.common.exceptions import exceptions
#.UnexpectedAlertPresentException
# ↓Windowsのとき(もしかしたらなくても動くかも)
#import chromedriver_binary
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# GUI
import FreeSimpleGUI as sg

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

        try:
            # Mac
            # webdriver_service = Service('./chromedriver')
            # Windows
            webdriver_service = Service('./chromedriver.exe')
            self.driver = webdriver.Chrome(service=webdriver_service)
            self.driverWait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print('chromedriverの起動に失敗しました')
            print('ご利用のGoogleChromeと同じバージョンのchromedriver.exeに更新してください')
            print('・https://chromedriver.chromium.org/downloads')
            print('・https://googlechromelabs.github.io/chrome-for-testing/#stable')
            print('-------')
            print(e)
            self.driver.quit()
        
        # self.driverWait = WebDriverWait(self.driver, 10)
        
        print('Chrome init end')
        printRuledLine()

    def __del__(self):
        self.driver.quit()
        print('Chrome quit')


    def quit(self):
        self.driver.quit()
        print('Chrome quit')

    # hangeログアウト
    def hange_logout(self):
        print('ログアウト開始')
        # マイページに遷移
        self.driver.get('https://puretomo.hange.jp/')
        time.sleep(0.5)
        
        # ヘッダーのメニューボタンをクリック
        self.driver.find_element(By.CSS_SELECTOR, '#__next > div.Header_container__1RawY.undefined > header > nav > div.GlobalHeader_buttonWrap__2ro_f.GlobalHeader_login__3iuxy > a > svg > g').click()
        
        # ログアウトボタンをクリック
        self.driverWait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#__next > div.GlobalModalArea_GlobalModalArea__Uo-TC.GlobalModalArea_lightMode__16WtT > div > div > div.UserInfoMenu_LogoutBtn__1tqPf > button')))
        self.driver.find_element(By.CSS_SELECTOR, '#__next > div.GlobalModalArea_GlobalModalArea__Uo-TC.GlobalModalArea_lightMode__16WtT > div > div > div.UserInfoMenu_LogoutBtn__1tqPf > button').click()
        
        time.sleep(0.5)
        print('ログアウト完了')
        printRuledLine()

    # hangeログイン
    def hange_login(self, inputId, inputPass):
        print('ログイン開始')
        try:
            self.driver.get('https://top.hange.jp/login/?nexturl=https%3A%2F%2Fwww.hange.jp%2F')

            self.driverWait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginform > a.loginBtn')))

            loginId = self.driver.find_element(By.CSS_SELECTOR, '#strmemberid')
            loginPass = self.driver.find_element(By.CSS_SELECTOR, '#strpassword')
            loginButton = self.driver.find_element(By.CSS_SELECTOR, '#loginform > a.loginBtn')

            loginId.send_keys(inputId)
            loginPass.send_keys(inputPass)

            loginButton.click()
            
            time.sleep(0.2)
            # ログインに問題がないかマイページへの遷移で確認する
            self.driver.get('https://puretomo.hange.jp/closet/')
        except Exception as e:
            print('ログインエラー。id,パスワードを確認して再度お試しください')
            print('---- selenium エラー ----')
            print(e)

            # ログイン再開できるようにログインページに戻る
            self.driver.get('https://top.hange.jp/login/?nexturl=https%3A%2F%2Fwww.hange.jp%2F')
            return False
        
        print('ログイン完了')
        printRuledLine()
        return True

    # puretomo マネキン一覧画面に遷移
    def transition_puretomo_mannequin(self):
        print('puretomo着替えページへ遷移開始')
        self.driver.get('https://puretomo.hange.jp/closet/')
        # マイページに遷移することがあるため1秒待機してリトライ
        time.sleep(1)
        self.driver.get('https://puretomo.hange.jp/closet/')

        # マネキンボタンをクリック
        print('着替えページを表示, マネキン一覧へ遷移します')
        self.driverWait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_mainTab__1fA0U > div:nth-child(6) > button')))
        mannequinBtn = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_mainTab__1fA0U > div:nth-child(6) > button')
        mannequinBtn.click()
        print('マネキン一覧への遷移完了')
        printRuledLine()

        # 新規driverではアラートが表示されるため4秒待機して表示させた後に拒否する
        # ↓アラートのセレクタもXPATHもclass_nameもno such elementで取得できなかった
        #time.sleep(4)
        #self.driver.find_element(By.CSS_SELECTOR, 'div > div > div.buttons > button.deny').click()
        #self.driver.find_element(by=By.CLASS_NAME, value="deny")
        #wait.until(EC.alert_is_present())
        #Alert(self.driver).deny()

    # マネキン名一覧取得
    def get_mannequins(self):
        print('マネキン取得開始')
        # ページ数を取得
        page = self.driver.find_elements(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li')
        pageNum = len(page)

        mannequinNames = []
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
        printRuledLine()

        # 着替え時に前から検索できるように先頭ページに遷移しておく
        if currentPage != 1:
            firstPageButton = self.driver.find_element(By.CSS_SELECTOR, '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(2) > button')
            firstPageButton.click()

        print(mannequinNames)
        return mannequinNames

    # マネキン着替え保存
    def change_mannequin(self, changeMannequinName, inputId):
        # ページ数を取得
        page = self.driver.find_elements(By.CSS_SELECTOR,
                                         '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li'
                                         )
        pageNum = len(page)

        saveFlag = False
        currentPage = 1
        for i in range(pageNum - 2):
            # マネキン2ページ目から遷移が必要なため遷移する
            if i != 0:
                pageSelector = ('#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child('
                                + str(i + 2) + ') > button')
                pageButton = self.driver.find_element(By.CSS_SELECTOR, pageSelector)
                pageButton.click()
                currentPage += 1
                time.sleep(0.5)  # ここはそのまま（ページ遷移用）

            # 1ページあたりのマネキン数を取得
            mannequinNum = 15

            for j in range(mannequinNum):
                self.driver.implicitly_wait(5)
                # マネキン名を取得
                mannequinSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div:nth-child(' + str(
                    j + 1) + ') > p'
                mannequinName = self.driver.find_element(By.CSS_SELECTOR, mannequinSelector).text
                if mannequinName == changeMannequinName:
                    # マネキン画像をクリック
                    mannequinImageSelector = '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.mannequinList_mannequinList__2WDuH > div:nth-child(' + str(
                        j + 1) + ') > div > div'
                    mannequinImage = self.driver.find_element(By.CSS_SELECTOR, mannequinImageSelector)
                    mannequinImage.click()

                    # --- 保存ボタンが active になるまで待つ ---
                    saveButtonSelector = '#gtm_closet_save_' + str(inputId)

                    def wait_save_button_active(driver):
                        btn = driver.find_element(By.CSS_SELECTOR, saveButtonSelector)
                        classes = btn.get_attribute("class") or ""
                        # 押下可能になると AvatarViewArea_active__2upp2 が付与される
                        if "AvatarViewArea_active__2upp2" in classes:
                            return btn
                        return False

                    saveButton = self.driverWait.until(wait_save_button_active)
                    saveButton.click()
                    saveFlag = True

                    # 保存処理が走り終わってボタンが active でなくなるまで待つ
                    def wait_save_button_inactive(driver):
                        btn = driver.find_element(By.CSS_SELECTOR, saveButtonSelector)
                        classes = btn.get_attribute("class") or ""
                        # active が外れる（inactive や saveLoad など別状態になる）まで待機
                        return "AvatarViewArea_active__2upp2" not in classes

                    self.driverWait.until(wait_save_button_inactive)
                    # --- 修正ここまで（time.sleep(0.5) を廃止） ---

                    # 着替え完了でbreak
                    break
            if saveFlag == True:
                break

        # 着替え時に前から検索できるように先頭ページに遷移しておく
        if currentPage != 1:
            # ページ移動したときは早すぎて落ちるので追加で待機
            time.sleep(0.5)
            firstPageButton = self.driver.find_element(By.CSS_SELECTOR,
                                                       '#closetAreaWrap > div.areaWrap > div.closet_itemBagArea__hcoGs > div.closet_itemListMainAreaWrap__esqU- > div.pager > nav > ul > li:nth-child(2) > button')
            firstPageButton.click()


def printRuledLine():
    print('----------------------------')

# マネキンを選択して着替えられるウィンドウを表示
def mannequinChangeWindow(chrome, mannequinNames, inputId):
    # ログインフラグ
    isLogin = True

    sg.theme('Purple')   # デザインテーマの設定

    # ウィンドウに配置するコンポーネント
    layout = [[sg.Text('login_id: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Text('login_pass: ',size=(12,1)), sg.InputText(password_char="*")],
            [sg.Button('ログイン'), sg.Button('マネキン取得'), sg.Button('終了')],
            [sg.Text('----------------------------')],
            [sg.Text('マネキン一覧')]
            ]

    # マネキンボタンを追加
    addLayout = []
    for buttonName in mannequinNames:
        addLayout.append(sg.Button(buttonName, size=(10,1)))
        if len(addLayout) == 5:
            layout.append(addLayout)
            addLayout = []
    if addLayout != []:
        layout.append(addLayout)

    # ウィンドウの生成
    changeWindow = sg.Window('puretomoマネキン自動着替え(非公式)', layout)

    # イベントループ
    while True:
        event, values = changeWindow.read()
        if event == sg.WIN_CLOSED or event == '終了':
            if isLogin:
                chrome.hange_logout()
            chrome.quit()
            break
        elif event == 'ログイン':
            if isLogin:
                print('既にログインしています')
            else:
                # TODO ここには入らない, いつか整理する
                print('ここには来ない')
        elif event == 'マネキン取得':
            if isLogin:
                print('既に取得しています')
            else:
                # TODO ここには入らない, いつか整理する
                print('ログインしてください')
        elif event in mannequinNames:
            print('「' + str(event) + '」に着替えます')
            try:
                chrome.change_mannequin(str(event), inputId)
                # 連続して着替えすぎると失敗するためスリープ
                time.sleep(1)
            except Exception as e:
                print('マネキン着替え保存でエラー')
                print('短時間に着替えすぎるとサイトが追いつかず失敗することがあります')
                print('---- selenium エラー ----')
                print(e)
            printRuledLine()
            
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
            if isLogin:
                chrome.hange_logout()
            chrome.quit()
            break
        
        elif event == 'ログイン':
            if isLogin:
                print('既にログインしています')
            else:
                isLogin = chrome.hange_login(str(values[0]), str(values[1]))
                if isLogin:
                    try:
                        chrome.transition_puretomo_mannequin()
                    except Exception as e:
                        print('puretomoページへの遷移に失敗')
                        print('---- selenium エラー ----')
                        print(e)
        elif event == 'マネキン取得':
            if isLogin:
                try:
                    mannequinNames = chrome.get_mannequins()
                except Exception as e:
                    print('マネキン取得でエラー。')
                    print('chromeにダイアログが表示されている場合は拒否して再度お試しください')
                    print('---- selenium エラー ----')
                    print(e)

                    # Puretomoマネキンページに戻ってリトライできるようにする
                    chrome.transition_puretomo_mannequin()
                if len(mannequinNames) != 0:
                    window.Hide()
                    # マネキン着替え用画面を表示
                    mannequinChangeWindow(chrome, mannequinNames, str(values[0]))
                    window.UnHide()
                    break
            else:
                print('ログインしてください')

    window.close()

if __name__ == '__main__':
    main()

