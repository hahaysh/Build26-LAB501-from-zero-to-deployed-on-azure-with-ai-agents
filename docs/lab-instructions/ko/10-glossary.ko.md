# 용어집

LAB501 실습에서 반복적으로 등장하는 핵심 용어를 한국어 기준으로 정리했습니다.

## 플랫폼 및 서비스

| 용어 | 한국어 표현 | 설명 |
| --- | --- | --- |
| Azure Container Apps | Azure Container Apps | 컨테이너 기반 웹앱/백엔드 실행 서비스 |
| Azure Container Registry | Azure Container Registry | 컨테이너 이미지를 저장하는 프라이빗 레지스트리 |
| Azure Cosmos DB | Azure Cosmos DB | 글로벌 분산형 NoSQL 데이터베이스 |
| Azure Functions | Azure Functions | 이벤트/HTTP 기반 서버리스 실행 환경 |
| Log Analytics | Log Analytics | 로그 수집/조회 작업공간 |
| Application Insights | Application Insights | 애플리케이션 모니터링/텔레메트리 서비스 |
| Azure Developer CLI | Azure Developer CLI | `azd` 기반 개발/배포 워크플로 도구 |
| Azure MCP Server | Azure MCP Server | Azure 작업을 도구 형태로 제공하는 MCP 서버 |

## 보안 및 접근 제어

| 용어 | 한국어 표현 | 설명 |
| --- | --- | --- |
| Managed Identity | 관리 ID | 비밀값 없이 Azure 리소스가 다른 서비스에 인증할 수 있도록 하는 신원 |
| System-assigned Managed Identity | 시스템 할당 관리 ID | 리소스와 함께 생성/삭제되는 관리 ID |
| User-assigned Managed Identity | 사용자 할당 관리 ID | 여러 리소스에 재사용 가능한 관리 ID |
| RBAC | 역할 기반 접근 제어 | 역할로 권한을 부여하는 접근 제어 모델 |
| Least Privilege | 최소 권한 | 필요한 권한만 부여하는 보안 원칙 |
| AcrPull | AcrPull 역할 | ACR에서 이미지를 pull할 수 있게 하는 역할 |

## 운영 및 진단

| 용어 | 한국어 표현 | 설명 |
| --- | --- | --- |
| Health Probe | 상태 프로브 | 앱 정상 여부를 확인하는 probe |
| ProbeFailed | ProbeFailed | 상태 프로브 실패 이벤트 |
| Revision | 리비전 | Container App의 배포 버전 단위 |
| Cold Start | 콜드 스타트 | 초기 기동으로 응답이 느려지는 현상 |
| Triage | 트리아지 | 장애 원인 후보를 좁혀 가는 진단 과정 |
| Post-mortem | 사후 분석 | 장애 발생 후 원인/영향/대응을 정리하는 분석 |
| Alert Rule | 경고 규칙 | 특정 조건 충족 시 알림을 발생시키는 규칙 |

## 개발 및 문서

| 용어 | 한국어 표현 | 설명 |
| --- | --- | --- |
| Bicep | Bicep | Azure 인프라를 선언적으로 정의하는 IaC 언어 |
| KQL | KQL | Kusto Query Language, 로그 분석용 질의 언어 |
| Mermaid Diagram | Mermaid 다이어그램 | 코드 블록으로 작성하는 아키텍처/흐름도 |
| Starter App | 스타터 앱 | 실습 시작용 기본 애플리케이션 |
| Scaffold | 스캐폴드 | 기본 파일/구조를 자동 생성하는 작업 |

## 번역 원칙

- Azure 제품명, CLI 명령, 코드 식별자는 영문 원문 유지
- 설명 문장, 실습 가이드, 오류 해석은 한국어 우선
- 검색이 필요한 오류 메시지는 가능하면 영문 원문도 함께 유지

---

**돌아가기:** [한국어 실습 인덱스](README.md)
