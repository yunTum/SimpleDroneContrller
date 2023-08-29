# SimpleDroneContrller
## Tello SDK
通常の操作からコマンドでの操作に変更する
```
https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf
```

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
