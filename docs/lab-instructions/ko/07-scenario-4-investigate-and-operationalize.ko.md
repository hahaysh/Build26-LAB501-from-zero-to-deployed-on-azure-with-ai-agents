# 시나리오 4 — 조사하고 운영화하기 (~15분)

인시던트는 복구되었습니다. 이제 핵심 질문은 두 가지입니다. "다운타임이 얼마나 지속됐는가?" "다음에는 어떻게 자동 감지할 것인가?"

> ⏱️ **로그 수집 지연:** Container App 시스템 로그는 Log Analytics에 반영되기까지 약 5분이 걸릴 수 있습니다.

## 1부 — KQL 기반 사후 분석하기 (~7분)

**Copilot에 입력하세요:**

```text
Query the Log Analytics workspace for my Container App. Show me what happened during the port mismatch incident.
```

### 7️⃣ `azure-diagnostics` 활성화

일반적으로 아래 흐름으로 조사를 구성합니다.

1. **Workspace discovery**: 리소스 그룹에서 Log Analytics workspace 식별
2. **Table exploration**: `ContainerAppSystemLogs_CL` 이벤트 타입 탐색
3. **Event distribution**: `summarize count() by Reason_s`로 ProbeFailed/ReplicaUnhealthy/RevisionUpdate 분포 확인
4. **Incident timeline**: `earliest(TimeGenerated)`/`latest(TimeGenerated)` 기반 다운타임 계산
5. **Recovery confirmation**: `RevisionReady` 이벤트로 복구 확인

> 💡 **스킬 포인트:** 자연어 입력을 바탕으로 KQL을 자동 작성합니다. 생성된 쿼리를 읽고 직접 수정해 보세요.

생성된 쿼리를 복사해 `| where TimeGenerated > ago(1h)`를 추가하거나, `summarize`에 `bin(TimeGenerated, 5m)`를 포함해 시계열로 바꿔 실행해 보세요.

✅ **확인 지점:** ProbeFailed 이벤트, 인시던트 타임라인, 복구 확인용 KQL 결과를 확보했습니다.

---

## 2부 — 운영화하기 (~8분)

> ⚠️ 랩 환경 정책에 따라 일부 명령은 실패할 수 있습니다. 실패하더라도 KQL/Alert 구성 패턴을 이해하는 것이 핵심입니다.

**Copilot에 입력하세요:**

```text
Create a KQL alert rule that fires when ProbeFailed events appear in the Container App system logs.
```

`azure-diagnostics`는 다음을 이어서 수행합니다.

- `ContainerAppSystemLogs_CL` 대상 alert KQL 생성
- threshold/frequency/severity/action group이 포함된 `az monitor scheduled-query create` 명령 제시
- 운영 환경에 맞게 조정할 파라미터 설명

> ⚠️ 사전 요구사항: `az extension add --name scheduled-query --yes`

이어서 아래 질문도 실행해 보세요.

```text
What other alert rules should I have for a production Container App backed by Cosmos DB?
```

일반적으로 replica health, restart loop, high latency, 5xx, memory, Cosmos RU 소비, 429 throttling 관련 제안이 나옵니다.

✅ **확인 지점:** `az monitor scheduled-query list -g <rg> -o table`에 생성된 alert rule이 표시됩니다.

**핵심 정리:** 인시던트 복구 이후 운영화까지 한 번에 연결할 수 있어야 프로덕션 대응 역량이 완성됩니다.

> 💡 **팁:** `--condition`은 DSL 형식이며 raw KQL 자체가 아닙니다. 실제 KQL은 `--condition-query`로 전달되므로 두 파라미터의 테이블/조건 일관성을 확인하세요.

---

**다음:** [문제 해결 가이드 →](08-troubleshooting.ko.md)
