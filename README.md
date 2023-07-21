# 注意
ハンゲログインをseleniumで実施することの安全性は不明(一応seleniumで銀行系ログインとかしている人もいる https://qiita.com/yoshi2045/items/765c589ce0c02e9d888d)

利用する場合は自己責任でお願いします

# PuretomoAuto
puretomoのマネキン自動着替え

# 概要
seleniumのブラウザ操作で無理やりpuretomoのマネキン着替えを行う

# Installation
zipをダウンロードして実行ファイル実行
- [mac用](https://github.com/wagowa5/PuretomoAuto/raw/master/mac%E5%AE%9F%E8%A1%8C%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB/puretomo_auto.zip)
- [Windows用](https://github.com/wagowa5/PuretomoAuto/raw/master/windows%E5%AE%9F%E8%A1%8C%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB/puretomoAuto.exe)

GoogleChromeのバージョンとchromedriver.exeのバージョンが一致していないと動きません
chromedriver.exeをインストールされているGoogleChromeのバージョンに合ったものに置き換えてください(zipに入っているのは`115.0.5790.102`です)

- 最新バージョン: https://googlechromelabs.github.io/chrome-for-testing/#stable
    - 2023-07-21時点の最新: https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.102/win64/chromedriver-win64.zip
- 過去バージョン: https://chromedriver.chromium.org/downloads

------

ソースも置いてあるのでpython触れる方はソースから実行もできます
- 必要なmodule
    - selenium
    - pysimplegui
    - もしかしたらchrome関連(importでコメントアウトしているやつ)
