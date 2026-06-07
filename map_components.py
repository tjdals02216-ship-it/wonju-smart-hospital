def get_hospital_finder_css():
    """스마트 병원 찾기 페이지 전용 CSS 디자인"""
    return """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;} 
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