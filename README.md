<p align="center">
<img src="img/banner-build-26.png" alt="Microsoft Build 2026" width="1200"/>
</p>

# [Microsoft Build 2026](https://build.microsoft.com)

## 🔥 LAB501: Azure AI 에이전트로 시작부터 배포까지

### 세션 설명

이 실습에서는 GitHub Copilot CLI와 Azure skills를 사용해 빈 터미널 상태에서 실제 Azure 배포까지 진행합니다. 참가자는 Python Flask 기반 LEGO 세트 브라우저와 Azure Function App을 함께 배포하고, AI가 생성한 Bicep과 아키텍처 결정을 검토하면서 보안 강화, 장애 유도, 진단, 운영화까지 단계적으로 수행합니다.

75분 동안(Level 300) 하나의 Copilot 프롬프트에서 두 개의 서비스를 배포합니다. 하나는 Azure Container Apps에서 실행되는 Python **Flask LEGO 세트 브라우저**이고, 다른 하나는 Azure Cosmos DB에 LEGO 세트를 일괄 upsert하는 Python **Azure Function App**입니다. 이후 생성된 Bicep을 검토하고, managed identity + RBAC 기반으로 배포를 강화하고, 의도적으로 장애를 만든 뒤, KQL로 포렌식 조사까지 수행합니다.

### 🏫 가이드 세션으로 시작하기

- Skillable lab VM에 로그인하고 **Docker Desktop**을 실행합니다.
- PowerShell을 열고 `az login`, `azd auth login`, `copilot` 순서로 실행합니다. Azure Skills plugin 설치는 [시작 전 - 로그인 및 런치](docs/lab-instructions/ko/02-login-and-launch.ko.md)를 참고하세요.
- 실습은 [한국어 개요](docs/lab-instructions/ko/00-overview.ko.md) 또는 [한국어 실습 인덱스](docs/lab-instructions/ko/README.md)에서 시나리오 순서대로 진행합니다.

### 🇰🇷 한국어 빠른 시작 (Build Localhost Seoul)

한국 참가자는 아래 순서로 진행하면 가장 빠르게 완주할 수 있습니다.

1. Skillable VM 로그인 후 Docker Desktop 실행
2. PowerShell에서 `az login`, `azd auth login`, `copilot` 순서로 로그인
3. 한국어 실습 문서 인덱스에서 시나리오 순서대로 진행:
    [docs/lab-instructions/ko/README.md](docs/lab-instructions/ko/README.md)

핵심 동선 바로가기:

- [개요](docs/lab-instructions/ko/00-overview.ko.md)
- [시작 전 - 로그인 및 런치](docs/lab-instructions/ko/02-login-and-launch.ko.md)
- [시나리오 1 - Ship It & Harden It](docs/lab-instructions/ko/04-scenario-1-ship-and-harden.ko.md)
- [문제 해결 가이드](docs/lab-instructions/ko/08-troubleshooting.ko.md)

### 🏠 내 환경에서 시작하기

- 리포지토리를 클론합니다: `git clone https://github.com/microsoft/Build26-LAB501.git`
- [사전 준비](docs/lab-instructions/ko/01-prerequisites.ko.md)를 설치합니다: Python 3.13+, Docker Desktop, Git, Azure CLI(Bicep 포함), Azure Developer CLI(`azd`), GitHub Copilot CLI, Contributor 권한의 Azure subscription
- LEGO 데이터셋이 포함된 Azure Cosmos DB를 직접 준비한 뒤(database `LegoDatabase`, container `legoSets`), [스타터 앱 준비](docs/lab-instructions/ko/03-getting-started.ko.md)부터 네 개의 시나리오를 순서대로 진행합니다.

### 🧠 학습 목표

- GitHub Copilot CLI에서 하나의 자연어 프롬프트로 `azure-prepare` → `azure-validate` → `azure-deploy` 체인을 호출해 컨테이너 앱을 배포할 수 있습니다.
- AI가 생성한 Bicep, Dockerfile, 아키텍처 다이어그램을 검토해 프로덕션 격차를 식별하고 보완할 수 있습니다.
- `azure-diagnostics`를 사용해 503 장애를 진단하고, KQL과 alert rule로 운영화까지 연결할 수 있습니다.

