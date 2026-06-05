# 시나리오 3 — 장애를 내고 진단하기 (~10분)

새벽 2시, 앱이 503을 반환합니다. 정답만 보지 말고 AI의 진단 추론 체인을 관찰하세요.

## 장애 유도하기

Scenario 1A에서 생성된 실제 Container App 이름(`<app>`)과 리소스 그룹(`<rg>`)으로 바꿔 아래 명령을 실행하세요. 값이 기억나지 않으면 `azd env get-values`로 확인할 수 있습니다.

```powershell
az containerapp ingress update --name <app> -g <rg> --target-port 9999
```

> ⏱️ 새 revision 활성화로 30초~2분 정도 걸릴 수 있습니다. 정상 동작이며 Ctrl+C로 중단하지 마세요.

엔드포인트를 호출하면 `503 Service Unavailable`이 발생합니다.

---

## AI로 진단하기

**Copilot에 입력하세요:**

```text
My Container App is returning 503. What's wrong?
```

### 6️⃣ `azure-diagnostics` 활성화

진단 체인은 보통 다음 순서로 진행됩니다.

1. **가설 수립**: app crash, ingress misconfiguration, bad image, unhealthy environment 등 다중 가능성 검토
2. **로그 수집**: `az containerapp logs show --type system`로 시스템 로그 조회
3. **로그 상관분석**: `Reason: ProbeFailed` 탐지
4. **설정 검증**: ingress target port(9999)와 컨테이너 listen port(8000, Dockerfile의 gunicorn) 비교
5. **원인/복구 제시**: 올바른 포트로 되돌리는 CLI 명령 제공

> 💡 **스킬 포인트:** `azure-diagnostics`는 단순 문자열 매칭이 아니라 가설 → 증거 → 교차검증 흐름으로 진단합니다.

---

## 복구 적용하기

제시된 복구 명령(예: 아래)을 실행합니다.

```powershell
az containerapp ingress update --name <app> -g <rg> --target-port 8000
```

복구 후 엔드포인트를 다시 확인하면 `200 OK`가 반환됩니다.

✅ **확인 지점:** `curl <your-endpoint-url>`가 다시 LEGO set browser HTML을 반환합니다.

**핵심 정리:** 자연어 질문 하나로 `azure-diagnostics`가 활성화되고, 로그 상관분석 기반의 root cause와 fix를 빠르게 제시합니다.

---

**다음:** [시나리오 4 - 조사하고 운영화하기 →](07-scenario-4-investigate-and-operationalize.ko.md)
