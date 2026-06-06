# 시나리오 2 — 보고 평가하기 (~10분)

아키텍처 다이어그램은 오래되었거나, 틀렸거나, 아예 없는 경우가 많습니다. AI가 즉시 만들어줄 수는 있지만 정확할까요?

## 1부 — 다이어그램 생성하기 (~4분)

**Copilot에 입력하세요:**

```text
Visualize the resources in my resource group as an architecture diagram.
```

### 5️⃣ `azure-resource-visualizer` 활성화

다음 동작을 확인하세요.

- Azure Resource Graph를 질의해 리소스 그룹의 리소스를 인벤토리화
- 관계 맵핑: Container App → Container Apps Environment → Log Analytics, Container App → ACR
- 서브그래프/리소스 타입/연결 화살표가 포함된 Mermaid 다이어그램 생성
- Mermaid viewer에 붙여 넣을 수 있는 markdown 출력

> 💡 **스킬 포인트:** 이 스킬은 리소스 이름 추측이 아니라 ARM 속성(예: `environmentId`) 기반으로 관계를 추론합니다.
> 💡 **Cosmos DB 주의:** 앱이 참조하는 Cosmos DB가 다른 리소스 그룹에 있으면 자동 다이어그램에서 누락될 수 있습니다. cross-resource-group 의존성은 사람이 검증해야 합니다.

---

## 2부 — 다이어그램 평가하기 (~6분)

생성된 markdown을 열어 아래 관점으로 검토하세요.

- 배포된 리소스(Container App, Environment, ACR, Log Analytics)가 모두 보이는가?
- 관계가 맞는가? ACR → Container App pull 경로가 보이는가?
- Cosmos DB 의존성이 표시되는가? 없다면 중요한 누락입니다.
- 프로덕션 아키텍처 리뷰 관점에서 무엇이 빠졌는가?

**Copilot에 입력하세요:**

```text
What's missing from this architecture for a production deployment? The app also connects to an existing Cosmos DB for its data.
```

Scenario 1B에서 찾은 보안/운영 격차와 AI 제안을 비교해 보세요.

✅ **확인 지점:** 연결 화살표가 포함된 Mermaid 다이어그램을 확보했습니다. 렌더링은 [mermaid.live](https://mermaid.live), VS Code Mermaid 확장, 또는 GitHub markdown에서 가능합니다.

**핵심 정리:** `azure-resource-visualizer`는 "현재 무엇이 배포되어 있는가"를 빠르게 파악하는 데 매우 강력하지만, 문서로 쓰기 전에 전문가 검토가 필요합니다.

---

**다음:** [시나리오 3 - 장애를 내고 진단하기 →](06-scenario-3-break-and-triage.ko.md)
