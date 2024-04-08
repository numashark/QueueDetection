# print("1行目")
# 机の範囲に映ってる人だけカウントされないパターン（右側は最悪lineで制限？）
import cv2
from ultralytics import YOLO
import numpy
import picamera2


print("作動")
# 学習済みのモデルをロード
model = YOLO('yolov8n.pt')
print("動作確認")
results = model('tcp://127.0.0.1:8888', stream=True)

# 机の座標リセット
X1 = 0
X2 = 0

# 平均する要素のリセット
a1 = -1
a2 = -1
a3 = -1
a4 = -1
a5 = -1

# カウント用
number = 0

# 肩幅用
PX1 = 0
PX2 = 0

while True:
    for result,box, class_id in zip(results,bounding_boxes, class_ids):
        print("-----")
        #print(type(result))
        #print(result)
        #結果を画像に変換
        annotated_frame = result.plot()

        # results[0]からResultsオブジェクトを取り出す
        result_object = result

        # バウンディングボックスの座標を取得
        bounding_boxes = result_object.boxes.xyxy
        # print(bounding_boxes)

        # クラスIDを取得
        class_ids = result_object.boxes.cls

        # クラス名の辞書を取得
        class_names_dict = result_object.names
        
    # バウンディングボックスとクラス名を組み合わせて表示
        print("ffffffffffffffffffffffffffffff")
        class_name = class_names_dict[int(class_id)]
        x1,y1,x2,y2 = [int(i) for i in box]
        # 検知した机の端から端までの除外範囲
        if(class_id == 60):   
            X1 = x1
            X2 = x2
        # 最後尾の人の肩幅
        if(class_id == 0):   
            if((x2 - x1) > (PX2 - PX1)):
                PX1 = x1 + -2
                PX2 = x2 + 2
                print("更新された左肩",PX1,"更新された右肩",PX2,)

        print(f'Object:{class_name} Coordinates: StartX = {x1}, StartY={y1}, EndX={x2}, EndY={y2}')

        # print(f"Box coordinates: {box}, Object: {class_name}")    

        if(class_id == 0 and x1<X1 or class_id == 0 and X2<x2):
            if(class_id == 0 and PX1 <= x1 and PX2 >= x2):    
                number += 1

        # 机の座標を表示
        print("左の机の端の座標は", X1 , '、右の机の端の座標は', X2 , 'です。')
        print(number)
        print(a1)
        
        if(a4!=-1):
            a5 = number
            
        if(a3!=-1):
            a4 = number
            
        if(a2!=-1):
            a3 = number
            
        if(a1!=-1):
            a2 = number    
            
        if(a1==-1):
            a1 = number
        print("...................")
        if(a1!=-1 and a2==-1):
            print("1回目の計測結果は",a1,"人です。")
        if(a2!=-1 and a3==-1):    
            print("2回目の計測結果は",a2,"人です。")
        if(a3!=-1 and a4==-1):
            print("3回目の計測結果は",a3,"人です。")
        if(a4!=-1 and a5==-1):
            print("4回目の計測結果は",a4,"人です。")
        if(a5!=-1):
            print("5回目の計測結果は",a5,"人です。")   
            
            if(a1!=-1 and a2!=-1 and a3!=-1 and a4!=-1 and a5!=-1 ):
                print('机の間に並んでる人数（平均値）は、',(a1 + a2 + a3 + a4 + a5)/5,'人です') 
                # 平均する要素をリセット
                a1 = -1
                a2 = -1
                a3 = -1
                a4 = -1
                a5 = -1
                print("抽出した要素をそれぞれ",a1,a2,a3,a4,a5,"にリセット")
                    
            # OpenCVで表示＆キー入力チェック
            cv2.imshow("YOLOv8 Tracking ", annotated_frame)
            key = cv2.waitKey(1)
            if key != -1 : 
                print("STOP PLAY")
                break
