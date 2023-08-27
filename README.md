# SimpleDroneContrller

## 外部ライブラリ
```
・PySimpleGUI
```

## 起動方法
### TelloController
通常モードの起動
```
python main.py
```

テストモードでの起動
```
python main.py testmode
```

### テストサーバー
テストを行う場合には、TelloControllerよりも先にテストサーバーを立ち上げること
testserverフォルダ配下
```
python server.py
```