# 미디어 출처와 교체 방법

| 파일 | 무엇을 보여주나 | 출처 |
| --- | --- | --- |
| [control-response.png](control-response.png) | 구간별 명령과 1차 모델의 속도 응답 | 합성 입력으로 새로 제작. 실제 주행 영상·로그 미사용 |

## 실측 자료를 추가할 때

실제 촬영본은 합성 예제와 다른 파일명으로 추가하세요. 예를 들어 `media/recordings/patrol-command-response.mp4`와 정지 화면 `media/recordings/patrol-command-response.png`를 둡니다. 연결할 프로젝트 문서에는 촬영일, 로봇 종류, 시험 환경, 관찰한 동작을 적습니다.

실제 데이터와 합성 예제는 각각의 그림 설명을 유지합니다. 실측제어 그래프를 올릴 때는 명령과 odometry의 시간 기준·단위·표본 구간을 표시합니다. 합성 그래프를 설명하는 실험 문서와 생성 코드는 그대로 재현할 수 있습니다.
