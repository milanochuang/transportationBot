# Transportation ChatBot - 幫你購票的機器人！


## 背景
:bulb:不知道你有沒有過以下經驗：
搭高鐵想知道離現在最接近時間的高鐵或者是票價，但是又很不想按進去高鐵訂票APP輸入起訖車站還有出發時間，因為這樣又要按半天，確認自己有沒有輸入錯誤或是按錯，點APP上的按鍵又很容易按錯，最後弄到自己「氣身惱命」的嗎？只要在Line或是Discord上加入Transportation ChatBot，就可以直接以自然語言查詢你想知道的資訊喔！

## 專案内容列表
- [目錄](#目錄)
- [環境設定](#環境設定)
- [使用說明](#使用說明)
- [使用者輸入範例](#使用者輸入範例)
- [相關Repositories](#相關Repositories)
- [作者](#作者)


## 目錄
Transportation ChatBot的Repository包含以下內容：

1. [Discord](https://github.com/milanochuang/transportationBot/tree/master/Discord)
2. [Data](https://github.com/milanochuang/transportationBot/tree/master/Data)
3. [ref](https://github.com/milanochuang/transportationBot/tree/master/ref)
4. [Line](https://github.com/milanochuang/transportationBot/tree/master/Line)

## 環境設定

### 註冊Loki帳號

1. 請至[卓騰語言科技](https://api.droidtown.co/)官方網站註冊帳號並登入頁面。

2. 註冊會員 

![](https://i.imgur.com/WLqveN1.jpg)

3. 註冊完成後的登入畫面

![](https://i.imgur.com/03aEksl.jpg)


4. 順利登入會員之後，藉由「加值應用」區塊的第一個圖示進入Loki應用程式。

![](https://i.imgur.com/nTf65Hp.jpg)



### 安裝套件
本專案使用了以下套件：

1. [ArticutAPI](https://pypi.org/project/ArticutAPI/)
```shell=
$ pip3 install ArticutAPI
```
* [Articut官方說明文件](https://api.droidtown.co/document/#Articut)

2. [Dateparser](https://pypi.org/project/dateparser/) 
```shell=
$ pip install dateparser
```
3. [Datetime](https://pypi.org/project/DateTime/)
```shell=
$ pip install datetime
```



## 使用說明
* 使用Discord來操作Transportation ChatBot，請點選 **Discord** 資料夾以瀏覽更多說明。
* 欲讀取已建立好的Loki意圖，請點選 **ref** 資料夾瀏覽更多說明。

## 使用者輸入範例

在Discord輸入列標記ChatBot「@幫你買票機器人」，並輸入「出來」以檢視ChatBot兩項功能的使用說明。
* 查詢「票價」：「五位大人兩位小孩，台北到台中，商務」
* 查詢「班次」：「下午三點，台南到左營」

## 相關Repositories

- [LokiHub](https://github.com/Droidtown/LokiHub) — ☑️文意理解工具＆文字轉換API

## 作者

[@milanochuang](https://github.com/milanochuang)<br/>
[@KevinKang1211](https://github.com/KevingKang1211)


## How to contribute?

歡迎[提出任何建議](https://github.com/milanochuang/transportationBot/issues/new/choose)或者Pull Request。