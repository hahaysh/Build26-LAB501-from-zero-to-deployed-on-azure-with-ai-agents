# 시나리오 1 — 배포하고 강화하기 (~35분)

AI는 몇 분 안에 Azure 배포 골격을 만들 수 있습니다. 하지만 AI가 생성한 Bicep을 검토 없이 프로덕션에 바로 반영해도 될까요?

## 1부 — 배포하기 (~25분)

> 💡 **앱이 실행 중이 아니어야 합니다.** 체크포인트에서 `python app.py`를 실행했다면 진행 전에 **Ctrl+C**로 중지하세요.

현재 위치가 **lego-set-browser** 디렉터리가 아니라면 먼저 이동한 뒤, 아래 명령으로 **yolo mode** Copilot 세션을 시작하세요.

```bash
copilot --yolo
```

`--yolo` 플래그는 명령 자동 승인(확인 프롬프트 생략) 모드입니다. 이 랩은 샌드박스 환경이므로 사용해도 안전하며 진행 시간을 절약할 수 있습니다. 이후 Copilot에 아래 프롬프트를 입력하세요.

```text
  Create and deploy 2 Azure services 

   **Environment:**
   - Subscription: Current subscription
   - Create a new resource group: rg-lego-set-browser-dev
   - Region: West US 3
   
   **Existing Cosmos DB (do NOT create a new one):**
   - Look for the existing cosmos DB in the current subscription
   - Database: LegoDatabase / Container: legoSets
   
   **1. Python Azure Function App** — HTTP POST trigger on Flex Consumption (FC1):
   - Accepts JSON array of LEGO sets; batch-upserts to Cosmos DB above
   - Fields: set_number (→ id), name, theme_name, year_released, number_of_parts, type, image_url
   - User-assigned managed identity for Cosmos DB (Built-in Data Contributor)
   
   **2. Flask app in this folder → Azure Container Apps:**
   - Name: ca-web-lego-<XXXX>
   - Already uses DefaultAzureCredential + env vars COSMOS_ENDPOINT, COSMOS_DATABASE, COSMOS_CONTAINER
   - System-assigned managed identity for Cosmos DB (Built-in Data Reader)
```

이 한 번의 프롬프트로 **three-skill chain**이 실행됩니다. Copilot이 아래 순서로 스킬을 호출하는지 확인하세요.

### 1️⃣ `azure-prepare`가 먼저 실행

핵심 포인트는 서로 다른 출발점을 한 번에 처리하는 방식입니다.

- **Flask app → Container Apps (출발점: 워크스페이스의 기존 소스 코드):**
  - 워크스페이스를 스캔해 `requirements.txt`, `app.py`를 확인하고 Python Flask 웹앱으로 분류
  - 호스팅 대상으로 Container Apps를 선택
  - 기존 `Dockerfile`을 재사용/갱신 판단
  - 기존 코드 위에 인프라를 생성
- **Python Function App → Azure Functions (출발점: 프롬프트만 있고 소스 코드 없음):**
  - 워크스페이스에 함수 코드가 없으므로 프롬프트를 읽고 적절한 Python Functions 템플릿을 가져옴
  - LEGO JSON 스키마에 맞게 핸들러 수정(`set_number → id` 매핑, Cosmos 연결, UAMI 바인딩)
  - **Flex Consumption (FC1)** 계획 선택, 배포 패키지용 Storage account 포함
  - 템플릿 기반으로 인프라와 소스 코드 동시 생성
- **공통 처리:**
  - 두 서비스 선언이 포함된 `azure.yaml`과 `infra/` Bicep 템플릿 생성
  - AZD 환경 생성 및 구독/리전 설정

> 💡 **스킬 포인트:** `azure-prepare`는 파일만 생성하는 도구가 아닙니다. 런타임/Bicep/AZD/Functions 템플릿 참조를 조합해 결과를 만듭니다. 생성된 `infra/` Bicep과 `function_app.py`를 열어 확인해 보세요.

### 2️⃣ `azure-validate`가 다음 실행

두 서비스 대상으로 사전 검증(pre-flight)을 수행합니다.

- Bicep 컴파일(`az bicep build`)로 구문 오류 사전 검출
- Docker 실행 상태 확인(미실행 시 Container App 이미지 빌드 실패)
- Python 런타임 및 선택 리전의 FC1 가용성 확인
- 구독 접근 권한, 리소스 그룹 이름 충돌 확인

### 3️⃣ `azure-deploy`가 마지막 실행