### 💬 Copilot으로 더 학습하기

아래 프롬프트를 GitHub Copilot에 넣어 이번 세션의 주제를 더 탐색해 볼 수 있습니다. VS Code에서 Copilot Chat을 열고(`Ctrl+Alt+I` 또는 `Cmd+Shift+I`) 프롬프트를 붙여 넣어 결과를 확인해 보세요. 최신 공식 문서를 함께 보려면 [Microsoft Learn MCP Server](#-microsoft-learn-mcp-server) 연결도 권장합니다.

아래 예시는 출발점입니다. 필요하면 그대로 복사하거나 목적에 맞게 수정해 사용하세요.

- KR: "ACR pull과 Cosmos DB 접근에 managed identity를 적용해, Bicep과 `azd`로 Azure Container Apps의 Python Flask 앱 **그리고** Python Azure Function App을 함께 스캐폴딩해줘."
    EN: "Scaffold a Python Flask app on Azure Container Apps **and** a Python Azure Function App with Bicep and `azd`, using managed identity for ACR pulls and Cosmos DB access."
- KR: "내 Container App Bicep을 프로덕션 관점에서 검토해줘. managed identity, RBAC, VNet 통합, 진단 설정, 헬스 프로브의 갭을 찾고 수정안을 제안해줘."
    EN: "Review my Container App Bicep for production-readiness gaps — managed identity, RBAC, VNet integration, diagnostic settings, and health probes — and propose fixes."
- KR: "데이터 읽기 전용 앱에 필요한 최소 권한 Cosmos DB RBAC 역할을 찾아주고, `az cosmosdb sql role assignment create` 명령을 생성해줘."
    EN: "Find the minimum-privilege Cosmos DB RBAC role for an app that only reads data, and generate the `az cosmosdb sql role assignment create` command."
- KR: "내 리소스 그룹의 리소스를 Mermaid 아키텍처 다이어그램으로 시각화해줘. Cosmos DB 같은 교차 리소스 그룹 의존성도 포함해줘."
    EN: "Visualize the resources in my resource group as a Mermaid architecture diagram, including cross-resource-group dependencies like Cosmos DB."
- KR: "내 Container App이 503을 반환하고 있어. 시스템 로그를 수집하고 ingress 설정과 상관 분석해서 원인과 해결책을 알려줘."
    EN: "My Container App is returning 503. Pull system logs, correlate with ingress configuration, and tell me the root cause and fix."
- KR: "`ContainerAppSystemLogs_CL`에서 첫 `ProbeFailed` 이벤트와 다음 `RevisionReady` 이벤트 사이 다운타임을 계산하는 KQL을 작성하고, 이를 `az monitor scheduled-query create` 경고 규칙으로 만들어줘."
    EN: "Write a KQL query against `ContainerAppSystemLogs_CL` that calculates downtime between the first `ProbeFailed` event and the next `RevisionReady` event, then turn it into an `az monitor scheduled-query create` alert rule."

### 💻 사용 기술

1. GitHub Copilot CLI + Azure Skills plugin (`azure-prepare`, `azure-validate`, `azure-deploy`, `azure-rbac`, `azure-resource-visualizer`, `azure-diagnostics`) + Azure MCP Server
2. Azure Container Apps, **Azure Functions (Python, Flex Consumption)**, Azure Container Registry, Azure Cosmos DB(NoSQL), managed identity + RBAC
3. Azure Developer CLI(`azd`), Bicep, Docker, Python 3.13 / Flask, Azure Monitor + Log Analytics, KQL

### 📚 참고 자료와 다음 단계

| 자료 | 설명 |
| :--------- | :------------ |
| [https://aka.ms/build26-next-steps](https://aka.ms/build26-next-steps) | Build 2026 이후 학습을 확장하기 위한 다음 단계 |
| [한국어 개요](docs/lab-instructions/ko/00-overview.ko.md) | 아키텍처 다이어그램, skills 맵, 섹션별 실습 안내 |
| [What's Next](docs/lab-instructions/09-whats-next.md) | private endpoints, VNet integration, Key Vault, OIDC 기반 CI/CD, Terraform 확장 아이디어 |
| [Announcing the Azure Skills Plugin](https://devblogs.microsoft.com/all-things-azure/announcing-the-azure-skills-plugin/) | 이 실습에서 사용하는 Azure skills 배경 설명 |
| [Azure MCP Server docs](https://learn.microsoft.com/azure/developer/azure-mcp-server) | Azure skills를 구동하는 MCP 도구 참고 문서 |
| [GitHub Copilot CLI docs](https://docs.github.com/en/copilot/github-copilot-in-the-cli) | GitHub Copilot CLI 설치, 설정, 확장 문서 |
| [Deploy and manage Container Apps](https://learn.microsoft.com/training/paths/deploy-manage-container-apps) | Azure Container Apps 학습 경로 |
| [Azure Cosmos DB documentation](https://learn.microsoft.com/azure/cosmos-db) | Cosmos DB의 데이터 모델링, RBAC, 운영 가이드 |

### 한국어 참고 자료

- [한국어 실습 인덱스](docs/lab-instructions/ko/README.md)
- [한국어 개요](docs/lab-instructions/ko/00-overview.ko.md)
- [한국어 용어집](docs/lab-instructions/ko/10-glossary.ko.md)

### 🌟 Microsoft Learn MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D)

Microsoft Learn MCP Server는 GitHub Copilot 같은 AI 클라이언트가 Microsoft 공식 문서의 최신 정보를 직접 가져올 수 있게 해 주는 원격 MCP Server입니다. 위의 원클릭 버튼으로 VS Code에 설치하거나, 이 리포에 포함된 [mcp.json](.vscode/mcp.json)을 직접 참고해 설정할 수 있습니다.

추가 설정 방법, 다른 개발 클라이언트용 안내, 질문/의견 등록은 Learn MCP Server GitHub 리포지토리([https://github.com/MicrosoftDocs/MCP](https://github.com/MicrosoftDocs/MCP))를 참고하세요. 다른 MCP Server 탐색은 [https://mcp.azure.com](https://mcp.azure.com)에서 가능합니다.

*참고: Learn MCP Server를 사용하면 [Microsoft Learn](https://learn.microsoft.com/en-us/legal/termsofuse) 및 [Microsoft API Terms](https://learn.microsoft.com/en-us/legal/microsoft-apis/terms-of-use) 약관에 동의하는 것으로 간주됩니다.*

## Content Owners

<table>
<tr>
    <td align="center"><a href="http://github.com/yunjchoi">
        <img src="https://github.com/yunjchoi.png" width="100px;" alt="Yun Jung Choi"/><br />
        <sub><b>Yun Jung Choi</b></sub></a><br />
            <a href="https://github.com/yunjchoi" title="talk">📢</a>
    </td>
</tr></table>

## 기여 안내

이 프로젝트는 기여와 제안을 환영합니다. 대부분의 기여는 Contributor License Agreement(CLA)에 동의해야 하며, 자세한 내용은 [Contributor License Agreements](https://cla.opensource.microsoft.com)에서 확인할 수 있습니다.

Pull Request를 제출하면 CLA bot이 자동으로 동의 필요 여부를 확인하고 필요한 안내를 제공합니다. 안내에 따라 한 번만 진행하면 동일한 CLA를 사용하는 다른 리포에서도 재사용됩니다.

이 프로젝트는 [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)를 따릅니다. 추가 정보는 [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)를 참고하거나 [opencode@microsoft.com](mailto:opencode@microsoft.com)으로 문의하세요.

## 상표

이 프로젝트에는 제품, 서비스, 프로젝트 관련 상표 또는 로고가 포함될 수 있습니다. Microsoft 상표 또는 로고 사용은 [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general)을 따라야 합니다. 수정된 버전에서 Microsoft 상표나 로고를 사용할 때는 Microsoft의 공식 후원처럼 보이거나 혼동을 일으켜서는 안 됩니다. 제3자 상표와 로고는 해당 정책을 따릅니다.
