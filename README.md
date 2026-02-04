🚀 Terminal Space Invader (Python Curses)리눅스 터미널 환경에서 가볍게 즐길 수 있는 아케이드 스타일 슈팅 게임입니다. 외부 엔진 없이 파이썬 표준 라이브러리인 curses만을 사용하여 고전 게임의 감성을 재현했습니다.🎮 게임 조작법 (Controls)키 (Key)기능 (Action)상세 설명← / →이동플레이어 기체를 좌우로 조작합니다.f공격탄환을 발사합니다. (AMMO 소모)r멀티샷[아이템] 5초간 전방 3방향으로 탄환을 발사합니다.t레일건[아이템] 3초간 직선상의 모든 적을 관통하는 레이저를 쏩니다.q종료게임을 즉시 종료하고 터미널로 돌아갑니다.🛠️ 주요 기술 스택 (Technical Features)이 프로젝트는 다음과 같은 기술적 요소들을 포함하고 있습니다:Real-time Game Loop: nodelay 모드를 활성화하여 사용자 입력과 상관없이 게임 화면이 실시간(TICK = 0.05)으로 갱신되도록 설계되었습니다.Dynamic Resource System:AMMO & REGEN: 무분별한 연사를 방지하기 위해 탄환 제한 및 자동 재생 로직을 적용했습니다.Upgrade System: 라운드 클리어 시 random 라이브러리를 활용해 공격 속도나 탄환 한계를 강화하는 성장 요소를 넣었습니다.Boss Pattern Logic: 10라운드마다 등장하는 보스는 일반 적과 다른 이동 알고리즘 및 탄막 살포(Burst Shot) 패턴을 가집니다.Collision Detection: 캐릭터와 탄환의 좌표값을 비교하여 실시간 충돌 판정을 수행합니다.🚀 설치 및 실행 (Setup)별도의 라이브러리 설치가 필요 없습니다. 파이썬 3가 설치된 리눅스나 macOS 환경이라면 바로 실행 가능합니다.Bash# 1. 저장소 클론
git clone https://github.com/사용자아이디/저장소이름.git

# 2. 폴더 이동
cd 저장소이름

# 3. 게임 실행
python3 shooting_game.py
📝 개발 노트그래픽: ASCII 문자를 활용한 텍스트 렌더링최적화: stdscr.clear()와 refresh()를 조합하여 화면 깜빡임을 최소화했습니다.
