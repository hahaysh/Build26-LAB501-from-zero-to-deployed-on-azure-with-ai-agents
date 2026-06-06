# 시작하기 — 스타터 앱 준비

아래 순서로 스타터 앱을 준비합니다.

## 1. Lab 리포지토리 클론

새 PowerShell 세션에서 리포를 클론하고 이동합니다.

```powershell
git clone https://github.com/microsoft/Build26-LAB501.git
```

```powershell
cd Build26-LAB501
```

## 2. 스타터 앱 복사

`src/`에는 Azure Cosmos DB 기반 LEGO 세트 브라우저(Flask)가 포함되어 있습니다. 이를 `lego-set-browser` 작업 디렉터리로 복사하고 별도 Git 리포로 초기화합니다.

```powershell
Copy-Item -Recurse src lego-set-browser
```

```powershell
cd lego-set-browser
```

```powershell
git config --global user.name "Your Name"
```

```powershell
git config --global user.email "you@example.com"
```

```powershell
git init
```

```powershell
git add -A
```

```powershell
git commit -m "init"
```

명령 실행 중 문제가 발생하면 명령을 직접 타이핑하고 한 번에 한 줄씩 실행해 보세요.

이후의 모든 명령은 `lego-set-browser` 디렉터리에서 실행합니다.

> 💡 **스타터 앱 구성:** `app.py`는 LEGO 세트 검색/조회 라우트를 가진 Flask 앱입니다. `requirements.txt`에는 Flask, azure-cosmos, azure-identity, gunicorn 의존성이 포함되어 있고, `Dockerfile`은 컨테이너 배포용입니다. Cosmos DB 인증은 `DefaultAzureCredential`을 사용합니다.
> 💡 **한국어 UI 기본값:** `.env.sample`을 복사해 사용할 때 `UI_LANG=ko`를 유지하면 앱이 기본적으로 한국어 UI로 열립니다. 필요하면 URL에 `?lang=en` 또는 `?lang=ko`를 붙여 즉시 전환할 수 있습니다.

## 3. 로컬 테스트

현장 실습에서는 전체 랩 완주 시간을 확보하기 위해 로컬 테스트는 의도적으로 생략합니다.

---

**다음:** [시나리오 1 - 배포하고 강화하기 →](04-scenario-1-ship-and-harden.ko.md)
