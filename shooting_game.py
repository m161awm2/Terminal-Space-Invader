import curses
import time
import random

# ================= 설정 =================
TICK = 0.05

PLAYER_CHAR = 'A'
INVADER_CHAR = 'W'
BOSS_CHAR = 'M'
BOSS_BULLET = 'o'
BULLET_CHAR = '|'
RAIL_CHAR = '║'
SHIELD_CHAR = 'X'  # 쉴드 표시

MAX_LIFE = 5
BASE_AMMO = 10
BASE_REGEN = 1

MULTI_TIME = 5.0
RAIL_TIME = 3.0
SHIELD_TIME = 25.0  # 쉴드 지속시간 25초
SHIELD_WIDTH = 3

BOSS_HP = 30

MIN_INV_MOVE = 0.1
MIN_BOSS_MOVE = 0.05

SPECIAL_SHOT_INTERVAL = 4.0  # 특수 잡몹 공격 간격

# ================= 메인 =================
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    h, w = stdscr.getmaxyx()

    # ===== 플레이어 =====
    px, py = w // 2, h - 2
    life = MAX_LIFE

    ammo = BASE_AMMO
    max_ammo = BASE_AMMO
    regen = BASE_REGEN
    last_regen = time.time()

    bullets = []

    # ===== 아이템 =====
    inventory = {"multishot": False, "railgun": False, "heal": False, "shield": False}
    multi_until = 0
    rail_until = 0
    shield_on = False
    shield_end = 0

    # ===== 메시지 =====
    msg, msg_end = "", 0
    def set_msg(t, d=2):
        nonlocal msg, msg_end
        msg, msg_end = t, time.time() + d

    # ===== 월드 =====
    round_num = 1
    invaders = []
    inv_dir = 1
    last_inv_move = time.time()
    special_shots = []

    boss = None
    boss_dir = 1
    boss_bullets = []
    last_boss_move = time.time()
    last_boss_shot = 0
    boss_burst_until = 0
    boss_count = 0  # 보스 등장 횟수

    # ===== 라운드 생성 =====
    def spawn_round():
        nonlocal invaders, boss, boss_bullets, boss_count
        invaders, boss_bullets = [], []

        # 일반 인베이더 생성 (최대 20마리)
        num_regular = min(6 + round_num, 20)
        for i in range(num_regular):
            invaders.append({
                "x": 4 + i * 3,
                "y": 3,
                "char": INVADER_CHAR,
                "size": 1,
                "special": False,
                "last_shot": 0
            })

        # 특별 인베이더: 5라운드마다 한 마리씩 추가
        num_special = round_num // 5
        if num_special > 0 and invaders:
            special_indices = random.sample(range(len(invaders)), min(num_special, len(invaders)))
            for idx in special_indices:
                invaders[idx]["special"] = True
                invaders[idx]["char"] = BOSS_CHAR  # M으로 표시

        # 보스 라운드
        if round_num % 10 == 0:
            boss = {"x": w // 2 - 1, "y": 2, "hp": BOSS_HP}
            boss_count += 1
            set_msg("BOSS STAGE!", 3)
        else:
            boss = None

        return boss

    boss = spawn_round()

    # ================= 메인 루프 =================
    while True:
        now = time.time()
        if shield_on and time.time() >= shield_end:
            shield_on = False
        stdscr.clear()

        # ---------- 입력 ----------
        key = stdscr.getch()
        if key == ord('q'):
            if inventory.get("shield", False):
                shield_on = True
                shield_end = now + SHIELD_TIME
                inventory["shield"] = False
                set_msg("SHIELD ACTIVATED (25s)")
            else:
                break
        if key == curses.KEY_LEFT and px > 1:
            px -= 1
        if key == curses.KEY_RIGHT and px < w - 2:
            px += 1

        if key == ord('f') and ammo > 0 and now > rail_until:
            ammo -= 1
            bullets.append({"x": px, "y": py - 1})
            if now < multi_until:
                if px > 1:
                    bullets.append({"x": px - 1, "y": py - 1})
                if px < w - 2:
                    bullets.append({"x": px + 1, "y": py - 1})

        if key == ord('r') and inventory["multishot"]:
            multi_until = now + MULTI_TIME
            inventory["multishot"] = False
            set_msg("ITEM USED: MULTISHOT (5s)")

        if key == ord('t') and inventory["railgun"]:
            rail_until = now + RAIL_TIME
            inventory["railgun"] = False
            set_msg("ITEM USED: RAILGUN (3s)")

        if key == ord('y') and inventory["heal"]:
            life += 2
            inventory["heal"] = False
            set_msg("ITEM USED: HEAL +2")

        # ---------- 탄 재생 ----------
        if now - last_regen >= 1:
            ammo = min(max_ammo, ammo + regen)
            last_regen = now

        rail_on = now < rail_until

        # ---------- 플레이어 총알 ----------
        for b in bullets[:]:
            b["y"] -= 1
            if b["y"] < 1:
                bullets.remove(b)
                continue
            for inv in invaders[:]:
                if inv["x"] == b["x"] and inv["y"] == b["y"]:
                    invaders.remove(inv)
                    bullets.remove(b)
                    break
            if boss and boss["y"] == b["y"] and boss["x"] <= b["x"] <= boss["x"] + 2:
                boss["hp"] -= 1
                bullets.remove(b)

        # ---------- 레일건 ----------
        if rail_on:
            invaders = [i for i in invaders if i["x"] != px]
            if boss and boss["x"] <= px <= boss["x"] + 2:
                boss["hp"] -= 0.1

        # ---------- 잡몹 이동 ----------
        inv_move_interval = max(MIN_INV_MOVE, 0.5 - round_num * 0.02)
        if invaders and now - last_inv_move > inv_move_interval:
            last_inv_move = now
            if any(i["x"] + inv_dir <= 1 or i["x"] + inv_dir >= w - 2 for i in invaders):
                inv_dir *= -1
                for i in invaders:
                    i["y"] += 1
            else:
                for i in invaders:
                    i["x"] += inv_dir

        # ---------- 특수 잡몹 공격 ----------
        for inv in invaders:
            if inv.get("special"):
                if now - inv["last_shot"] > SPECIAL_SHOT_INTERVAL:
                    inv["last_shot"] = now
                    for dx in [-1, 0, 1]:  # 3칸 폭
                        special_shots.append({"x": inv["x"] + dx, "y": inv["y"] + 1})

        # ---------- 특수 잡몹 공격 탄 이동 ----------
        for s in special_shots[:]:
            s["y"] += 1
            # 쉴드가 활성화되어 있으면 제거
            if shield_on and px-1 <= s["x"] <= px+1 and s["y"] == py - 1:
                special_shots.remove(s)
                continue
            if s["y"] == py and px == s["x"]:
                life -= 1
                special_shots.remove(s)
            elif s["y"] >= h:
                special_shots.remove(s)

        # ---------- 보스 ----------
        if boss:
            boss_move_interval = max(MIN_BOSS_MOVE, 0.1667 - (boss_count-1) * 0.005)
            if now - last_boss_move > boss_move_interval:
                last_boss_move = now
                if boss["x"] + boss_dir <= 1 or boss["x"] + boss_dir + 2 >= w - 2:
                    boss_dir *= -1
                boss["x"] += boss_dir

            if now > boss_burst_until and now - last_boss_shot > 3:
                boss_burst_until = now + 1
                last_boss_shot = now

            if now < boss_burst_until and int(now * 10) % 1 == 0:
                boss_bullets.append({
                    "x": boss["x"] + random.randint(0, 2),
                    "y": boss["y"] + 1
                })

        for bb in boss_bullets[:]:
            bb["y"] += 1
            # 쉴드가 활성화되어 있으면 제거
            if shield_on and px-1 <= bb["x"] <= px+1 and bb["y"] == py - 1:
                boss_bullets.remove(bb)
                continue
            if bb["y"] == py and bb["x"] == px:
                life -= 1
                boss_bullets.remove(bb)
            elif bb["y"] >= h:
                boss_bullets.remove(bb)

        # ---------- 라운드 클리어 ----------
        if not invaders and (not boss or boss["hp"] <= 0):
            round_num += 1
            if round_num % 2 == 0:
                item = random.choice(["multishot", "railgun", "heal", "shield"])
                inventory[item] = True
                set_msg(f"ITEM ACQUIRED: {item.upper()}")
            else:
                if random.choice([True, False]):
                    regen += 1
                    set_msg("UPGRADE: REGEN +1")
                else:
                    max_ammo += 3
                    ammo = max_ammo
                    set_msg("UPGRADE: MAX AMMO +3")
            boss = spawn_round()

        # ---------- UI ----------
        stdscr.addstr(
            0, 2,
            f"LIFE:{life} AMMO:{ammo}/{max_ammo} REGEN:{regen} ROUND:{round_num} "
            f"INV_SPEED:{1/inv_move_interval:.1f} "
            f"BOSS_SPEED:{(1/max(MIN_BOSS_MOVE, 0.1 - (boss_count-1)*0.005)):.1f}"
        )

        inv_text = "INV: "
        if inventory["multishot"]:
            inv_text += "[R] MULTI  "
        if inventory["railgun"]:
            inv_text += "[T] RAIL  "
        if inventory["heal"]:
            inv_text += "[Y] HEAL  "
        if inventory.get("shield", False):
            inv_text += "[Q] SHIELD"
        stdscr.addstr(1, 2, inv_text)

        if now < multi_until:
            stdscr.addstr(2, 2, f"MULTISHOT {multi_until-now:.1f}s")
        if now < rail_until:
            stdscr.addstr(3, 2, f"RAILGUN {rail_until-now:.1f}s")
        if shield_on:
            stdscr.addstr(4, 2, f"SHIELD {shield_end-now:.1f}s")

        if now < msg_end:
            stdscr.addstr(h // 3, w // 2 - len(msg) // 2, msg, curses.A_BOLD)

        # ---------- 그리기 ----------
        stdscr.addch(py, px, PLAYER_CHAR, curses.A_BOLD)

        for b in bullets:
            stdscr.addch(b["y"], b["x"], BULLET_CHAR)

        for i in invaders:
            stdscr.addch(i["y"], i["x"], i["char"])

        for s in special_shots:
            if 0 <= s["x"] < w and 0 <= s["y"] < h:
                stdscr.addch(s["y"], s["x"], BOSS_BULLET)

        if rail_on:
            for y in range(1, py):
                stdscr.addch(y, px, RAIL_CHAR, curses.A_REVERSE)

        # 쉴드 표시 (플레이어 위 3칸 폭)
        if shield_on:
            for dx in [-1, 0, 1]:
                if 0 <= px + dx < w:
                    stdscr.addch(py - 1, px + dx, SHIELD_CHAR, curses.A_BOLD)

        if boss:
            for i in range(3):
                stdscr.addch(boss["y"], boss["x"] + i, BOSS_CHAR)
            bar = int((boss["hp"] / BOSS_HP) * 20)
            stdscr.addstr(1, w - 22, "[" + "#" * bar + " " * (20 - bar) + "]")

        for bb in boss_bullets:
            stdscr.addch(bb["y"], bb["x"], BOSS_BULLET)

        if life <= 0:
            stdscr.addstr(h // 2, w // 2 - 5, "GAME OVER\nROUND : %d"%round_num)
            stdscr.refresh()
            time.sleep(2)
            break

        stdscr.refresh()
        time.sleep(TICK)

if __name__ == "__main__":
    curses.wrapper(main)

