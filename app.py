import streamlit as st
from google import genai

# 1. 페이지 기본 설정 (타이틀 및 레이아웃)
st.set_page_config(page_title="AI와 함께하는 재미있고 쉬운 사주풀이", page_icon="🔮", layout="centered")

# 2. 웹페이지 상단 제목 및 안내문
st.title("🔮 AI 재미있고 쉽게 즐겨보는 사주!")
st.write("생년월일과 시간을 입력하시면 누구나 이해하기 쉽게 사주를 풀어드립니다.")
st.markdown("---")

# 3. 사용자 입력 양식 (숫자 직접 입력 방식)
user_name = st.text_input("이름(또는 닉네임) 입력", placeholder="예: 홍길동")

col1, col2 = st.columns(2)

with col1:
    birth_date = st.text_input("생년월일 입력", placeholder="예: 19960515 또는 1996-05-15")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

with col2:
    unknown_time = st.checkbox("태어난 시간 모름")
    if unknown_time:
        birth_time = "모름"
    else:
        birth_time = st.text_input("태어난 시간 입력", placeholder="예: 07:40 또는 14:30")

st.markdown("---")

# 4. 분석 버튼 클릭 시 동작
if st.button("✨ 쉽고 재미있는 사주 보기", use_container_width=True):
    if not birth_date:
        st.warning("생년월일을 입력해 주세요.")
    elif "GEMINI_API_KEY" not in st.secrets:
        st.error("API 키가 설정되지 않았습니다. Streamlit Secrets 설정을 확인해주세요.")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        
        with st.spinner("AI가 당신의 사주를 가장 쉽고 재미있게 해석하는 중입니다..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # 초등학생도 한눈에 이해할 수 있는 쉬운 설명 프롬프트
                prompt = f"""
                당신은 복잡하고 어려운 사주 용어를 세상에서 가장 쉽고 재미있게 설명해 주는 태민사주 입니다.
                다음 사용자 정보를 바탕으로 사주를 분석해 주세요.

                - 생년월일: {birth_date}
                - 태어난 시간: {birth_time}
                - 성별: {gender}

                [작성 가이드라인 - 필수]
                1. 한자어나 용어는 사용하지 말아주세요. 만약 사용하게 된다면 해석을 알아듣기 쉽게 해주세요.
                2. 어렵고 복잡한 명리학 용어(십성, 용신, 신살, 격국, 갑목, 병화 등)는 사용하되 알아들을수 있게 해석해서 알려주세요.
                3. AI 같지 않고 전문적으로 알려주세요
                4. 타고난 사주 기운을 '자연의 요소(따뜻한 햇살, 울창한 나무, 비옥한 땅, 반짝이는 보석, 시원한 바다 등)'에 비유해서 친근하게 설명하세요.
                5. 친절하고 다정한 말투(~해요, ~랍니다)를 사용하세요.
                6. 직관적이고 읽기 쉬운 표현을 사용하여 아래 8가지 항목으로 나누어 작성해 주세요.

                [출력 양식]
                1. 🌿 **나를 나타내는 자연의 기운**
                   - 내가 어떤 성향의 자연 이미지(나무, 불, 흙, 쇠, 물)를 닮았는지 쉽고 재미있게 비유해 주세요.

                2. 💡 **타고난 성격과 숨겨진 매력**
                   - 남들이 보는 나의 장점과 내 안에 숨겨진 매력, 그리고 주의하면 더 좋을 점을 알려주세요. 또 단점도 알려주세요

                3. 💰 **재물운과 나에게 딱 맞는 일**
                   - 돈을 어떻게 모으는 스타일인지, 어떤 환경이나 분야에서 내 능력이 가장 빛나는지 설명해 주세요, 또 재물운은 어떤지 알려주세요.

                4. 💌 **내 삶이 더 행복해지는 꿀팁**
                   - 일상생활에서 쉽게 실천할 수 있는 현실적이고 따뜻한 조언 2~3가지를 들려주세요.
                   
                5. 👍 **오늘의 운세!!**
                   - 오늘 날짜의 운세를 풀어서 알려주세요.
                   
                6. ⏩ **이달의 운세!!*
                   - 이달의 운세를 풀어서 전문적으로 알려주세요.

                7. 🌹 **일년 운세를!!*
                   - 이번년도 운세를 풀어서 전문적으로 알려주세요.
                   
                8. 👍 **총평과 운세**
                   - 운세의 총평과 또 피해야할것 좋은것 어느날이 좋은지 몇월이 좋은지 등을 전문적으로 풀어서 알려주세요.
                   
                """

                # 지정된 gemini-3.6-flash 모델 적용
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )

                st.success("분석이 완료되었습니다!")
                st.markdown("### 📜 사주풀이 결과")
                st.write(response.text)

            except Exception as e:
                st.error(f"죄송합니다. 현재 동시에 많은 사용자가 접속하여 응답이 지연되고 있습니다. 잠시후 다시 [사주보기] 버튼을 눌러주세요!. 감사합니다.!")