`azd up --no-prompt`로 프로비저닝+배포를 한 번에 수행합니다.

- **Container App 측면:** ACR, Container Apps Environment, Log Analytics, Container App 생성 + Docker 이미지 빌드/푸시
- **Function App 측면:** Storage account, FC1, UAMI, Application Insights, Function App 생성 + 함수 코드 패키징/배포
- 두 서비스 모두에 Cosmos 환경변수를 연결하고 HTTPS 엔드포인트를 반환

### 동작 확인

```bash
curl <your-endpoint-url>
```

> 💡 **엔드포인트 URL 찾기:** 화면에서 URL을 놓쳤다면 `azd env get-values`를 실행하거나 Copilot에 "What's the URL for my Container App?"라고 물어보세요. URL 형태는 `https://<app-name>.<region>.azurecontainerapps.io`입니다.
> 💡 **첫 요청 지연:** 배포 직후 첫 요청은 새 revision 활성화로 10-15초 정도 걸릴 수 있습니다. 정상 동작입니다.
> ⚠️ **Container App의 Cosmos DB 접근:** 배포 후 Container App이 Cosmos DB에 접근할 권한이 아직 없을 수 있습니다. 이 경우 아래 강화 단계에서 managed identity + Cosmos DB RBAC 구성을 점검하고 보완합니다.

**완료 상태:** LEGO set browser를 제공하는 HTTPS 엔드포인트가 살아있는 상태입니다. 스킬 3개, 프롬프트 1개로 여기까지 도달합니다.

![브라우저에서 실행 중인 LEGO Vault](../images/workingApp.png)

> 📁 **어떤 파일이 생성되나요?** 배포 단계 이후 `lego-app` 디렉터리에 `azure.yaml`, `infra/`(예: `main.bicep`, `main.parameters.json`, 모듈 파일) 등이 생성됩니다. 기존 `Dockerfile`은 그대로 유지되거나 일부 업데이트될 수 있습니다.

---

## 2부 — 강화하기 (~10분)

> ⚠️ **권한 참고:** managed identity role assignment 같은 작업은 구독에 대해 **Owner** 또는 **User Access Administrator** 권한이 필요할 수 있습니다. 랩 환경에서 권한 오류가 나면, 모든 명령 실행보다 패턴 이해와 AI 제안 검토에 집중하세요.

`infra/` 디렉터리의 Bicep 파일을 검토하세요. `azure-prepare` 실행 과정에서 일부 보안 강화가 이미 적용됐을 수 있습니다. 이 단계의 목적은 **AI가 무엇을 했고 무엇을 놓쳤는지 감사(audit)** 하는 것입니다.

**Copilot에 입력하세요:**

```text
Review my deployed Container App infrastructure for production readiness gaps. Check for managed identity, Cosmos DB RBAC access (instead of keys), VNet integration, diagnostic settings, and health probes.
```

### 무엇을 봐야 하나요

| Gap | Why It Matters | Severity |
| --- | --- | --- |
| **No managed identity for ACR pull** | Container App이 관리자 자격증명으로 이미지 pull 수행 | High |
| **No managed identity for Cosmos DB** | 키 기반 접근으로 전환되어 키 유출 리스크 | High |
| **No VNet integration** | Container Apps Environment가 공용 네트워크에 노출 | Medium |
| **No diagnostic settings** | 플랫폼 메트릭 미전송으로 알림 누락 가능 | Medium |
| **No health probe configured** | 기본 TCP probe 사용, 앱 경로 기반 probe 부재 | Low |

> 💡 **일부 항목은 이미 강화됐을 수 있습니다.** `azure-prepare`에는 보안 강화 단계가 있어 managed identity/RBAC를 초기 생성 시 설정할 수 있습니다. 이미 적용되어 있다면 정상이며, 미적용 항목을 중심으로 보완하세요.

✅ **확인 지점:** 생성 인프라를 검토했고, AI가 이미 강화한 부분과 추가 보완이 필요한 부분을 식별했습니다. 최종적으로 Container App은 ACR pull과 Cosmos DB 접근 모두 managed identity 기반이어야 합니다.

**핵심 정리:** AI가 처음부터 꽤 안전한 배포를 만들 수도, 아닐 수도 있습니다. 보안 강화는 비결정적이므로 사람이 프로덕션 기준으로 확인하는 역량이 핵심입니다.

---

**다음:** [시나리오 2 — 보고 평가하기 →](05-scenario-2-see-and-evaluate.ko.md)
