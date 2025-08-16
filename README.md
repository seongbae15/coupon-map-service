# 민생 회복 쿠폰 사용처 데이터 수집 도구
 
이 프로젝트는 **Playwright 웹 스크래핑**을 통해 **민생 회복 쿠폰 사용처** 정보를 수집하고, **Django**를 이용해 백엔드 서버를 구축하는 코드입니다.

- **데이터베이스(DB)는 제공하지 않습니다.**  
- 실제 데이터는 각 사용자가 직접 크롤링해야 합니다.
    - 크롤링 과정은 네트워크 속도와 API 호출 제한에 따라 상당한 시간이 소요될 수 있습니다.
- 웹사이트마다 구조가 다르므로, 코드 수정이 필요할 수 있습니다.

## 기능
- **Playwright 기반 크롤링**
  - 업종, 가맹점명, 주소를 추출합니다. (개인정보 보호를 위해, 전화번호는 수집하지 않음)
  - 사이트 구조에 따라 크롤링 로직을 수정해야 합니다.
- **Django**를 이용한 Backend 구축
    - SQLite 또는 설정된 DB에 저장
    - 모델 정의와 마이그레이션 파일 포함
    - **네이버 지도 Geocoding API 연동**
    - 추출된 주소 → 위도/경도 변환
    - 변환된 좌표를 기반으로 지도 시각화 가능
 
## 사용 방법
1. 환경 설정
    - 가상환경 생성 및 활성화
        ```bash
        python -m venv venv
        source venv/bin/activate   # Linux / Mac
        ```
    - 필요 라이브러리를 설치
        ```bash
        pip install -r requirements.txt
        ```
    - 네이버 Geocoding API 키**를 발급받아 환경 변수 추가.
        - `.env` 파일에 환경 변수 추가.

2. 사용 방법
    - Crawling: 동 별로 .json파일로 저장됨.
        - `market-crawling/main.py`의 URL 수정 및 크롤링하려는 웹사이트에 맞게 수정.
        - 코드 실행
            ```bash
            cd market-crawling
            python main.py
            # 작업 완료 후.
            cd ..
    - DB 저장: 추출한 .json파일을 DB(SQLite)에 저장
        - 데이터 변환 과정은 네트워크 속도와 API 호출 제한에 따라 상당한 시간이 소요될 수 있습니다.(Geocoding API에서 위도, 경도를 추출할 수 없는 가맹점은 제외됨.)
        ```bash
        python backend/scripts/geocode_json.py
        ```
