import streamlit as st
import smtplib
import os
from email.message import EmailMessage

# ✅ 수정된 키 이름으로 불러오기
EMAIL_USER = st.secrets["EMAIL_ADDRESS"]
EMAIL_PASS = st.secrets["EMAIL_PASSWORD"]

def send_email_with_attachment(receiver_email: str, subject: str, body: str, file_path: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email
    msg.set_content(body)

    # 파일 첨부
    with open(file_path, 'rb') as f:
        file_data = f.read()
        filename = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='application', subtype='zip', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    print(f"✅ 이메일 전송 완료: {receiver_email}")
