# Private MCP Development — v0.1.0

근거 확인일: 2026-09-10. 한국어 연구 기반 개발 스킬 초안이다. 별도의 MCP 서버 구현이나 배포 제품이 아니다. 35개 핵심 출처, 16개 공통 검토 영역, 36개 인수 시험 설계를 연결한다.

> 이 저장소는 Private MCP 개발 공통 설계 스킬의 소스 원본을 관리한다. `.docx`, `.zip`, 패키지 해시처럼 다시 생성할 수 있는 배포 산출물은 저장하지 않고, 검토·변경·시험 가능한 텍스트 소스와 코드만 추적한다.

## 시작

`SKILL.md`를 먼저 읽고, 필요한 프로파일·통제·시험 문서만 추가로 읽는다. 파일 기반 Agent Skills를 지원하는 호스트에서 사용할 수 있도록 구성했지만, 특정 호스트에서 설치·호출·정책 집행을 실제 시험한 것은 아니다. 이 저장소를 복제한 것만으로 프로젝트 전체에 자동 등록되거나 활성화되지 않는다.

`assets/project-manifest.template.json`을 프로젝트 작업 폴더에 복사한 뒤 설계·검증 기록을 작성한다. 빈 값과 `not_run`은 의도적인 초기 상태다. 실제 증거 없이 이를 완료·통과로 바꾸지 않는다. `tool-contract.template.json`은 도구별 설계 계약이며 MCP wire 메시지나 실행 설정이 아니다.

## 기록 구조 검사기

Python 3.10 이상 표준 라이브러리만 필요하다. 네트워크·서버 호출·외부 명령 실행은 하지 않는다. 저장소 루트에서 다음 명령을 실행한다.

```bash
python scripts/validate_artifacts.py assets/project-manifest.template.json
python scripts/validate_artifacts.py /path/to/project-manifest.json --release-record
python scripts/validate_artifacts.py /path/to/project-manifest.json --release-record --as-of 2026-09-10
python -m unittest discover -s tests -v
```

기본 모드는 JSON 구조·필수 필드 유형·카탈로그 ID를 확인한다. 빈 설계 양식도 구조가 맞으면 성공한다. `--release-record`는 적용 판단·완료 상태·증거 참조·검토자·날짜 등 제출된 릴리스 기록의 완결성을 추가 확인한다. 실제 운영 준비 완료를 판정하는 명령이 아니다.

종료 코드 0은 해당 **기록 검사** 통과, 1은 기록 문제, 2는 입력 파일·인수 문제다. 구조 검사 결과만으로 증거의 진위, 참조 URI의 존재, 실제 인증·인가·보안 통제, protocol conformance, 성능, 모델·호스트 평가의 성공을 확인할 수 없다. 합성 문자열을 넣은 가짜 기록도 형식 조건을 충족할 수 있으므로 독립적인 증거 검토가 필요하다.

`--as-of`는 예외 만료와 검토 날짜의 비교 기준을 지정하며 생략하면 실행 환경의 로컬 날짜를 사용한다. 이 옵션을 과거로 돌려 만료 정책을 우회하는 것은 허용된 운영 절차가 아니다.

## 입력 기록 보충

`compatibility.hosts` 항목은 `name`, `version`, `transport`, `evidence` 배열을 포함한다. `profiles`는 프로젝트 분류 P1–P7을 사용한다. 구체적 고정 버전/커밋이 실제 불변인지, 호스트가 지원하는지는 사람이 별도 확인한다.

`controls`의 `not_applicable`도 검토 판단이다. 릴리스 기록 모드에서는 책임자·이유·메커니즘 설명·검토 증거를 요구한다. 구현할 기능이 없으면 그 이유와 경계가 왜 충족되는지 설명한다. 통제 영역 자체를 무시한다는 뜻이 아니다.

조건부 `tests`를 적용 제외하려면 `applicable: false`, `status: "not_applicable"`, 이유와 검토 증거를 남긴다. 모든 서버에서 검토할 시험은 적용 제외로 완료 처리할 수 없다. 추가 업무 시험은 별도 부록에 기록하거나 카탈로그·검사기 버전을 함께 변경한다.

예외 항목의 필드는 `id`, `kind: "project_policy"`, `controls`, `reason`, `risk`, `compensating_control`, `approver`, `expires_at`, `approved`다. 예외를 등록해도 미통과 시험을 검사기가 자동 통과시키지 않는다. 사양 MUST 위반을 예외로 ‘사양 적합’으로 바꾸지 않는다.

## 파일 구성

`references/protocol-profiles.md`: 버전·전송·인증·상태·조건별 프로파일.

`references/security-controls.md`: C01–C16의 질문·강제 위치·근거·시험 연결.

`references/validation.md`: T01–T36의 적용 조건·절차·판정·기록.

`references/case-studies.md`: 공개 개발 사례와 연구의 관찰·설계 추론 구분.

`references/research-evidence.md`, `references/sources.json`: 출처·날짜·활용 범위.

`assets/`: 설계·도구 계약·호환성·릴리스·결정 양식과 기계 판독 카탈로그.

`scripts/`, `tests/`: 기록 구조 검사기와 합성 데이터 기반 자체 시험.

## 제작 시 검증 범위

검사기 자체 시험 18개 통과, 빈 양식의 구조 검사 통과, 빈 양식의 릴리스 기록 검사 실패를 확인했다. 카탈로그의 통제·시험·출처 ID 연결도 자체 시험에 포함한다. 실제 MCP 서버 시험 T01–T36, 인용한 벤치마크 재현, 호스트 설치·활성화는 수행하지 않았다.

공개 문서와 논문은 원 출처의 조건·버전 안에서 해석한다. 본문을 그대로 복제한 자료나 제3자 서버 코드는 포함하지 않았으며, 연구 요약과 새로 작성한 양식·검사기를 제공한다.
