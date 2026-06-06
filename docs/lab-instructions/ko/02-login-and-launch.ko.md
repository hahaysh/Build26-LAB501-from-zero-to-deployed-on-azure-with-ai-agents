# 시작 전 — 로그인 및 런치

## 1. Azure 로그인

터미널을 열고(권장: PowerShell 단축키 Ctrl + Shift + 4) 아래 단계를 진행하세요.

```bash
az login
```

로그인 팝업이 나타나면 **Work or school account**를 선택하고 **Continue**를 클릭합니다. Skillable VM의 **Resources** 탭에서 키보드 아이콘을 눌러 사용자 이름을 확인해 입력하고 **Next**를 클릭합니다. 같은 방식으로 TAP를 입력해 로그인 완료합니다. **Sign in to all apps and websites on this device?** 창에서는 **Yes**를 클릭합니다.

터미널에서 구독 선택 프롬프트가 나오면 변경 없이 **Enter**를 누르세요.

> ⚠️ **"Microsoft account"(개인 계정)를 선택하지 마세요.** 로그인 화면에 여러 옵션이 보이더라도 반드시 **Work or school account**를 선택해야 합니다. 잘못 선택하면 access denied 오류가 발생합니다.

## 2. Azure Developer CLI 로그인

```bash
azd auth login
```

이전 단계에서 로그인한 Azure 계정을 선택하고 인증을 완료합니다.

## 3. GitHub 로그인

브라우저에서 다음 링크를 여세요: [https://github.com/enterprises/skillable-events/sso](https://github.com/enterprises/skillable-events/sso). Skillable Events SSO 프롬프트가 나오면 **Continue**를 클릭합니다. 방금 인증한 Azure 계정을 선택한 뒤, 안내에 따라 인증을 마무리합니다.

## 4. GitHub Copilot CLI 로그인

아래 명령으로 GitHub Copilot CLI를 시작합니다.

```bash
copilot
```

대화형 Copilot CLI 세션이 열립니다. 이 랩의 모든 Copilot 입력 프롬프트는 여기에서 입력합니다. **랩이 끝날 때까지 이 세션을 유지하세요.**

> 💡 **Terminal vs. Copilot:** 이 랩에서는 두 위치에서 명령을 실행합니다. **Copilot CLI**는 AI 프롬프트(예: "Deploy my app to Azure")용이고, **터미널 명령**은 `!` 접두사를 붙여 Copilot 내부에서 실행할 수 있습니다(예: `curl`, `az`, `git`).

```bash
/login
```

로그인 계정 선택 프롬프트가 나오면 GitHub.com을 선택합니다. 브라우저 인증을 위해 아무 키나 입력하라는 안내가 나오면 그대로 진행하고, 이미 로그인된 계정으로 권한 부여를 완료합니다.

## 5. Rubberduck Agent 비활성화

랩에서는 필요하지 않으므로 아래 프롬프트로 Copilot CLI의 rubberduck agent를 끕니다.

Copilot에 입력하세요:

```text
 Update the settings.json for Copilot CLI to disable rubber duck with this, "builtInAgents": {"rubberDuck": false},
```

![Copilot CLI에서 Rubber Duck agent 비활성화](../images/disablingRubberDuck.png)

## 6. Azure Skills Plugin 설치

1. Microsoft marketplace 추가: `/plugin marketplace add microsoft/azure-skills`

2. Azure plugin 설치: `/plugin install azure@azure-skills`

3. Azure MCP 리로드: `/mcp reload`

4. **터미널을 닫으세요.** Copilot 설정 변경이 다음 실행 시 반영됩니다.

> 💡 **MCP tools vs. Azure skills:** Azure MCP server는 리소스 조회/로그 질의/배포 관리 같은 저수준 **MCP tools**를 제공합니다. Azure **skills**는 여러 MCP tools를 도메인 지식과 함께 체이닝하는 상위 프롬프트 워크플로입니다. 이 랩은 둘 다 사용합니다.
> 💡 **팁:** 나중에 플러그인을 업데이트하려면 `/plugin update azure@azure-skills`를 실행하세요.

✅ **확인 지점:** GitHub/Azure 로그인 완료, Copilot CLI 실행 중, Azure skills와 Azure MCP Server 설치 완료.

---

**다음:** [스타터 앱 준비 →](03-getting-started.ko.md)
