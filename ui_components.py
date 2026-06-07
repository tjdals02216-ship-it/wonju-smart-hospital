import base64

def get_custom_css():
    return """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    .block-container { padding: 0rem !important; max-width: 100% !important; }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }

    .top-navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background-color: #ffffff; 
        border-bottom: 1px solid #f0f0f0;
        z-index: 9999;
        display: flex; justify-content: space-between; align-items: center; 
        padding: 0 1.5%; 
    }
    
    .top-navbar .logo { display: flex; align-items: center; }
    
    .top-navbar .logo img { 
        height: 65px;  
        cursor: pointer; 
        transition: opacity 0.2s; 
        mix-blend-mode: multiply;
    }
    .top-navbar .logo img:hover { opacity: 0.8; }
    
    .top-navbar .menu-items { display: flex; gap: 30px; font-weight: 600; color: #333; font-size: 16px; }
    
    .top-navbar .menu-items a { text-decoration: none; color: inherit; cursor: pointer; transition: color 0.2s; }
    .top-navbar .menu-items a:hover { color: #3162C7; }

    .stHorizontalBlock { padding: 0 1.5% !important; }
    
    .main-card-full-screen {
        padding: 40px; background: white; border-bottom: 2px solid #3162C7; 
        height: 100%; margin-bottom: 15px; transition: transform 0.2s, background-color 0.2s;
    }
    .main-card-full-screen:hover { transform: translateY(-5px); background-color: #f8fbff; }
    .card-icon { font-size: 50px; margin-bottom: 20px; }
    .card-title { font-size: 24px !important; font-weight: 800 !important; color: #1a1a1a; margin-bottom: 10px !important; }
    .card-text { font-size: 16px !important; color: #555; line-height: 1.7; }
    
    .stButton>button {
        border-radius: 8px !important; font-weight: bold !important; border: 1px solid #3162C7 !important;
        color: #3162C7 !important; background-color: white !important; transition: all 0.3s;
        padding: 15px 0 !important; font-size: 16px !important; margin-bottom: 40px !important; 
    }
    .stButton>button:hover { background-color: #3162C7 !important; color: white !important; }
    </style>
    """

def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}" 
    except FileNotFoundError:
        return ""

def get_navbar_html():
    logo_img_url = get_image_base64("image/sajo_logo.png")
    
    return f"""
    <div class="top-navbar">
        <div class="logo">
            <a href="/" target="_self" title="메인으로 가기">
                <img src="{logo_img_url}" alt="사조참치 로고">
            </a>
        </div>
        <div class="menu-items">
            <a href="/Hospital_Finder" target="_self">스마트 병원찾기</a>
            <a href="/Night_Clinic" target="_self">야간 진료 안내</a>
        </div>
    </div>
    """

