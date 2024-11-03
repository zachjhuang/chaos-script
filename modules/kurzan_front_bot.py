# pylint: disable=missing-module-docstring
import time

import pyautogui
import pydirectinput

import modules.dungeon_bot as db
import modules.utilities as util
from modules.menu_nav import quit_chaos, restart_check, toggle_menu, wait_for_menu_load
from modules.minimap import Minimap

SCREEN_CENTER_X = 960
SCREEN_CENTER_Y = 540

SCREEN_CENTER_POS = (960, 540)
SCREEN_CENTER_REGION = (685, 280, 600, 420)

CHAOS_CLICKABLE_REGION = (460, 290, 1000, 500)
CHAOS_LEAVE_MENU_REGION = (0, 154, 250, 300)

ABIDOS_ICON_POS = {
    1640: (830, 670),
    1660: (965, 590)
}


class KurzanFrontBot(db.DungeonBot):
    """
    DungeonBot child class for completing Kurzan Front.
    """

    def __init__(self, roster):
        super().__init__(roster)
        self.remaining_tasks: list[int] = [
            (
                1
                if char["chaosItemLevel"] is not None and char["chaosItemLevel"] >= 1640
                else 0
            )
            for char in self.roster
        ]
        self.minimap = Minimap()

    def do_tasks(self) -> None:
        if self.done_on_curr_char():
            return

        toggle_menu("defaultCombatPreset")

        enter_kurzan_front(self.roster[self.curr]["chaosItemLevel"])
        db.wait_dungeon_load()
        self.run_start_time = int(time.time())
        print("kurzan front loaded")

        if util.get_config("auraRepair"):
            db.do_aura_repair(False)

        util.left_click_at_position(SCREEN_CENTER_POS)
        util.random_sleep(1500, 1600)

        self.use_skills()
        end_time = int(time.time())
        self.update_print_metrics(end_time - self.run_start_time)
        self.remaining_tasks[self.curr] = 0
        quit_chaos()

    def use_skills(self) -> None:
        """
        Moves character and uses skills. Behavior changes depending on the floor.
        """
        self.minimap = Minimap()
        curr_class = self.roster[self.curr]["class"]
        char_skills = self.skills[curr_class]
        normal_skills = [
            skill for skill in char_skills if skill["skillType"] == "normal"
        ]
        awakening_skill = [
            skill for skill in char_skills if skill["skillType"] == "awakening"
        ][0]
        # awakeningUsed = False
        jumped = False
        x, y, magnitude = self.minimap.get_game_coords()
        while True:
            self.died_check()
            self.health_check()
            restart_check()
            self.timeout_check()
            timeout = 0
            # cast sequence
            for i, skill in enumerate(normal_skills):
                if check_kurzan_finish():
                    print("KurzanFront finish screen")
                    return
                self.died_check()
                self.health_check()
                if not jumped and check_50_percent_progress() and self.minimap.check_jump():
                    timeout = 0
                    while True:
                        if (
                            util.find_image_center(
                                "./screenshots/jumpArrow.png", confidence=0.75
                            )
                            is not None
                        ):
                            print("arrow found")
                            util.find_and_click_image("jumpArrow", confidence=0.75)
                            util.random_sleep(1000, 1100)

                        if util.check_image_on_screen(
                            "./screenshots/chaos/jump.png",
                            confidence=0.75,
                        ):
                            util.left_click_at_position(SCREEN_CENTER_POS)
                            break
                        x, y, magnitude = self.minimap.get_game_coords(
                            target_found=self.minimap.check_jump(), pathfind=True
                        )
                        db.move_in_direction(x, y, magnitude)
                        util.random_sleep(100, 150)
                        util.left_click_at_position(SCREEN_CENTER_POS)
                        timeout += 1
                        if timeout == 10:
                            db.random_move()
                            util.random_sleep(400, 500)
                            timeout = 0

                    pydirectinput.press("g")
                    util.random_sleep(300, 350)
                    pydirectinput.press("g")
                    print("jumped")
                    jumped = True
                    self.minimap.targets = []

                elif (
                    self.minimap.check_buff()
                    or self.minimap.check_boss()
                    or self.minimap.check_elite()
                ):
                    x, y, magnitude = self.minimap.get_game_coords(
                        target_found=True, pathfind=True
                    )
                    db.move_in_direction(x, y, magnitude)
                    if util.check_image_on_screen(
                        "./screenshots/chaos/bossBar.png", confidence=0.75
                    ):
                        db.cast_skill(awakening_skill)
                elif timeout == 5:
                    db.random_move()
                    timeout = 0
                else:
                    print("target not found")
                    x, y, magnitude = self.minimap.get_game_coords(
                        target_found=False, pathfind=True
                    )
                    db.move_in_direction(x, y, magnitude)
                    timeout += 1
                db.perform_class_specialty(
                    self.roster[self.curr]["class"], i, normal_skills
                )
                db.cast_skill(skill)


def check_50_percent_progress() -> bool:
    """
    Check if the progress meter in the top left is approximately 50% completed.

    Used to check when to perform a jump.

    Returns:
        bool: True if progress is around 50%, False otherwise.
    """
    im = pyautogui.screenshot()
    r, _g, _b = im.getpixel((89, 292))
    return r > 130


def enter_kurzan_front(ilvl: int) -> None:
    """
    Enters specified Kurzan Front level.
    """
    toggle_menu("content")
    wait_for_menu_load("kazerosWarMap")
    util.random_sleep(1200, 1300)
    util.left_click_at_position(ABIDOS_ICON_POS[ilvl])
    wait_for_menu_load("kurzanFront")
    util.random_sleep(1200, 1300)
    util.find_and_click_image("enterButton", region=(
        1300, 750, 210, 40), confidence=0.75)
    util.random_sleep(1200, 1300)
    util.find_and_click_image(
        "acceptButton", region=SCREEN_CENTER_REGION, confidence=0.75)
    util.random_sleep(800, 900)


def check_kurzan_finish() -> bool:
    """
    Returns true if chaos finish screen detected and clears the finish overlay. 
    Otherwise returns false.
    """
    match util.find_image_center(
        "./screenshots/chaos/kurzanFrontClearOK.png",
        confidence=0.65,
        region=(880, 820, 150, 70),
    ):
        case x, y:
            util.left_click_at_position((x, y))
            util.random_sleep(800, 900)
            return True
        case _:
            return False
