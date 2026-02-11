共立電子(日本・大阪・日本橋)で購入した32x16dot LED マトリックスモジュールのラズパイ用駆動アプリです。
詳しくは、[Vaphio-Magiのブログ](http://vaphiomagi.cocolog-nifty.com/blog/)を参照ください。
* dotLEDs.py...  テキスト化したパターンファイルをLED表示する(gpiozeroを使用しているので、ラズパイ5以外ではちらつく)
* dotLEDsz.py...  上記と同じだが、gpiozeroの代わりにRPi.GPIOを使用。ラズパイZero2でも問題なし
* pop.txt...      上記アプリで使用するサンプルパターンファイル。「たのしい電子工作」を縦書き表示
* nenga2.txt...    上記アプリで使用するサンプルパターンファイル。「謹賀新年　明けましておめでとうございます。」と表示(MSゴシック)
* clock16.py...    dotLEDsz.pyを使用して時計を表示するアプリ。num_MS.txtとtanni_MS.txtを使用して、表示パターンを動的に変更する例。
* num_MS.txt...    上記clock16.pyで使用する半角数字のパターンファイル
* tanni_MS.txt...  同じく、clock16.pyで使用する「年月日時分秒」のパターンファイル。

