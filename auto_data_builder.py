import requests
import json
import time
import os
from datetime import datetime

# Danh sách từ vựng mục tiêu Band 5.0 - 6.0. 
# Bạn có thể copy hàng nghìn từ trên mạng thả vào danh sách này.
TARGET_WORDS = [
    "analyze", "approach", "assess", "assume", "authority",
    "available", "benefit", "concept", "consistent", "context",
    "create", "data", "definition", "derived", "distribution",
    "economic", "environment", "established", "estimate", "evidence",
    "export", "factor", "financial", "formula", "function",
    "identify", "income", "indicate", "individual", "interpretation",
    "involved", "issue", "labor", "legal", "legislation",
    "major", "method", "occur", "percent", "period",
    "policy", "principle", "procedure", "process", "required",
    "research", "response", "role", "significant", "similar"
]

# Các cấu trúc Speaking Linearthinking nạp cứng vào hệ thống
SPEAKING_TIPS = [
    "A.R.E.A: Answer directly -> Give Reason -> Give Example -> Alternative/Addition.",
    "Kéo dài thời gian: 'To be honest, this isn't something I normally think about...'",
    "Đánh giá hai mặt: 'It's a double-edged sword. On the one hand..., but on the other hand...'",
    "Nêu lợi ích: 'It does wonders for my mental and physical health.'",
    "Lấy ví dụ: 'Speaking from my own experience, I vividly remember a time when...'"
]

def fetch_word_data(word):
    """Gọi API từ điển mở để lấy nghĩa và ví dụ tự động"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()[0]
            
            # Lấy định nghĩa đầu tiên tìm thấy
            meaning = data['meanings'][0]['definitions'][0]['definition']
            
            # Cố gắng lấy ví dụ, nếu không có thì để trống
            example = data['meanings'][0]['definitions'][0].get('example', 'No example provided by API.')
            
            return {
                "word": word.capitalize(),
                "meaning": meaning,
                "example": example,
                "next_review": str(datetime.now().date()), # Ngày mai bắt đầu học
                "interval": 0,
                "ease": 2.5
            }
        else:
            print(f"⚠️ Không tìm thấy dữ liệu cho từ: {word}")
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối khi tra từ {word}: {e}")
        return None

def build_database(filename="ielts_data.json"):
    print(f"🚀 Bắt đầu tự động lấy dữ liệu cho {len(TARGET_WORDS)} từ vựng...\n")
    
    vocab_database = []
    
    for i, word in enumerate(TARGET_WORDS):
        print(f"[{i+1}/{len(TARGET_WORDS)}] Đang xử lý: {word}...")
        word_data = fetch_word_data(word)
        
        if word_data:
            vocab_database.append(word_data)
            
        # Nghỉ 0.5 giây giữa mỗi lần gọi API để tránh bị chặn IP
        time.sleep(0.5)
        
    print("\n✅ Đã lấy xong dữ liệu từ vựng!")
    
    # Đóng gói toàn bộ thành cấu trúc JSON cho Web App
    app_data = {
        "vocab": vocab_database,
        "tips": SPEAKING_TIPS,
        "streak": 0,
        "last_login": str(datetime.now().date())
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(app_data, f, ensure_ascii=False, indent=4)
        
    print(f"💾 Hoàn tất! File {filename} đã được cập nhật.")
    print("👉 Bây giờ hãy chạy lệnh 'streamlit run app.py' để bắt đầu học!")

if __name__ == "__main__":
    build_database()