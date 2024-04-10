import streamlit as st
import pandas as pd
from transformers import pipeline

# نصب کتابخانه‌های مورد نیاز
# !pip install streamlit transformers pandas

# تنظیمات اولیه Streamlit
st.set_page_config(page_title="شرکت کشت و صنعت نیشکر دهخدا", page_icon="https://example.com/logo.png")

# لود کردن لوگو
logo = "https://example.com/logo.png"

# تنظیمات اولیه Chatbot
chatbot = pipeline("conversational")

# توابع برای ورودی فایل
def upload_file(file_type):
    uploaded_file = st.file_uploader(f"آپلود {file_type} (فرمت: .xlsx یا .pdf)")
    if uploaded_file is not None:
        if file_type == "Excel":
            df = pd.read_excel(uploaded_file)
        else:
            # در اینجا کد برای خواندن فایل PDF قرار داده شود
            pass
        return df

# صفحه اصلی برنامه
def main():
    st.title("خوش آمدید به Zali AI")
    st.image(logo, caption='شرکت کشت و صنعت نیشکر دهخدا', use_column_width=True)

    # ورودی فایل‌ها
    st.sidebar.title("ورودی فایل‌ها")
    file_type = st.sidebar.radio("نوع فایل", ("Excel", "PDF"))
    df = upload_file(file_type)
    
    # Chatbot
    st.sidebar.title("Chatbot")
    user_input = st.text_input("پرسش خود را وارد کنید:")
    if user_input:
        if df is not None:
            # اینجا می‌توانید کد برای پردازش سوالات از فایل اکسل یا پی‌دی‌اف قرار دهید
            pass
        else:
            response = chatbot(user_input)
            st.text("پاسخ از Zali AI:")
            st.write(response[0]['generated_text'])

if __name__ == "__main__":
    main()
