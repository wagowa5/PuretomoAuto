# 注意
ハンゲログインをseleniumで実施することの安全性は不明(一応seleniumで銀行系ログインとかしている人もいる https://qiita.com/yoshi2045/items/765c589ce0c02e9d888d)

利用する場合は自己責任でお願いします

# PuretomoAuto
puretomoのマネキン自動着替え

# 概要
seleniumのブラウザ操作で無理やりpuretomoのマネキン着替えを行う

# Installation
zipをダウンロードして実行ファイル実行
- mac用は現在動きません
- [Windows用](https://github.com/wagowa5/PuretomoAuto/raw/master/windows%E5%AE%9F%E8%A1%8C%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB/puretomo_auto.zip)

GoogleChromeのバージョンとchromedriver.exeのバージョンが一致していないと動きません

使用中のGoogleChromeと同じバージョンのchromedriver.exeに置き換えてください(zipに入っているchromedriver.exeは`115.0.5790.102`です)

- 最新バージョン: https://googlechromelabs.github.io/chrome-for-testing/#stable
    - 2023-07-21時点の最新: https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.102/win64/chromedriver-win64.zip
- 過去バージョン: https://chromedriver.chromium.org/downloads

------

ソースも置いてあるのでpython触れる方はソースから実行もできます
- 必要なmodule
    - selenium
    - freesimplegui
    - もしかしたらchrome関連(importでコメントアウトしているやつ)

インストール例:
```
pip install selenium FreeSimpleGUI
```



------

## GoogleChromeの自動更新でchromedriverの最新バージョンより進んでしまって動かなくなってしまった方へ
↓で使えると思います

1. [ダウンロード](https://drive.google.com/file/d/15l33FuDAyfxz1YhjrPdrfONRtxti5WUl/view?usp=sharing)
2. 1のzip展開
3. 中にあるpuretomoAuto.exeのショートカットを作成する
4. ショートカットを使いやすい場所に移動

chromedriverのバージョンと同じバージョンのテスト用Chromeを使用して動くようにしています

