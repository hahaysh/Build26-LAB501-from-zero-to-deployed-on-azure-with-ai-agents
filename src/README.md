# LEGO Set Browser — Sample App

A Flask web application that browses a LEGO set catalog stored in Azure Cosmos DB. This is the starter app for **Build 2026 — LAB501**.

## 한국어 빠른 안내

이 앱은 LAB501 실습용 스타터 애플리케이션입니다. 기능은 다음과 같습니다.

- Azure Cosmos DB의 LEGO 세트 데이터를 조회/검색/상세 보기
- `DefaultAzureCredential` 기반 인증 사용
- 로컬 실행(`python app.py`)과 컨테이너 실행(`docker run`) 모두 지원

실습 문서는 아래 한국어 가이드를 먼저 참고하세요.

- [한국어 실습 인덱스](../docs/lab-instructions/ko/README.md)
- [시작하기 - 스타터 앱 준비](../docs/lab-instructions/ko/03-getting-started.ko.md)

기본 UI를 한국어로 표시하려면 `.env` 또는 환경변수에 아래 값을 설정하세요.

```bash
UI_LANG=ko
```

이 값을 설정하면 앱은 기본적으로 한국어 UI로 열리고, 필요하면 화면 상단의 EN/KR 토글이나 `?lang=en` 쿼리로 전환할 수 있습니다.

## Prerequisites

- Python 3.13+
- An Azure Cosmos DB account with the LEGO dataset loaded
- Azure CLI logged in (for `DefaultAzureCredential`)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the environment sample and fill in your values
cp .env.sample .env

# 3. Run locally
python app.py
```

The app will be available at `http://localhost:5000`.

## Running with Docker

```bash
docker build -t lego-set-browser .
docker run -p 8000:8000 lego-set-browser
```

## Project Structure

```text
src/
├── app.py                 # Flask application (routes + Cosmos DB queries)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── .dockerignore          # Docker build exclusions
├── .env.sample            # Environment variable template
├── static/css/style.css   # Custom CSS (Star Wars theme)
└── templates/
    ├── base.html          # Layout template
    ├── home.html          # Landing page with featured sets
    ├── browse.html        # Paginated browse/search/filter page
    ├── detail.html        # Individual set detail page
    └── 404.html           # Custom 404 page
```

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `COSMOS_ENDPOINT` | Cosmos DB account endpoint | *(see .env.sample)* |
| `COSMOS_DATABASE` | Database name | `LegoDatabase` |
| `COSMOS_CONTAINER` | Container name | `legoSets` |
| `UI_LANG` | Default UI language (`en` or `ko`) | `ko` |
| `AZURE_CLIENT_ID` | Managed Identity client ID (optional) | — |
