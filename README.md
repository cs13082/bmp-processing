# bmp-processing
BMPファイルを読み込み，画像処理した結果を出力します．  
あえてOpenCVなどのライブラリを使わないようにしています．

## 起動方法
```
python .\bmp-processing.py [inputBMP outputBMP [processing_number]]
```

## できる画像処理 (processing_number)
1. グレースケール（中間値法）
1. グレースケール（NTSC加重平均法）
1. 色反転
1. ぼかし
1. 画像拡縮（最近傍法）
1. 2値化
