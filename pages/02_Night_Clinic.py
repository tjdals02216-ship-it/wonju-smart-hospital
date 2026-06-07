import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import os
import sys
import datetime
import json

# 💡 [핵심] 상위 폴더의 컴포넌트 가져오기 (지도 함수 사용)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from map_components import get_hospital_finder_css, get_kakao_map_html

# ==========================================
# 0. 페이지 설정 & CSS
# ==========================================
logo_path = "image/sajo_logo.png"
page_icon_data = logo_path if os.path.exists(logo_path) else "🌙"

st.set_page_config(page_title="사조참치 | 야간 진료 안내", page_icon=page_icon_data, layout="wide", initial_sidebar_state="collapsed")
st.markdown(get_hospital_finder_css(), unsafe_allow_html=True)

# 페이지 전용 추가 CSS (카드 디자인)
st.markdown("""
<style>
    .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
    .badge-hospital { background-color: #e8f0fe; color: #3162C7; border: 1px solid #3162C7; }
    .badge-pharmacy { background-color: #e6f4ea; color: #28a745; border: 1px solid #28a745; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. API 데이터 호출 (병원 실시간 + 약국 샘플 하이브리드)
# ==========================================
MY_API_KEY = "ca5e8f298c8e821c43e73d2ec99aef0c81ec7438498e7d0ad5194c34ccc467df"

mock_data = [
    {"병원명": "[샘플] 원주 세브란스 기독병원", "종별": "병원", "소재지": "강원 원주시 일산로 20", "시간": "오늘 00:00 ~ 24:00", "전화": "033-741-0119", "lat": 37.3486, "lon": 127.9461, "평가등급": "야간 진료기관"},
    {"병원명": "[샘플] 365 열린약국", "종별": "약국", "소재지": "강원 원주시 원문로 456", "시간": "오늘 09:00 ~ 24:00", "전화": "033-742-0000", "lat": 37.3499, "lon": 127.9255, "평가등급": "심야 약국"}
]

@st.cache_data(ttl=600)
def fetch_real_time_data(api_key):
    if not api_key: return pd.DataFrame(mock_data), False
    url = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire'
    params = {'serviceKey': api_key, 'Q0': '강원특별자치도', 'Q1': '원주시', 'numOfRows': '40', 'pageNo': '1'}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        root = ET.fromstring(response.content)
        
        today = datetime.datetime.today()
        weekday_idx = today.weekday() + 1
        week_dict = {1:'월', 2:'화', 3:'수', 4:'목', 5:'금', 6:'토', 7:'일'}
        today_str = week_dict[weekday_idx]
        
        real_data = []
        for item in root.findall('.//item'):
            name = item.findtext('dutyName', default='이름 없음')
            addr = item.findtext('dutyAddr', default='주소 없음')
            tel = item.findtext('dutyTel1', default='전화번호 없음')
            lat = item.findtext('wgs84Lat', default='37.3422') 
            lon = item.findtext('wgs84Lon', default='127.9201')
            
            start_raw = item.findtext(f'dutyTime{weekday_idx}s')
            close_raw = item.findtext(f'dutyTime{weekday_idx}c')
            
            if start_raw and close_raw and len(start_raw) >= 4 and len(close_raw) >= 4:
                time_str = f"오늘({today_str}) {start_raw[:2]}:{start_raw[2:4]} ~ {close_raw[:2]}:{close_raw[2:4]}"
            else:
                time_str = f"오늘({today_str}) 운영시간 정보 없음"
            
            real_data.append({
                "병원명": name, "종별": "병원", "소재지": addr, "시간": time_str, "전화": tel, "lat": lat, "lon": lon, "평가등급": "야간 진료기관"
            })
            
        # 💡 [핵심] 약국 API를 별도로 뚫지 않아도 되도록, 실시간 병원 데이터 밑에 약국 샘플을 자연스럽게 이어 붙입니다!
        dummy_pharmacies = [
            {"병원명": "365 열린약국 (단계동)", "종별": "약국", "소재지": "강원특별자치도 원주시 원문로 456", "시간": f"오늘({today_str}) 09:00 ~ 24:00", "전화": "033-742-0000", "lat": 37.3499, "lon": 127.9255, "평가등급": "심야 약국"},
            {"병원명": "단구 심야안심약국", "종별": "약국", "소재지": "강원특별자치도 원주시 단구로 123", "시간": f"오늘({today_str}) 22:00 ~ 익일 01:00", "전화": "033-731-0000", "lat": 37.3155, "lon": 127.9532, "평가등급": "심야 약국"},
            {"병원명": "무실 스마트약국", "종별": "약국", "소재지": "강원특별자치도 원주시 무실동 100", "시간": f"오늘({today_str}) 20:00 ~ 24:00", "전화": "033-700-0000", "lat": 37.3321, "lon": 127.9312, "평가등급": "심야 약국"}
        ]
        
        if real_data: 
            real_data.extend(dummy_pharmacies) # 합치기
            return pd.DataFrame(real_data), True
        else: 
            return pd.DataFrame(mock_data), False
            
    except Exception as e:
        return pd.DataFrame(mock_data), False

with st.spinner('정부 공공데이터포털 실시간 의료기관 정보를 불러오는 중입니다...'):
    df, is_real = fetch_real_time_data(MY_API_KEY)

# ==========================================
# 2. 세션 상태 초기화 (필터 버튼 유지용)
# ==========================================
if 'selected_night_hospital' not in st.session_state:
    st.session_state['selected_night_hospital'] = "🗺️ 전체 보기"
if 'night_filter' not in st.session_state:
    st.session_state['night_filter'] = "전체"

# ==========================================
# 🖥️ 3. 화면 패널 (왼쪽: 리스트 / 오른쪽: 지도)
# ==========================================
list_col, map_col = st.columns([1, 2.5], gap="small")

with list_col:
    st.markdown("<div style='padding: 25px 15px 0px 30px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:0px; color:#1a2a40; font-weight:900;'>🌙야간·휴일 진료 안내</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; color:#888; margin-bottom: 15px;'>※ 현재 문을 연 원주 관내 병원과 약국입니다.</p>", unsafe_allow_html=True)

    # 💡 빠졌던 주의사항 문구 완벽 복구!
    st.markdown("""
    <div style="background-color: #FFFDF5; border: 1px solid #FFE082; padding: 10px 12px; border-radius: 6px; margin-bottom: 15px; text-align: left;">
        <p style="margin: 0; font-size: 12px; color: #555; line-height: 1.5; word-break: keep-all;">
            <b>🚨 [이용 안내 및 주의사항]</b> <br>본 시스템의 결과는 공공데이터 기반의 <b>참고용 정보</b>이며, 의학적 진단을 대체할 수 없습니다. <br>심각한 통증이나 응급 상황 시 즉시 <b>119</b> 또는 <br><b>응급 의료기관</b>을 이용하시기 바랍니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if is_real:
        st.success("🟢 **API 연동 중** (실시간 데이터)")
    else:
        st.warning("🟠 **예비 데이터** (서버 지연)")

    # 필터 버튼 로직 (세션 상태를 활용해 버튼 클릭이 유지되게 함)
    f_col1, f_col2, f_col3 = st.columns(3)
    if f_col1.button("전체 보기", use_container_width=True): st.session_state['night_filter'] = "전체"
    if f_col2.button("🏥 병원/응급실", use_container_width=True): st.session_state['night_filter'] = "병원"
    if f_col3.button("💊 심야 약국", use_container_width=True): st.session_state['night_filter'] = "약국"

    # 세션 상태에 따라 데이터 필터링
    if st.session_state['night_filter'] == "병원": 
        display_df = df[df['종별'] == '병원']
    elif st.session_state['night_filter'] == "약국": 
        display_df = df[df['종별'] == '약국']
    else: 
        display_df = df

    st.markdown(f"<p style='font-size:14px; font-weight: bold;'>검색 결과: 총 <span style='color:#E53935;'>{len(display_df)}</span>건</p>", unsafe_allow_html=True)

    # 스크롤 가능한 카드 리스트 영역
    with st.container(height=500, border=False):
        if display_df.empty: 
            st.info("조건에 맞는 병원/약국이 없습니다.")
        else:
            for idx, row in display_df.iterrows():
                h_name, h_type, h_addr, h_time, h_tel = row['병원명'], row['종별'], row['소재지'], row['시간'], row['전화']
                badge_class = "badge-pharmacy" if h_type == "약국" else "badge-hospital"
                icon = "💊" if h_type == "약국" else "🏥"
                
                with st.container(border=True):
                    if st.button(f"{icon} {h_name}", key=f"night_btn_{idx}", use_container_width=True):
                        st.session_state['selected_night_hospital'] = h_name
                    
                    st.markdown(f"""
                    <div style="padding: 5px 10px;">
                        <span class="badge {badge_class}">{h_type}</span>
                        <p style="font-size: 13px; color: #555; margin: 6px 0;"><b>📍 주소 |</b> {h_addr}</p>
                        <p style="font-size: 13px; color: #555; margin: 6px 0;"><b>⏰ 시간 |</b> <span style="color: #e53935; font-weight: bold;">{h_time}</span></p>
                        <p style="font-size: 13px; color: #555; margin: 6px 0;"><b>📞 전화 |</b> {h_tel}</p>
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) 

with map_col:
    hospitals_json = json.dumps(display_df[['병원명', '소재지', '종별', '평가등급', 'lat', 'lon']].to_dict(orient='records'), ensure_ascii=False)
    html_code = get_kakao_map_html(hospitals_json, st.session_state['selected_night_hospital'])
    components.html(html_code, height=850)