# Translation Handoff Guide

이 문서는 LAB501 한국어 번역 작업을 다른 PC/환경/작업자에게 이어서 전달하기 위한 가이드입니다.

## 1) 권장 방식: 브랜치로 이어서 작업

현재 로컬에서:

```bash
git checkout -b chore/ko-translation-handoff
git add .
git commit -m "Korean translation handoff checkpoint"
git push -u origin chore/ko-translation-handoff
```

다른 환경에서:

```bash
git clone https://github.com/microsoft/Build26-LAB501.git
cd Build26-LAB501
git fetch origin
git checkout chore/ko-translation-handoff
```

장점:
- 변경 이력, diff, 리뷰, PR 연계가 가장 쉬움
- 팀 협업/코드리뷰에 적합

## 2) 원격 push가 어려울 때: patch 파일 전달

현재 로컬에서:

```bash
git diff > ko-translation.patch
```

다른 환경에서:

```bash
git apply ko-translation.patch
```

장점:
- 저장소 권한이 없어도 전달 가능
- 이메일/메신저로 파일 공유 가능

주의:
- 파일 충돌이 있으면 수동 병합이 필요할 수 있음

## 3) 오프라인 전달: git bundle

현재 로컬에서:

```bash
git bundle create ko-translation.bundle --all
```

다른 환경에서:

```bash
git clone ko-translation.bundle Build26-LAB501
cd Build26-LAB501
git checkout main
```

장점:
- 네트워크 없이도 전체 이력 전달 가능

## 현재 번역 핵심 산출물 위치

- 루트 안내 및 진입 동선: README.md
- 한국어 운영 가이드: GUIDANCE.ko.md
- 한국어 실습 인덱스: docs/lab-instructions/ko/README.md
- 한국어 실습 본문: docs/lab-instructions/ko/00-overview.ko.md ~ 10-glossary.ko.md
- 앱 한국어 UI/i18n: src/app.py, src/templates/*.html

## 재개 시 빠른 점검 체크리스트

1. 한국어 문서 링크 일관성 확인
- ko 문서 내부 링크가 ko 파일을 가리키는지 확인

2. 앱 UI 언어 동작 확인
- 기본값: UI_LANG=ko
- 라우트 확인: /, /browse, /set/<id>, /missing

3. 문서 품질 점검
- markdownlint 경고 중 템플릿 관성(배너/HTML table)과 실제 오류를 구분

4. 최종 전달 준비
- PR 본문에 번역 원칙(명령어/코드/제품명 영문 유지)을 명시
- 필요 시 리뷰어에게 용어집(10-glossary.ko.md) 우선 검토 요청

## 권장 커밋 단위

- docs 번역(ko 폴더)
- 루트/문서 README 한국어 동선
- src UI i18n
- GUIDANCE 한국어 병행본

커밋을 나누면 리뷰와 롤백이 쉬워집니다.
