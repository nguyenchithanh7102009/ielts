import streamlit as st
import json
import os
from datetime import datetime, timedelta
import random
from gtts import gTTS  # <--- Thêm dòng này
import io              # <--- Thêm dòng này

# --- 1. CẤU HÌNH & DỮ LIỆU ---
DATA_FILE = "ielts_data.json"

# Bộ từ vựng khởi tạo (Mức độ 5.0 - 6.0). Bạn có thể thêm 7000 từ vào đây.
INITIAL_VOCAB = [
    {"word": "Crucial", "meaning": "Rất quan trọng", "example": "It is crucial to practice speaking every day.", "next_review": str(datetime.now().date()), "interval": 0, "ease": 2.5},
    {"word": "Beneficial", "meaning": "Có lợi", "example": "Reading books is highly beneficial for mental health.", "next_review": str(datetime.now().date()), "interval": 0, "ease": 2.5},
    {"word": "Tackle", "meaning": "Giải quyết", "example": "The government needs to tackle environmental issues.", "next_review": str(datetime.now().date()), "interval": 0, "ease": 2.5},
    {"word": "Widespread", "meaning": "Lan rộng, phổ biến", "example": "There is widespread support for the new policy.", "next_review": str(datetime.now().date()), "interval": 0, "ease": 2.5},
    {"word": "Vital", "meaning": "Sống còn, thiết yếu", "example": "Water is vital for human survival.", "next_review": str(datetime.now().date()), "interval": 0, "ease": 2.5}
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"vocab": INITIAL_VOCAB, "streak": 0, "last_login": str(datetime.now().date())}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load data vào Session State
if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

# Cập nhật chuỗi ngày học liên tục (Streak)
today_str = str(datetime.now().date())
if st.session_state.app_data["last_login"] != today_str:
    last_login_date = datetime.strptime(st.session_state.app_data["last_login"], "%Y-%m-%d").date()
    if datetime.now().date() - last_login_date == timedelta(days=1):
        st.session_state.app_data["streak"] += 1
    else:
        st.session_state.app_data["streak"] = 0
    st.session_state.app_data["last_login"] = today_str
    save_data(st.session_state.app_data)


# --- 2. GIAO DIỆN WEB ---
st.set_page_config(page_title="Hành Trình IELTS 6.0", layout="wide")
st.title("🚀 Tốc Chiến IELTS 6.0 trong 8 Tháng")
st.sidebar.header(f"🔥 Streak: {st.session_state.app_data['streak']} ngày liên tục")

# Tạo 2 tab chính
tab1, tab2 = st.tabs(["📚 Flashcard Từ Vựng (SRS)", "🎙️ Luyện Speaking (Tự kiểm tra)"])

# --- TAB 1: HỌC TỪ VỰNG ---
with tab1:
    st.header("Ôn tập & Học mới mỗi ngày")
    
    due_cards = [word for word in st.session_state.app_data["vocab"] 
                 if datetime.strptime(word["next_review"], "%Y-%m-%d").date() <= datetime.now().date()]
    
    if not due_cards:
        st.success("🎉 Bạn đã hoàn thành xuất sắc mục tiêu từ vựng hôm nay! Hãy nghỉ ngơi hoặc chuyển sang Speaking.")
    else:
        st.write(f"**Số từ cần ôn hôm nay: {len(due_cards)}**")
        current_card = due_cards[0]
        
        st.markdown("---")
        st.subheader(f"🔤 Từ vựng: **{current_card['word']}**")
        
        # --- NÚT PHÁT ÂM AUDIO ---
        if st.button("🔊 Nghe phát âm"):
            tts = gTTS(text=current_card['word'], lang='en', tld='co.uk') # Giọng Anh-Anh (chuẩn IELTS)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
        # -------------------------

        if st.button("Lật thẻ xem đáp án"):
            st.info(f"**Nghĩa:** {current_card['meaning']}")
            st.warning(f"**Ví dụ:** {current_card['example']}")
            
            # --- NÚT ĐỌC CÂU VÍ DỤ ---
            if st.button("🔊 Nghe đọc câu ví dụ"):
                tts_ex = gTTS(text=current_card['example'], lang='en', tld='co.uk')
                audio_bytes_ex = io.BytesIO()
                tts_ex.write_to_fp(audio_bytes_ex)
                st.audio(audio_bytes_ex, format='audio/mp3', autoplay=True)
            # -------------------------
            
            st.write("**Đánh giá mức độ nhớ của bạn:**")
            col1, col2, col3 = st.columns(3)
            
            def update_card(quality):
                if quality == 1:
                    current_card['interval'] = 1
                    current_card['ease'] = max(1.3, current_card['ease'] - 0.2)
                elif quality == 2:
                    current_card['interval'] = max(1, current_card['interval'] * 2)
                else:
                    current_card['interval'] = max(1, int(current_card['interval'] * current_card['ease']))
                    current_card['ease'] += 0.1
                
                next_date = datetime.now() + timedelta(days=current_card['interval'])
                current_card['next_review'] = str(next_date.date())
                save_data(st.session_state.app_data)
                st.rerun()

            with col1:
                if st.button("🔴 Khó (Quên sạch)", use_container_width=True): update_card(1)
            with col2:
                if st.button("🟡 Bình thường (Hơi vấp)", use_container_width=True): update_card(2)
            with col3:
                if st.button("🟢 Dễ (Nhớ rõ)", use_container_width=True): update_card(3)


# --- TAB 2: LUYỆN SPEAKING KHÔNG CẦN AI ---
with tab2:
    st.header("Luyện phản xạ với cấu trúc A.R.E.A")
    st.write("Hệ thống sẽ lấy ngẫu nhiên 3 từ vựng của bạn để ép bạn sử dụng trong câu trả lời.")
    
    questions = [
        "What do you usually do in your free time?",
        "Do you prefer traveling alone or with a group?",
        "How has technology changed the way people study?",
        "Describe a place you have visited that left a strong impression on you.",
        "What are the benefits of playing video games?"
    ]
    
    if st.button("🎲 Bốc câu hỏi mới"):
        st.session_state.current_q = random.choice(questions)
        vocab_pool = [v["word"] for v in st.session_state.app_data["vocab"]]
        random.shuffle(vocab_pool)
        st.session_state.target_words = vocab_pool[:3] if len(vocab_pool) >= 3 else vocab_pool
        
    if "current_q" in st.session_state:
        st.markdown(f"### ❓ Câu hỏi: *{st.session_state.current_q}*")
        st.markdown(f"🎯 **Nhiệm vụ:** Trả lời to thành tiếng và cố gắng lồng ghép 3 từ này: **{', '.join(st.session_state.target_words)}**")
        
        st.markdown("---")
        st.write("✅ **Tự kiểm tra (Self-Checklist) sau khi nói:**")
        st.checkbox("Tôi đã dùng mẫu câu kéo dài thời gian (To be honest, ...)")
        st.checkbox("Tôi đã trả lời trực tiếp vấn đề (Answer)")
        st.checkbox("Tôi đã giải thích bằng cấu trúc 'It allows me to...' (Reason)")
        st.checkbox("Tôi đã lấy ví dụ từ bản thân (Speaking from my own experience...)")
        st.checkbox("Tôi đã nhét được ít nhất 1 từ khóa được giao vào bài")