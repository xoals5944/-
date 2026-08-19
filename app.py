import streamlit as st
from google import genai

# 1. 페이지 기본 설정
st.set_page_config(page_title="AI 사주 명리학 분석", page_icon="🔮", layout="centered")

# 2. 웹페이지 제목 및 설명
st.title("🔮 AI 사주 명리학 분석")
st.write("생년월일과 시간을 입력하시면 AI 사주 전문가가 명리학적으로 분석해 드립니다.")
st.markdown("---")

# 3. 사용자 입력 양식
col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input("생년월일 선택")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

with col2:
    unknown_time = st.checkbox("태어난 시간 모름")
    if unknown_time:
        birth_time = "모름"
    else:
        birth_time = st.time_input("태어난 시간")

st.markdown("---")

# 4. 분석 버튼 클릭 시 동작
if st.button("✨ 사주 분석 시작하기", use_container_width=True):
    # Secrets에서 API 키 불러오기
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API 키가 설정되지 않았습니다. Streamlit Secrets 설정을 확인해주세요.")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        
        with st.spinner("AI가 명리학 서적을 탐독하며 사주를 분석하는 중입니다..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                당신은 깊이 있는 명리학 지식을 가진 친절하고 정확한 AI 사주 전문가입니다.
                다음 사용자 정보를 바탕으로 사주를 정밀하게 분석해 주세요.

                - 생년월일: {birth_date}
                - 태어난 시간: {birth_time}
                - 성별: {gender}

                [분석 요청 항목]
                1. 사주 오행(목, 화, 토, 금, 수)의 구성과 기운
                2. 타고난 성격과 장단점
                3. 재물운과 직업운
                4. 삶의 방향성을 위한 따뜻한 조언
                """

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )

                st.success("분석이 완료되었습니다!")
                st.markdown("### 📜 사주 분석 결과")
                st.write(response.text)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")