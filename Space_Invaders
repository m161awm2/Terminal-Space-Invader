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

MAX_LIFE = 5
BASE_AMMO = 10
BASE_REGEN = 1

MULTI_TIME = 5.0
RAIL_TIME = 3.0

BOSS_HP = 30


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
    inventory = {"multishot": False, "railgun": False}
    multi_until = 0
    rail_until = 0

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

    boss = None
    boss_dir = 1
    boss_bullets = []
    last_boss_move = time.time()
    last_boss_shot = 0
    boss_burst_until = 0

    # ===== 라운드 생성 =====
    def spawn_round():
        nonlocal invaders, boss, boss_bullets
        invaders, boss_bullets = [], []
        boss = None

        if round_num % 10 == 0:
            boss = {"x": w // 2 - 1, "y": 2, "hp": BOSS_HP}
            set_msg("BOSS STAGE!", 3)
        else:
            for i in range(6 + round_num):
                invaders.append({"x": 4 + i * 3, "y": 3})

    spawn_round()

    # ================= 메인 루프 =================
    while True:
        now = time.time()
        stdscr.clear()

        # ---------- 입력 ----------
        key = stdscr.getch()
        if key == ord('q'):
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

        # ---------- 탄 재생 ----------
        if now - last_regen >= 1:
            ammo = min(max_ammo, ammo + regen)
            last_regen = now

        rail_on = now < rail_until

        # ---------- 총알 ----------
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
        if invaders and now - last_inv_move > 0.5:
            last_inv_move = now
            if any(i["x"] + inv_dir <= 1 or i["x"] + inv_dir >= w - 2 for i in invaders):
                inv_dir *= -1
                for i in invaders:
                    i["y"] += 1
            else:
                for i in invaders:
                    i["x"] += inv_dir

        # ---------- 보스 ----------
        if boss:
            if now - last_boss_move > 0.1:
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
            if bb["y"] == py and bb["x"] == px:
                life -= 1
                boss_bullets.remove(bb)
            elif bb["y"] >= h:
                boss_bullets.remove(bb)

        # ---------- 라운드 클리어 ----------
        if not invaders and (not boss or boss["hp"] <= 0):
            round_num += 1

            if round_num % 2 == 0:
                item = random.choice(["multishot", "railgun"])
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

            spawn_round()

        # ---------- UI ----------
        stdscr.addstr(
            0, 2,
            f"LIFE:{life} AMMO:{ammo}/{max_ammo} REGEN:{regen} ROUND:{round_num}"
        )

        inv_text = "INV: "
        if inventory["multishot"]:
            inv_text += "[R] MULTI  "
        if inventory["railgun"]:
            inv_text += "[T] RAIL"
        stdscr.addstr(1, 2, inv_text)

        if now < multi_until:
            stdscr.addstr(2, 2, f"MULTISHOT {multi_until-now:.1f}s")
        if now < rail_until:
            stdscr.addstr(3, 2, f"RAILGUN {rail_until-now:.1f}s")

        if now < msg_end:
            stdscr.addstr(h // 3, w // 2 - len(msg) // 2, msg, curses.A_BOLD)

        # ---------- 그리기 ----------
        stdscr.addch(py, px, PLAYER_CHAR, curses.A_BOLD)

        for b in bullets:
            stdscr.addch(b["y"], b["x"], BULLET_CHAR)

        for i in invaders:
            stdscr.addch(i["y"], i["x"], INVADER_CHAR)

        if rail_on:
            for y in range(1, py):
                stdscr.addch(y, px, RAIL_CHAR, curses.A_REVERSE)

        if boss:
            for i in range(3):
                stdscr.addch(boss["y"], boss["x"] + i, BOSS_CHAR)
            bar = int((boss["hp"] / BOSS_HP) * 20)
            stdscr.addstr(1, w - 22, "[" + "#" * bar + " " * (20 - bar) + "]")

        for bb in boss_bullets:
            stdscr.addch(bb["y"], bb["x"], BOSS_BULLET)

        if life <= 0:
            stdscr.addstr(h // 2, w // 2 - 5, "GAME OVER")
            stdscr.refresh()
            time.sleep(2)
            break

        stdscr.refresh()
        time.sleep(TICK)


if __name__ == "__main__":
    curses.wrapper(main)
