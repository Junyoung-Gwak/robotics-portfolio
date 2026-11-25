# 미디어 출처와 교체 방법

| 파일 | 무엇을 보여주나 | 출처 |
| --- | --- | --- |
| [control-response.png](control-response.png) | 구간별 명령과 1차 모델의 속도 응답 | 합성 입력으로 새로 제작. 실제 주행 영상·로그 미사용 |
| [grid-search.mp4](grid-search.mp4) · [GIF](grid-search.gif) · [정지 화면](grid-search.png) | 동일한 합성 격자의 Dijkstra·A* 확장 순서 | 새로 작성한 Python 탐색 결과에서 렌더링. 현장 촬영본과 별도 |

## 실측 자료를 추가할 때

실제 촬영본은 합성 예제와 다른 파일명으로 추가하세요. 예를 들어 `media/recordings/patrol-command-response.mp4`와 정지 화면 `media/recordings/patrol-command-response.png`를 둡니다. 연결할 프로젝트 문서에는 촬영일, 로봇 종류, 시험 환경, 관찰한 동작을 적습니다.

실제 데이터와 합성 예제는 각각의 그림 설명을 유지합니다. 실측제어 그래프를 올릴 때는 명령과 odometry의 시간 기준·단위·표본 구간을 표시합니다. 합성 그래프를 설명하는 실험 문서와 생성 코드는 그대로 재현할 수 있습니다.

주차 시연을 촬영한다면 한 화면에 시작·목표와 차량의 실제 이동이 보이게 하고 개입 여부를 기록합니다. `projects/navigation.md`에 촬영본과 캡션을 추가하면 됩니다. `labs/path-search.md`의 27·217·125는 합성 시나리오 전용 수치입니다.

### 프로젝트 시연 자리 교체

저장소 루트에서 아래처럼 실행합니다. 날짜, 입력 파일 경로, 캡션은 실제 촬영 내용으로 입력하세요.

```sh
python tools/register_demo.py navigation "/path/to/recording.mp4" --kind recorded --date YYYY-MM-DD --caption "촬영 장소와 관찰한 동작"
```

이 명령은 원본을 복사하고 해당 프로젝트 문서의 시연 부분만 교체합니다. 파일명에는 내용의 해시가 들어가 이전 자료를 보존합니다. 포스터를 함께 쓰려면 `--poster "/path/to/still.png"`를 붙입니다. `--preview`는 파일을 바꾸기 전 표시될 문구를 보여줍니다. 설명용으로 제작한 미디어는 `--kind generated`를 선택합니다. 사용 가능한 프로젝트 키는 `navigation`, `localization`, `perception`, `integration`, `robot-cells`입니다.