def get_slider_html():
    img1_base64 = get_image_base64("image/img1.png")
    img2_base64 = get_image_base64("image/img2.png")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; overflow: hidden; }}
            .slider-wrapper {{ position: relative; width: 100vw; height: 700px; overflow: hidden; }}
            .slide {{ 
                position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                opacity: 0; transition: opacity 1.5s ease-in-out; 
                background-size: cover; background-position: center; 
                display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; 
            }}
            .slide.active {{ opacity: 1; }}
            .overlay {{ position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0, 10, 30, 0.6); z-index: 1; }}
            .content {{ position: relative; z-index: 2; color: white; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); padding: 20px; }}
            h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 20px; letter-spacing: -1.5px; }}
            p {{ font-size: 24px; font-weight: 300; color: #e0e5f0; }}
            .progress-area {{ position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%); width: 80%; max-width: 900px; display: flex; flex-direction: column; align-items: center; gap: 15px; z-index: 3; }}
            .progress-track {{ width: 100%; height: 3px; background: rgba(255,255,255,0.3); overflow: hidden; }}
            .progress-fill {{ height: 100%; background: #ffffff; width: 0%; transition: width 0.05s linear; }}
            .slide-indicator {{ color: white; font-size: 15px; font-weight: 600; letter-spacing: 4px; }}
        </style>
    </head>
    <body>
        <div class="slider-wrapper">
            <div class="slide active" style="background-image: url('{img1_base64}');">
                <div class="overlay"></div>
                <div class="content">
                    <h1> 원주 의료, 이제 스마트하게.</h1>
                    <p>AI 기반 맞춤 병원 추천부터 시민 소통까지, 원스톱 헬스케어 플랫폼</p>
                </div>
            </div>
            
            <div class="slide" style="background-image: url('{img2_base64}');">
                <div class="overlay"></div>
                <div class="content">
                    <h1>🌙 언제, 어디서 아플지 모르니까.</h1>
                    <p>24시간 내 손안의 주치의, 원주 관내 야간·휴일 진료 병원 실시간 안내</p>
                </div>
            </div>
            
            
            
            <div class="progress-area">
                <div class="progress-track"><div class="progress-fill" id="fill"></div></div>
                <div class="slide-indicator" id="indicator">01 ━ 03</div>
            </div>
        </div>
        
        <script>
            const slides = document.querySelectorAll('.slide');
            const fill = document.getElementById('fill');
            const indicator = document.getElementById('indicator');
            let currentIdx = 0; let progress = 0;
            const duration = 6000; 
            const interval = 20; const step = (interval / duration) * 100;
            
            setInterval(() => {{
                progress += step; fill.style.width = progress + '%';
                if (progress >= 100) {{
                    progress = 0; slides[currentIdx].classList.remove('active');
                    currentIdx = (currentIdx + 1) % slides.length; slides[currentIdx].classList.add('active');
                    indicator.innerText = `0${{currentIdx + 1}} ━ 0${{slides.length}}`;
                }}
            }}, interval);
        </script>
    </body>
    </html>
    """

def get_hospital_finder_css():
    """스마트 병원 찾기 페이지 전용 CSS 디자인"""
    return """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #3162C7 !important;
        width: 300px !important; 
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] input, div[data-baseweb="select"] * {
        color: #000000 !important;
        font-weight: bold;
    }
    
    .stButton>button { border-radius: 8px; font-weight: bold; }
    [data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }
    </style>
    """

def get_kakao_map_html(hospitals_json, selected_hospital):
    """카카오맵을 렌더링하는 HTML/JS 코드를 생성합니다."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            .info-window {{ padding: 12px; background: white; border: 1px solid #ccc; border-radius: 8px; width: 220px; font-family: sans-serif; box-shadow: 0 2px 6px rgba(0,0,0,0.3); }}
            .info-window h4 {{ margin: 0 0 5px 0; font-size: 15px; color: #333; }}
            .info-window p {{ margin: 2px 0; font-size: 12px; color: #666; }}
            .btn-kakao {{ display: block; margin-top: 10px; padding: 8px; background-color: #FFEB00; color: #3C1E1E; text-align: center; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 13px; }}
        </style>
    </head>
    <body style="margin: 0; padding: 0;">
    <div id="map" style="width:100%; height:850px;"></div>

    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=1b4fdb69fa82e1614b3c8bdea143de2f"></script>
    <script>
        var mapContainer = document.getElementById('map');
        var mapOption = {{ center: new kakao.maps.LatLng(37.3422, 127.9201), level: 5 }};
        var map = new kakao.maps.Map(mapContainer, mapOption);
        
        var starSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png';
        var starSize = new kakao.maps.Size(24, 35);
        var starMarker = new kakao.maps.MarkerImage(starSrc, starSize);
        
        var hospitals = {hospitals_json};
        var selectedHospName = "{selected_hospital}";
        var activeWindow = null;

        hospitals.forEach(function(h) {{
            var isFirstGrade = (h.평가등급 && h.평가등급.indexOf('1등급') !== -1);
            var marker = new kakao.maps.Marker({{
                map: map,
                position: new kakao.maps.LatLng(h.lat, h.lon),
                image: isFirstGrade ? starMarker : null
            }});

            var gradeText = isFirstGrade ? "<span style='color:red; font-weight:bold;'>" + h.평가등급 + "</span>" : h.평가등급;
            var linkUrl = "https://map.kakao.com/link/to/" + h.병원명 + "," + h.lat + "," + h.lon;

            var content = '<div class="info-window"><h4>' + h.병원명 + '</h4><p>' + h.소재지 + '</p><p>분류: ' + h.종별 + '</p><p>' + gradeText + '</p><a href="' + linkUrl + '" target="_blank" class="btn-kakao">🧭 카카오맵 길찾기</a></div>';

            var infowindow = new kakao.maps.InfoWindow({{ content: content, removable: true }});

            if (h.병원명 === selectedHospName) {{
                infowindow.open(map, marker);
                activeWindow = infowindow;
                map.setCenter(new kakao.maps.LatLng(h.lat, h.lon));
                map.setLevel(3);
            }}

            kakao.maps.event.addListener(marker, 'click', function() {{
                if (activeWindow) {{ activeWindow.close(); }}
                infowindow.open(map, marker);
                activeWindow = infowindow;
            }});
        }});
    </script>
    </body>
    </html>
    """