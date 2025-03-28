# streamlit_app.py
import streamlit as st
import os
import socket
from report_generator import generate_all_documents  # 보고서+PPT+리서치 생성
from email_utils import send_email_with_attachment   # 이메일 전송 함수

# ✅ secrets.toml 또는 Streamlit Cloud의 설정값 불러오기
app_password = st.secrets.get("APP_PASSWORD", "")
email_user = st.secrets.get("EMAIL_USER", "")
email_pass = st.secrets.get("EMAIL_PASS", "")
openai_key = st.secrets.get("OPENAI_API_KEY", "")

# ✅ OpenAI 키 환경 변수 등록 (research.py에서 사용하도록)
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["EMAIL_USER"] = email_user
os.environ["EMAIL_PASS"] = email_pass

# 🧱 기본 설정
st.set_page_config(page_title="🚀 신사업 제안 보고서 생성기", layout="wide")
st.title("🔒 신사업 제안 보고서 생성 에이전트")

# 🔐 비밀번호 인증
input_pw = st.text_input("접속 비밀번호를 입력하세요", type="password")
if input_pw != app_password:
    st.warning("🚫 잘못된 비밀번호입니다.")
    st.stop()

# ✅ 메인 UI
st.title("📊 GPT 기반 신사업 제안 보고서 에이전트")
topic = st.text_input("📝 주제 입력", placeholder="예: 일본 장례 플랫폼 시장")

if st.button("🚀 보고서 생성 시작") and topic.strip():
    with st.spinner("📚 GPT 심층 리서치 및 보고서 생성 중..."):
        # 📁 문서 생성
        zip_path, zip_name = generate_all_documents(topic)

        # 🧠 로컬 환경 감지
        is_local = socket.gethostname() in ["localhost", "127.0.0.1"] or "local" in socket.getfqdn()

        # 💾 바탕화면 자동 저장 (로컬 환경인 경우)
        if is_local:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            final_path = os.path.join(desktop_path, zip_name)
            os.replace(zip_path, final_path)
            st.success(f"📁 바탕화면에 '{zip_name}' 저장 완료!")
        else:
            # 🌐 외부 환경 - 다운로드 버튼 제공
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 ZIP 파일 다운로드",
                    data=f,
                    file_name=zip_name,
                    mime="application/zip"
                )
            final_path = zip_path  # 외부일 땐 이 경로 유지

        # 📬 이메일 발송 옵션
        if st.checkbox("📬 이메일로도 전송할까요?"):
            receiver = st.text_input("✉️ 받을 이메일 주소")
            if st.button("이메일 보내기") and receiver:
                try:
                    send_email_with_attachment(
                        receiver_email=receiver,
                        subject=f"[신사업 제안서] {topic}",
                        body=f"'{topic}'에 대한 자동 생성 보고서를 첨부드립니다.",
                        file_path=final_path
                    )
                    st.success("📤 이메일 발송 완료!")
                except Exception as e:
                    st.error(f"이메일 전송 실패: {e}")
