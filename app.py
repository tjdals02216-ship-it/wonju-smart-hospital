import streamlit as st
import streamlit.components.v1 as components
import os

from ui_components import get_custom_css, get_navbar_html, get_slider_html

logo_path = "sajo_logo.png"
page_icon_data = logo_path if os.path.exists(logo_path) else "⚕️"

st.set_page_config(
    page_title="사조참치 | 원주 스마트 의료 통합 서비스", 
    page_icon=page_icon_data,              
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
st.markdown(get_navbar_html(), unsafe_allow_html=True)

st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

# 🎬 꽉 차는 웅장한 오토 슬라이더
components.html(get_slider_html(), height=700)

# ==========================================
# 3. 하단 꽉 찬 메뉴 영역 (핵심 기능 2개 배치)
# ==========================================
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 60px; font-weight: 900; color:#1a1a1a; letter-spacing:-1px;'> 원주 의료 서비스 바로가기</h1>", unsafe_allow_html=True)

row1_col1, gap1, row1_col2 = st.columns([1, 0.02, 1])

with row1_col1:
    st.markdown("""
    <div class="main-card-full-screen">
        <div class="card-icon">🔍</div>
        <h2 class="card-title">AI 스마트 병원 찾기</h2>
        <p class="card-text">어디가 아프신가요? 내 증상을 AI가 분석하여 가장 적합한 진료과와 원주 관내 1등급 병원을 지도로 한눈에 찾아줍니다.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("병원 찾기 시작하기", use_container_width=True):
        st.switch_page("pages/01_Hospital_Finder.py")

with row1_col2:
    st.markdown("""
    <div class="main-card-full-screen">
        <div class="card-icon">🌙</div>
        <h2 class="card-title">야간·휴일 진료 안내</h2>
        <p class="card-text">늦은 밤이나 주말, 갑자기 아플 때 당황하지 마세요. 현재 문을 연 원주 관내 야간 진료 병원과 심야 약국을 안내합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    # 💡 야간 진료 안내 페이지로 바로 넘어가도록 연결 완료!
    if st.button("진료 안내 보기", use_container_width=True):
        st.switch_page("pages/02_Night_Clinic.py")

# ==========================================
# 4. 하단 Footer (면책 조항 및 카피라이트)
# ==========================================
st.divider()

# 세련된 면책 조항 및 카피라이트 영역
st.markdown("""
<div style='text-align: center; color: #888; font-size: 13px; line-height: 1.6; margin-bottom: 20px;'>
    <b>⚠️ [이용 안내 및 주의사항]</b><br>
    본 시스템이 제공하는 병원 추천 및 AI 증상 분석 결과는 공공데이터 기반의 <b>참고용 정보</b>이며, 전문의의 의학적 진단을 대체할 수 없습니다.<br>
    심각한 통증이나 응급 상황 시 즉시 <b>119</b> 또는 <b>가까운 응급 의료기관</b>을 이용하시기 바랍니다.
</div>
<p style='text-align: center; color: #bbb; font-size: 12px; padding-bottom: 40px;'>
    © 2026 SAJO TUNA Team. Capstone Design Project | 지도교수: 권기태
</p>
""", unsafe_allow_html=True)