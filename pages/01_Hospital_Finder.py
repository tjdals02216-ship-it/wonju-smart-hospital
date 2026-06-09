import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import json
import os
import sys
from google import genai

# 💡 상위 폴더에 있는 컴포넌트(CSS 및 카카오맵) 가져오기
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from map_components import get_hospital_finder_css, get_kakao_map_html

# ==========================================
# 🔒 보안 및 배포 설정 (API 키 숨기기)
# ==========================================
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ==========================================
# 0. 페이지 설정
# ==========================================
logo_path = "image/sajo_logo.png"
page_icon_data = logo_path if os.path.exists(logo_path) else "⚕️"

st.set_page_config(page_title="사조참치 | 원주 스마트 병원 찾기", page_icon=page_icon_data, layout="wide", initial_sidebar_state="expanded")

# CSS 씌우기
st.markdown(get_hospital_finder_css(), unsafe_allow_html=True)

# ==========================================
# 💾 1. 데이터 로드 
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv('hira_data_latlon.csv', encoding='utf-8-sig')

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 오류: {e}")
    st.stop()

if 'selected_hospital' not in st.session_state:
    st.session_state['selected_hospital'] = "🗺️ 전체 보기"

# ==========================================
# 🎨 2. 첫 번째 패널 (사이드바)
# ==========================================
with st.sidebar:
    st.subheader("🤖 AI 증상 분석기")
    user_symptom = st.text_area("증상을 자세히 적어주세요", placeholder="예: 배가 아프고 열이 나요", height=130)
    analyze_btn = st.button("분석 및 매칭 시작", use_container_width=True, type="primary")

    st.divider()
    
    st.subheader("📍 지역 선택")
    wonju_areas = ["전체", "단계동", "무실동", "반곡동", "단구동", "중앙동", "일산동", "학성동", "봉산동", "우산동", "태장동", "명륜동", "개운동", "관설동", "흥업면", "소초면", "호저면", "지정면", "문막읍", "부론면", "귀래면", "판부면", "신림면"]
    selected_area = st.selectbox("진료받을 지역을 골라주세요", wonju_areas)

    filtered_df = df.copy() 
    
    if analyze_btn or 'dept' in st.session_state:
        if analyze_btn:
            combined_symptom = user_symptom
            with st.sidebar.status("Gemini AI가 증상을 분석 중입니다...", expanded=True):
                try:
                    prompt = f"""
                    환자의 증상: "{combined_symptom}"
                    이 증상을 분석해서 1. 의심되는 질환 분류(예: 소화기 질환, 호흡기 질환, 근골격계 질환, 안구 질환, 피부 질환 등)와 2. 가장 적합한 진료과(예: 내과, 정형외과, 피부과, 안과, 이비인후과, 치과, 신경외과 중 택 1)를 도출해.
                    반드시 '질환, 진료과' 형식으로 쉼표로 구분해서 출력하고 다른 설명은 절대 쓰지마.
                    예시: 소화기 질환, 내과
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    
                    result_text = response.text.strip()
                    
                    if "," in result_text:
                        pred = result_text.split(",")[0].strip()
                        dept = result_text.split(",")[1].strip()
                    else:
                        pred, dept = "맞춤형 증상", result_text.replace("과", "") + "과"
                        
                    st.session_state['pred'], st.session_state['dept'] = pred, dept
                    st.session_state['selected_hospital'] = "🗺️ 전체 보기"
                    time.sleep(0.5) 
                    
                except Exception as e:
                    # 💡 비상 키워드 매칭 엔진 가동
                    symptom_txt = combined_symptom.lower()
                    
                    # 기본 디폴트값 세팅
                    pred = "일반/내과 질환"
                    dept = "내과"
                    
                    if any(w in symptom_txt for w in ["치아", "잇몸", "이빨", "치통", "스케일링", "사랑니", "충치", "치과"]):
                        pred, dept = "구강/치과 질환", "치과"
                    elif any(w in symptom_txt for w in ["눈", "시력", "충혈", "안구", "시야", "결막", "안과"]):
                        pred, dept = "안구 질환", "안과"
                    elif any(w in symptom_txt for w in ["피부", "가려움", "두드러기", "여드름", "발진", "아토피", "피부과"]):
                        pred, dept = "피부 질환", "피부과"
                    elif any(w in symptom_txt for w in ["목", "코", "귀", "기침", "가래", "인후염", "비염", "감기", "콧물", "이비인후과"]):
                        pred, dept = "이비인후 질환", "이비인후과"
                    elif any(w in symptom_txt for w in ["뼈", "허리", "어깨", "관절", "무릎", "다리", "발목", "손목", "근육", "인대", "정형외과"]):
                        pred, dept = "근골격계 질환", "정형외과"
                    elif any(w in symptom_txt for w in ["머리", "두통", "마비", "신경", "어지럼증", "신경외과"]):
                        pred, dept = "신경계 질환", "신경외과"
                    elif any(w in symptom_txt for w in ["배", "소화", "위", "토", "설사", "복통", "장염", "내과"]):
                        pred, dept = "소화기 질환", "내과"
                        
                    # 💡 [핵심] 팀장님 요청대로 "비상 백업 매칭"이라는 글자를 완벽히 제거했습니다.
                    # 이제 화면에는 "입력하신 증상은 근골격계 질환(으)로 의심되며..." 라고만 깔끔하게 나옵니다.
                    st.session_state['pred'] = pred
                    st.session_state['dept'] = dept
                    st.session_state['selected_hospital'] = "🗺️ 전체 보기"
        
        current_dept = st.session_state.get('dept', '전체')
        if current_dept != "전체":
            kw = "정형" if current_dept == "정형외과" else "이비인후" if current_dept == "이비인후과" else "치과" if current_dept == "치과" else current_dept.replace("과", "")
            filtered_df = filtered_df[filtered_df['병원명'].astype(str).str.contains(kw) | filtered_df['종별'].astype(str).str.contains(kw)]

    if selected_area != "전체":
        filtered_df = filtered_df[filtered_df['소재지'].astype(str).str.contains(selected_area)]


# ==========================================
# 🖥️ 3. 두 번째 패널 (리스트) & 세 번째 패널 (지도)
# ==========================================
list_col, map_col = st.columns([1, 2.5], gap="small")

with list_col:
    st.markdown("<div style='padding: 25px 15px 0px 30px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-bottom:0px; color:#333;'>검색결과 (<span style='color:#E53935;'>{len(filtered_df)}</span>건)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; color:#888; margin-bottom: 15px;'>※ 조건에 맞는 추천 병원 목록입니다.</p>", unsafe_allow_html=True)

    # AI 분석 결과 매칭 안내 박스
    if 'pred' in st.session_state and 'dept' in st.session_state and st.session_state['dept'] != "전체":
        st.markdown(f"""
        <div style="background-color: #e8f0fe; border-left: 4px solid #3162C7; padding: 12px 15px; border-radius: 6px; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 13px; color: #1a2a40; line-height: 1.5;">
                🤖 <b>AI 증상 분석 결과</b><br>
                입력하신 증상은 <b>{st.session_state['pred']}</b>(으)로 의심되며,<br>
                가장 적합한 진료과는 <span style="color: #3162C7; font-size: 16px; font-weight: 900;">'{st.session_state['dept']}'</span> 입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 기존 주의사항 UI
    st.markdown("""
    <div style="background-color: #FFFDF5; border: 1px solid #FFE082; padding: 10px 12px; border-radius: 6px; margin-bottom: 15px; text-align: left;">
        <p style="margin: 0; font-size: 12px; color: #555; line-height: 1.5; word-break: keep-all;">
            <b>🚨 [이용 안내 및 주의사항]</b> <br>본 시스템의 결과는 공공데이터 기반의 <b>참고용 정보</b>이며, 의학적 진단을 대체할 수 없습니다. <br>심각한 통증이나 응급 상황 시 즉시 <b>119</b> 또는 <br><b>응급 의료기관</b>을 이용하시기 바랍니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(height=650, border=False):
        if filtered_df.empty: st.info("조건에 맞는 병원이 없습니다.")
        else:
            for idx, row in filtered_df.iterrows():
                hosp_name, hosp_type, hosp_addr, hosp_grade = row['병원명'], row.get('종별', '정보없음'), row.get('소재지', '주소없음'), str(row.get('평가등급', ''))
                
                grade_html = '<div style="display: inline-block; background-color: #FFFDF5; border: 1px solid #FFB300; border-radius: 4px; padding: 4px 8px; font-size: 12px; font-weight: bold; margin-top: 5px; color: #FFB300;">🥇 1등급 우수병원</div>' if "1등급" in hosp_grade else '<div style="display: inline-block; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 4px; padding: 4px 8px; font-size: 12px; font-weight: bold; margin-top: 5px; color: #555;">🏅 일반병원</div>'
                
                with st.container(border=True):
                    if st.button(f"🏥 {hosp_name}", key=f"btn_{idx}", use_container_width=True):
                        st.session_state['selected_hospital'] = hosp_name
                    
                    st.markdown(f'<div style="padding: 5px 10px;"><p style="font-size: 13px; color: #555; margin: 6px 0;"><b>분류 |</b> {hosp_type}</p><p style="font-size: 13px; color: #555; margin: 6px 0;"><b>주소 |</b> {hosp_addr}</p>{grade_html}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) 

with map_col:
    hospitals_json = json.dumps(filtered_df[['병원명', '소재지', '종별', '평가등급', 'lat', 'lon']].to_dict(orient='records'), ensure_ascii=False)
    
    html_code = get_kakao_map_html(hospitals_json, st.session_state['selected_hospital'])
    components.html(html_code, height=850)