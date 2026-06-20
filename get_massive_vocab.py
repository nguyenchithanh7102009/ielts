import requests
import json
import time
from datetime import datetime

# Link kho dữ liệu 10.000 từ vựng tiếng Anh phổ biến nhất trên Github
URL_10K_WORDS = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"

def download_words():
    print("🌍 Đang tải kho từ vựng từ GitHub...")
    response = requests.get(URL_10K_WORDS)
    if response.status_code == 200:
        words = response.text.splitlines()
        # Chỉ lấy từ dài trên 4 chữ cái (bỏ các từ quá dễ như a, an, the, he, she)
        # Và giới hạn lấy 3000 từ đầu tiên (đủ để thi IELTS 6.5)
        filtered_words = [w for w in words if len(w) > 4][:3000]
        print(f"✅ Đã lọc ra {len(filtered_words)} từ cốt lõi nhất.")
        return filtered_words
    else:
        print("❌ Lỗi khi tải dữ liệu.")
        return []

def fetch_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()[0]
            meaning = data['meanings'][0]['definitions'][0]['definition']
            example = data['meanings'][0]['definitions'][0].get('example', 'No example.')
            return {
                "word": word.capitalize(),
                "meaning": meaning,
                "example": example,
                "next_review": str(datetime.now().date()),
                "interval": 0,
                "ease": 2.5
            }
    except Exception:
        pass
    return None

def build_database():
    target_words = download_words()
    if not target_words: return

    vocab_database = []
    print("\n🚀 Bắt đầu tra từ điển tự động. Sẽ mất khoảng 30 phút. Bạn cứ treo máy nhé...")
    
    for i, word in enumerate(target_words):
        # In tiến độ ra màn hình cho đỡ chán
        if i % 10 == 0:
            print(f"🔄 Đang xử lý: {i}/{len(target_words)} từ...")
            
        word_data = fetch_meaning(word)
        if word_data:
            vocab_database.append(word_data)
        
        # Ngủ 0.5s để không bị block API
        time.sleep(0.5)
        
    # Lưu vào database của app
    try:
        with open("ielts_data.json", "r", encoding="utf-8") as f:
            app_data = json.load(f)
    except FileNotFoundError:
        app_data = {"vocab": [], "streak": 0, "last_login": "", "tips": []}

    app_data["vocab"].extend(vocab_database)
    
    with open("ielts_data.json", "w", encoding="utf-8") as f:
        json.dump(app_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n🎉 HOÀN TẤT! Đã bơm thành công {len(vocab_database)} từ vựng chuẩn xịn vào ứng dụng của bạn.")

if __name__ == "__main__":
    build_database()