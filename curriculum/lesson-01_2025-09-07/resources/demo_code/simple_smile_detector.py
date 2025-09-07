#!/usr/bin/env python3
"""
簡化版微笑偵測演示程式
專為第一課教學設計 - 適合12歲學生觀看

這個程式比完整版更簡單，重點在於清楚展示：
1. 藍色：尋找臉部
2. 黃色：偵測微笑中
3. 綠色：確認微笑！

作者：MollysSnapAdventure 教學團隊
日期：2025年9月7日
"""

import cv2
import time

# 顏色定義 (BGR格式)
BLUE = (255, 0, 0)      # 藍色：尋找臉部
YELLOW = (0, 255, 255)  # 黃色：偵測中
GREEN = (0, 255, 0)     # 綠色：確認微笑
WHITE = (255, 255, 255) # 白色：文字

# 簡化的偵測參數
SMILE_THRESHOLD = 3  # 需要3幀確認微笑

def main():
    """簡化版微笑偵測主程式"""
    print("🏊‍♀️ 啟動 Molly 的簡化微笑偵測器！")
    print("按 'q' 退出程式")
    
    # 初始化攝影機
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 找不到攝影機！")
        return
    
    # 載入分類器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    smile_counter = 0
    
    print("📸 攝影機準備好了！看向鏡頭微笑吧！")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 鏡像翻轉
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 偵測臉部
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            current_color = BLUE  # 預設藍色
            status_text = "尋找臉部中..."
            
            for (x, y, w, h) in faces:
                # 找到臉部，改為黃色
                current_color = YELLOW
                status_text = "找到臉部！檢查微笑中..."
                
                # 在臉部區域尋找微笑
                roi_gray = gray[y:y+h, x:x+w]
                smiles = smile_cascade.detectMultiScale(
                    roi_gray, 
                    scaleFactor=1.7,
                    minNeighbors=22,
                    minSize=(25, 25)
                )
                
                # 如果偵測到微笑
                if len(smiles) > 0:
                    smile_counter += 1
                    if smile_counter >= SMILE_THRESHOLD:
                        current_color = GREEN
                        status_text = "🎉 確認微笑！游泳池獎勵！"
                else:
                    smile_counter = max(0, smile_counter - 1)
                
                # 畫臉部框架
                cv2.rectangle(frame, (x, y), (x+w, y+h), current_color, 3)
                
                # 顯示微笑偵測結果
                if len(smiles) > 0:
                    for (sx, sy, sw, sh) in smiles:
                        cv2.rectangle(frame, (x+sx, y+sy), (x+sx+sw, y+sy+sh), current_color, 2)
            
            # 如果沒有臉部，重置計數器
            if len(faces) == 0:
                smile_counter = 0
                current_color = BLUE
                status_text = "尋找臉部中..."
            
            # 顯示狀態
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, current_color, 2)
            
            # 顯示計數器（教學用）
            cv2.putText(frame, f"微笑計數: {smile_counter}/{SMILE_THRESHOLD}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
            
            # 顯示操作說明
            cv2.putText(frame, "按 'q' 退出", (10, frame.shape[0]-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
            
            # 如果確認微笑，顯示獎勵訊息
            if current_color == GREEN:
                cv2.putText(frame, "🏊‍♀️ 游泳池獎勵！", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, GREEN, 3)
            
            cv2.imshow("Molly's 簡化微笑偵測器", frame)
            
            # 檢查退出鍵
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n🏊‍♀️ 程式停止")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("👋 謝謝使用！下次見！")

if __name__ == "__main__":
    main()
