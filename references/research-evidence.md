# 연구 근거 인덱스

근거 확인일: 2026-09-10. 아래 목록은 설계 근거를 추적하기 위한 인덱스다. 가변 문서는 확인일의 내용으로 한정하며, 문서를 읽은 것과 해당 구현을 직접 실행 검증한 것을 구분한다.

| ID | 출처 | 활용 범위 |
|---|---|---|
| R01 | MCP Specification 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28 | 프로토콜 범위와 구현 책임 |
| R02 | Versioning and Compatibility — https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | Modern/Legacy/Dual-era와 버전 처리 |
| R03 | Key Changes — https://modelcontextprotocol.io/specification/2026-07-28/changelog | 변경점·확장·폐기 예정 기능 |
| R04 | Streamable HTTP — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | HTTP 전송·Origin·스트림 |
| R05 | stdio — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio | 로컬 프로세스 전송 경계 |
| R06 | Tools — https://modelcontextprotocol.io/specification/2026-07-28/server/tools | 도구 계약·오류·상태 |
| R07 | Authorization — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | HTTP 인증·인가 프로파일 |
| R08 | Authorization Security Considerations — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations | 토큰 대상·PKCE·리디렉션·자격증명 |
| R09 | Client Registration — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration | 등록 방식과 호환성 |
| R10 | MCP Security Best Practices — https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | 토큰 위임·SSRF·로컬 실행 경계 |
| R11 | Multi Round-Trip Requests — https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr | requestState 무결성·결속 |
| R12 | Caching — https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching | 캐시 범위·인증 문맥 격리 |
| R13 | Cancellation — https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation | 취소 의미와 전송 처리 |
| R14 | Tasks Extension — https://modelcontextprotocol.io/extensions/tasks/overview | 장기 작업 선택 확장 |
| R15 | OAuth Client Credentials Extension — https://modelcontextprotocol.io/extensions/auth/oauth-client-credentials | 기계 신원 선택지 |
| R16 | Enterprise-Managed Authorization — https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization | 조직 인증 정책 연동 |
| R17 | SEP-414 Request Metadata — https://modelcontextprotocol.io/seps/414-request-meta | 추적 문맥 전파 |
| R18 | GitHub MCP Server — https://github.com/github/github-mcp-server | 도구 노출·읽기 전용·Lockdown의 한계 |
| R19 | Spotify Engineering, Context engineering Part 2 — https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2 | 제한 도구·검증 추상화 |
| R20 | Spotify Engineering, Feedback loops Part 3 — https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3 | 독립 검증·완료 경로 |
| R21 | Spotify Ads API / Claude plugins — https://engineering.atspotify.com/2026/5/spotify-ads-api-claude-plugins | MCP 채택 여부 비교 사례 |
| R22 | Cloudflare Authorization for MCP servers — https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/ | OAuth·SSO 연동 예시 |
| R23 | Anthropic, Writing effective tools for agents — https://www.anthropic.com/engineering/writing-tools-for-agents | 작업 중심 도구 설계·과제 평가 |
| R24 | Invariant Labs GitHub MCP demonstration — https://invariantlabs.ai/blog/mcp-github-vulnerability | 비신뢰 콘텐츠와 정보 흐름 위험 |
| R25 | MCPTox — https://arxiv.org/abs/2508.14925 | 악성 도구 메타데이터 평가 관점 |
| R26 | MCP-Bench — https://arxiv.org/abs/2508.20453 | 복합 업무 수행 평가 |
| R27 | MCP-SafetyBench — https://arxiv.org/html/2512.15163v2 | 다중 턴·다중 서버 안전성 평가 |
| R28 | MCP Reference Servers — https://github.com/modelcontextprotocol/servers | 교육용 예시와 운영 구현의 구분 |
| R29 | MCP Conformance — https://github.com/modelcontextprotocol/conformance | requirement set·skip·expected failure 해석 |
| R30 | Agent Skills Specification — https://agentskills.io/specification | SKILL.md와 progressive loading 구조 |
| R31 | OWASP Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | 기본 거부·최소 권한·객체별 인가 |
| R32 | OWASP SSRF Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | 내부 목적지·리디렉션·네트워크 통제 |
| R33 | OWASP OS Command Injection Defense Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html | 실행 인수 검증·권한 축소 |
| R34 | NIST SP 800-207 Zero Trust Architecture — https://csrc.nist.gov/pubs/sp/800/207/final | 네트워크 위치만으로 신뢰하지 않는 원칙 |
| R35 | SLSA v1.2 — https://slsa.dev/spec/v1.2/ | 빌드 출처·산출물 무결성 참조 |

특정 논문의 과거 수치나 특정 공개 서버의 관찰을 현재 프로젝트의 취약률·적합성으로 그대로 일반화하지 않는다. 실제 지원·보안·업무 성공은 선택한 호스트·SDK·정책·도구 조합에서 다시 검증한다.
