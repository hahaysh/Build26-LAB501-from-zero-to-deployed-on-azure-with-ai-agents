# 문제 해결 가이드

## 로컬에서 Cosmos DB 연결 실패

**증상:** `python app.py` 실행 시 인증 또는 연결 오류 발생
**원인:** 앱은 `DefaultAzureCredential`을 사용하며, Azure CLI 로그인 상태가 필요함
**해결:** `az login` 실행 후 올바른 구독인지 확인. `.env`의 `COSMOS_ENDPOINT`가 실제 Cosmos DB endpoint와 일치하는지 확인

## ACR 이름에 하이픈 포함 → 배포 실패

**증상:** `azd up`가 invalid ACR name 오류로 실패
**원인:** ACR 이름은 영숫자만 허용. AZD environment 이름의 하이픈이 ACR 이름에 전파됨
**해결:** 하이픈 없는 environment 이름 사용(예: `lab501app`) 후 `azd init` 재실행

## AZD가 잘못된 구독으로 배포

**증상:** 리소스가 다른 구독에 생성되거나 권한 오류 발생
**원인:** AZD는 `az account show`와 별도의 구독 설정을 유지함
**해결:** 아래 명령으로 정렬
`azd env set AZURE_SUBSCRIPTION_ID $(az account show --query id -o tsv)`

## 배포 후 Container App이 Cosmos DB에 연결 불가

**증상:** 배포는 성공했지만 앱 접속 시 데이터베이스 오류
**원인:** Container App의 권한 또는 환경변수가 잘못됨
**해결:** `COSMOS_ENDPOINT`, `COSMOS_DATABASE`, `COSMOS_CONTAINER` 환경변수 확인. managed identity 사용 시 system-assigned identity에 적절한 Cosmos DB RBAC role이 할당됐는지 확인

## `az containerapp ingress update`가 2분 이상 멈춘 것처럼 보임

**증상:** 명령 실행 후 진행이 멈춘 것처럼 보임
**원인:** 새 Container Apps revision 활성화를 기다리는 정상 동작
**해결:** 완료될 때까지 기다림. Ctrl+C로 중단하지 않기

## 배포 직후 첫 요청이 느리거나 timeout 발생

**증상:** `curl` 첫 요청이 10초 이상 소요되거나 timeout
**원인:** 새 revision 활성화(cold start)
**해결:** 배포 완료 후 약 15초 대기 후 재시도

## 시나리오 4에서 KQL 결과가 비어 있음

**증상:** 쿼리 결과가 빈 테이블
**원인:** Log Analytics 수집 지연(약 5분), 메트릭 지연(약 15분)
**해결:** 시나리오 3 완료 후 5분 대기 후 재실행

## `az monitor scheduled-query create`에서 command not found

**증상:** `scheduled-query` 명령을 인식하지 못함
**원인:** preview CLI extension 미설치
**해결:** `az extension add --name scheduled-query --yes`

## `azd up` 중 Docker build 실패

**증상:** Docker 관련 오류로 배포 실패
**원인:** Docker Desktop 미실행
**해결:** Docker Desktop 실행 후 `docker version` 확인, 이후 `azd up` 재실행

## Python dependency 설치 실패

**증상:** `pip install -r requirements.txt` 오류
**원인:** 시스템 의존성 누락 또는 Python 버전 불일치
**해결:** `python --version`으로 Python 3.13+ 확인. 필요 시 먼저 `pip install --upgrade pip` 실행

## PowerShell에서 KQL 따옴표 이스케이프 오류

**증상:** `where Reason_s == "ProbeFailed"` 구문이 PowerShell에서 실패
**원인:** PowerShell과 bash의 따옴표 처리 방식 차이
**해결:** `==` 대신 `has` 사용 권장
`where Reason_s has "ProbeFailed"`

## 배포 후 Gunicorn 포트 불일치

**증상:** 새로 배포했는데도 Container App이 503 반환
**원인:** ingress target port와 gunicorn bind port(8000) 불일치
**해결:** Container App ingress target port를 `8000`으로 설정(`Dockerfile`의 `gunicorn --bind 0.0.0.0:8000`과 일치)

---

**돌아가기:** [개요](00-overview.ko.md) | [다음 단계 →](09-whats-next.ko.md)
