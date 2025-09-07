#!/usr/bin/env python3
"""
教師模擬AI演示程式
當技術設備不可用時，教師可以用這個程式"扮演"AI

功能：
- 教師按鍵控制AI回應
- 模擬藍→黃→綠的色彩變化
- 提供音效和視覺提示
- 適合課堂互動演示

使用方法：
- 按 'b': 藍色（尋找臉部）
- 按 'y': 黃色（偵測微笑中）
- 按 'g': 綠色（確認微笑！）
- 按 'r': 重置
- 按 'q': 退出

作者：MollysSnapAdventure 教學團隊
"""

import tkinter as tk
from tkinter import font
import pygame
import time

class TeacherAISimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 教師AI模擬器")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # 初始化音效系統
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False
            print("音效系統未啟用")
        
        self.current_state = "searching"  # searching, detecting, confirmed
        self.smile_count = 0
        
        self.setup_ui()
        self.bind_keys()
        
    def setup_ui(self):
        """設置使用者界面"""
        # 大標題
        title_font = font.Font(size=24, weight='bold')
        self.title_label = tk.Label(
            self.root, 
            text="🤖 AI 微笑偵測模擬器",
            font=title_font,
            fg='white',
            bg='black'
        )
        self.title_label.pack(pady=20)
        
        # 狀態顯示區域
        self.status_frame = tk.Frame(self.root, bg='blue', width=600, height=200)
        self.status_frame.pack(pady=20, padx=50, fill='both', expand=True)
        self.status_frame.pack_propagate(False)
        
        # 狀態文字
        status_font = font.Font(size=36, weight='bold')
        self.status_label = tk.Label(
            self.status_frame,
            text="🔍 尋找臉部中...",
            font=status_font,
            fg='white',
            bg='blue'
        )
        self.status_label.pack(expand=True)
        
        # 計數器
        counter_font = font.Font(size=18)
        self.counter_label = tk.Label(
            self.root,
            text=f"微笑計數: {self.smile_count}/3",
            font=counter_font,
            fg='white',
            bg='black'
        )
        self.counter_label.pack(pady=10)
        
        # 操作說明
        instructions = [
            "🎮 教師操作說明：",
            "B鍵 = 藍色（尋找臉部）",
            "Y鍵 = 黃色（偵測微笑中）", 
            "G鍵 = 綠色（確認微笑！）",
            "R鍵 = 重置",
            "Q鍵 = 退出"
        ]
        
        instruction_font = font.Font(size=12)
        for instruction in instructions:
            label = tk.Label(
                self.root,
                text=instruction,
                font=instruction_font,
                fg='lightgray',
                bg='black'
            )
            label.pack()
    
    def bind_keys(self):
        """綁定鍵盤事件"""
        self.root.bind('<KeyPress-b>', lambda e: self.set_state('searching'))
        self.root.bind('<KeyPress-B>', lambda e: self.set_state('searching'))
        self.root.bind('<KeyPress-y>', lambda e: self.set_state('detecting'))
        self.root.bind('<KeyPress-Y>', lambda e: self.set_state('detecting'))
        self.root.bind('<KeyPress-g>', lambda e: self.set_state('confirmed'))
        self.root.bind('<KeyPress-G>', lambda e: self.set_state('confirmed'))
        self.root.bind('<KeyPress-r>', lambda e: self.reset())
        self.root.bind('<KeyPress-R>', lambda e: self.reset())
        self.root.bind('<KeyPress-q>', lambda e: self.quit())
        self.root.bind('<KeyPress-Q>', lambda e: self.quit())
        
        # 確保窗口可以接收鍵盤事件
        self.root.focus_set()
    
    def set_state(self, state):
        """設置AI狀態"""
        self.current_state = state
        
        if state == 'searching':
            self.status_frame.configure(bg='blue')
            self.status_label.configure(
                text="🔍 尋找臉部中...",
                bg='blue'
            )
            self.smile_count = 0
            self.play_sound('search')
            
        elif state == 'detecting':
            self.status_frame.configure(bg='yellow')
            self.status_label.configure(
                text="👀 找到臉部！檢查微笑中...",
                bg='yellow',
                fg='black'
            )
            self.smile_count += 1
            self.play_sound('detect')
            
        elif state == 'confirmed':
            self.status_frame.configure(bg='green')
            self.status_label.configure(
                text="🎉 確認微笑！游泳池獎勵！🏊‍♀️",
                bg='green',
                fg='white'
            )
            self.smile_count = 3
            self.play_sound('confirm')
            
        self.update_counter()
    
    def update_counter(self):
        """更新計數器顯示"""
        self.counter_label.configure(text=f"微笑計數: {self.smile_count}/3")
    
    def reset(self):
        """重置狀態"""
        self.smile_count = 0
        self.set_state('searching')
    
    def play_sound(self, sound_type):
        """播放音效（如果可用）"""
        if not self.sound_enabled:
            return
            
        try:
            if sound_type == 'search':
                # 模擬搜尋音效
                pass
            elif sound_type == 'detect':
                # 模擬偵測音效
                pass
            elif sound_type == 'confirm':
                # 模擬確認音效
                pass
        except:
            pass
    
    def quit(self):
        """退出程式"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """啟動模擬器"""
        print("🎮 教師AI模擬器啟動！")
        print("請將視窗設為焦點，然後使用鍵盤控制")
        self.root.mainloop()

def main():
    """主程式"""
    print("🤖 啟動教師AI模擬器")
    print("這個工具讓教師可以手動模擬AI反應")
    print("適合在技術設備不可用時使用")
    print()
    
    simulator = TeacherAISimulator()
    simulator.run()

if __name__ == "__main__":
    main()
