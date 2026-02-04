# 🚀 Terminal Space Invader (아이디어 추천받음)

**Terminal Space Invader**는 리눅스 터미널 환경에서 가볍게 즐길 수 있는 아케이드 스타일 슈팅 게임입니다.  
외부 엔진 없이 파이썬 표준 라이브러리인 `curses`만을 사용하여 고전 게임의 감성을 재현했습니다. 🎮

---

## 🕹️ 게임 조작법 (Controls)

| 키 (Key) | 기능 (Action)         | 상세 설명 |
|----------|---------------------|-----------|
| ← / →    | 이동                | 플레이어 기체를 좌우로 이동합니다. |
| f        | 공격                | 탄환을 발사합니다. (AMMO 소모) |
| r        | MULTI SHOT [아이템]     | 5초간 전방 3방향으로 탄환을 발사합니다. |
| t        | Bon's RAIL [아이템]     | 3초간 직선상의 모든 적을 관통하는 레이저를 쏩니다. |
| q        | SHIED                | 정면과 옆에서 모든 공격을 막아내는 방패를 생성합니다. |
| y        | HEAL                | 즉시 생명력을 2 만큼 회복합니다. |
| q        | 종료                | 게임을 즉시 종료하고 터미널로 돌아갑니다. |

---

## 🛠️ 주요 기술 스택 (Technical Features)

- **Real-time Game Loop**  
  `nodelay` 모드를 활성화하여 사용자 입력과 상관없이 게임 화면이 실시간(`TICK = 0.05`)으로 갱신됩니다.

- **Dynamic Resource System**  
  - **AMMO & REGEN**: 무분별한 연사를 방지하기 위해 탄환 제한 및 자동 재생 로직 적용.

- **Upgrade System**  
  라운드 클리어 시 `random` 라이브러리를 활용해 공격 속도나 탄환 한계를 강화하는 성장 요소 포함.

- **Boss Pattern Logic**  
  10라운드마다 등장하는 보스는 일반 적과 다른 이동 알고리즘 및 탄막 살포(Burst Shot) 패턴 적용.

- **Collision Detection**  
  캐릭터와 탄환의 좌표값을 비교하여 실시간 충돌 판정 수행.

---

## 🚀 설치 및 실행 (Setup)

별도의 라이브러리 설치가 필요 없습니다.  
파이썬 3이 설치된 리눅스 또는 macOS 환경에서 바로 실행 가능합니다.

```bash
# 1. 저장소 클론
git clone https://github.com/사용자아이디/저장소이름.git

# 2. 폴더 이동
cd 저장소이름

# 3. 게임 실행
python3 shooting_game.py
