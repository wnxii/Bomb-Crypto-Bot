from cv2 import cv2
from os import listdir
import yaml
import src.logger as logger
import numpy
import mss
import pyautogui
import time

logger.log("Bomb Crypto Bot v1.1 by wenxi#9300", "log", "white")

# Load config and images
logger.log("Initializing config...", "debug")
stream = open("config.yaml", 'r')
cfg = yaml.safe_load(stream)

pause = cfg['mouse']['interval_between_movements']

pyautogui.PAUSE = pause

hero_sent_to_work = 0
prompt_popup = 0
unknown_check = 0

current_screen = "default"

last_action = {
    "send_hero_to_work": 0,
    "refresh_hero_position": 0,
    "screenshot_chest_interval": 0
}


def move_and_click(x, y, duration=cfg['mouse']['movement_duration']):
    pyautogui.moveTo(x, y, duration)
    pyautogui.click()


def print_screen():
    with mss.mss() as sct:
        sct_img = numpy.array(sct.grab(sct.monitors[1]))

        return sct_img[:,:,:3]


def snapshot_area(x, y, w, h, file_path="images/", file_name=logger.date_formatted("%d_%m_%Y_%I_%M_%S%p.png")):

    with mss.mss() as sct:

        monitor = {"top": y, "left": x, "width": w, "height": h, "mon": 1}
        output = file_path + file_name

        # Grab the data
        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        logger.log("Saved screenshot of x: " + str(x) + " y: " + str(y) + " width: " + str(w) + " height: " + str(h) + " to " + output, "debug")
        return output


# Unsure how this really works
def positions(img, threshold=cfg['threshold']['default_tolerance'], screen_img=None):

    if screen_img is None:
        screen_img = print_screen()

    result = cv2.matchTemplate(screen_img, img, cv2.TM_CCOEFF_NORMED)
    target_image_width = img.shape[1]
    target_image_height = img.shape[0]

    yloc, xloc = numpy.where(result >= threshold)

    rectangles = []

    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(target_image_width), int(target_image_height)])
        rectangles.append([int(x), int(y), int(target_image_width), int(target_image_height)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def is_same_row(bar, buttons):
    y_position = bar[1]

    for (x,y,w,h) in buttons:
        if y_position >= y and y_position <= y + h:
            return True, (x,y,w,h)

    return False, (x,y,w,h)


def set_hero_to_work():

    bars = positions(images['green-bar'], threshold=cfg['threshold']['stamina_bar_tolerance'])
    buttons = positions(images['go-work'], threshold=cfg['threshold']['stamina_bar_tolerance'])

    logger.log("Detected " + str(len(bars)) + " stamina bars", "debug")
    logger.log("Detected " + str(len(buttons)) + " non-working buttons", "debug")

    if len(buttons) == 0:
        return 0

    not_working_workable_heroes = []
    for bar in bars:
        row = is_same_row(bar, buttons)

        if row[0]:
            not_working_workable_heroes.append(row[1])

    if len(not_working_workable_heroes) > 0:
        logger.log("Setting " + str(len(not_working_workable_heroes)) + " to work", "debug")

    for (x, y, w, h) in not_working_workable_heroes:
        image_center_x_pos = x + w / 2
        image_center_y_pos = y + h / 2
        move_and_click(image_center_x_pos, image_center_y_pos)
        global hero_sent_to_work
        hero_sent_to_work = hero_sent_to_work + 1

    return len(not_working_workable_heroes)


def find_image(img_name, timeout=0, threshold=cfg['threshold']['default_tolerance']):

    logger.log("Attempting to find image: " + img_name, "debug")
    timeout_time = time.time() + timeout

    while True:

        image_matches = positions(images[img_name], threshold)

        if len(image_matches) == 0:
            if time.time() >= timeout_time:
                logger.log("Failed to find image: " + img_name + " timed out after " + str(round(time.time() - timeout_time + timeout, 2)) + "s", "debug", "red")
                return False, None, None, None, None

            continue

        logger.log("Found image: " + img_name, "debug", "green")
        x, y, w, h = image_matches[0]
        return True, x, y, w, h


def click_image(img_name, timeout=0, threshold=cfg['threshold']['default_tolerance'], duration=cfg['mouse']['movement_duration']):

    found, x, y, w, h = find_image(img_name, timeout, threshold)

    if not found:
        return False

    image_center_x_pos = x + w / 2
    image_center_y_pos = y + h / 2

    logger.log("Moving mouse to x: " + str(image_center_x_pos) + " y: " + str(image_center_y_pos) + " to click with duration: " + str(duration) + "s", "debug")
    move_and_click(image_center_x_pos, image_center_y_pos, duration)
    return True


def load_images(path):

    file_names = listdir(path)
    targets = {}
    for file_name in file_names:
        targets[file_name.removesuffix('.png')] = cv2.imread(path + '/' + file_name)

    return targets


def scroll(strength=-cfg['scroll']['scroll_size']):
    click_image("hero_border", cfg['threshold']['avatar_bar_tolerance'])
    pyautogui.dragRel(0, strength, cfg['scroll']['drag_duration'], button='left')


def send_hero_to_work():
    global hero_sent_to_work
    logger.log("Checking for heroes to work", "log")
    click_image("btn-back")
    click_image("hero-icon", timeout=1)
    click_image("hero_border", timeout=1)

    if not find_image("character-label")[0]:
        return False

    hero_sent_to_work = 0
    empty_scroll_attempts = cfg['scroll']['scroll_attempt']

    while empty_scroll_attempts > 0:
        clicked_buttons = set_hero_to_work()

        if clicked_buttons == 0:
            empty_scroll_attempts = empty_scroll_attempts - 1
        scroll()

        time.sleep(cfg['scroll']['wait_for_scroll_finish'])

    logger.log("Total sent " + str(hero_sent_to_work) + " heroes to work", "success")

    click_image("btn-close")
    click_image("treasure-hunt-icon")

    return True


def refresh_heroes():
    logger.log("Refreshing heroes' position", "log")
    click_image("btn-back")
    click_image("treasure-hunt-icon", timeout=1)


def capture_prompt_image(prompt_type):
    box_start = find_image("box_start", cfg['threshold']['box_tolerance'])
    box_end = find_image("box_end", cfg['threshold']['box_tolerance'])

    if not box_start[0] or not box_end[0]:
        return

    x = box_start[1]
    y = box_start[2]

    offset_width = box_end[3] - 4
    offset_height = box_end[3] - 1
    width = box_end[1] - box_start[1] + offset_width
    height = box_end[2] - box_start[2] + offset_height

    logger.send_screenshot_webhook(snapshot_area(x, y, int(width), int(height), "images/" + prompt_type + "/"), prompt_type)


def capture_screen_and_send(capture_type):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        logger.send_screenshot_webhook(snapshot_area(monitor['left'], monitor['top'], monitor['width'], monitor['height'], "images/" + capture_type + "/"), capture_type)


def open_chest_and_capture():
    click_image("chest_event")
    time.sleep(2)
    capture_prompt_image("chest")
    click_image("btn-close")


def do_prompt():
    global prompt_popup

    capture_screen_and_send("error")

    if click_image("ok", timeout=0):
        logger.log("Abnormal popup detected", "warning")
        prompt_popup = prompt_popup + 1

    if prompt_popup >= cfg['threshold']['error_popup']:
        logger.log("Error pop-ups exceeded threshold", "warning")
        prompt_popup = 0
        pyautogui.hotkey('ctrl', 'f5')
        logger.log("Possible error, refreshing page to try again", "error")


def do_new_map():
    logger.log("Detected new map", "log")
    click_image("new-map")
    time.sleep(2)
    capture_screen_and_send("new_map")


def do_in_game():

    if time.time() - last_action["screenshot_chest_interval"] > cfg['log']['screenshot_chest_interval'] * 60:
        open_chest_and_capture()
        last_action["screenshot_chest_interval"] = time.time()

    if time.time() - last_action["send_hero_to_work"] > cfg['update']['send_hero_to_work'] * 60:
        if send_hero_to_work():
            last_action["send_hero_to_work"] = time.time()
            last_action["refresh_hero_position"] = time.time()

    if time.time() - last_action["refresh_hero_position"] > cfg['update']['refresh_hero_position'] * 60:
        refresh_heroes()
        last_action["refresh_hero_position"] = time.time()


def do_login():
    logger.log("Trying to connect wallet", "log")

    click_image("connect-wallet", timeout=0)

    click_image("metamask-connect", timeout=5)

    if click_image("select-wallet-2", timeout=15):
        logger.log("Signing into metamask and loading into game!", "success")


def do_mode_selection():
    logger.log("Detected in mode selection screen, returning to game", "log")
    click_image("treasure-hunt-icon")


def do_hero_selection():
    logger.log("Detected in character selection screen, returning to game", "log")
    click_image("btn-close")
    click_image("treasure-hunt-icon", timeout=1)


def do_chest():
    logger.log("Chest screen detected and opened, closing it", "log")
    click_image("btn-close")


def process_current_screen():
    global current_screen, unknown_check
    logger.log("Detecting current screen", "debug")

    current_screen = "unknown"

    if find_image("ok", 0)[0]:
        current_screen = "pop-up"
        do_prompt()
    elif find_image("new-map", 0)[0]:
        current_screen = "new-map"
        do_new_map()
    elif find_image("btn-back", 0)[0]:
        current_screen = "in-game"
        do_in_game()
    elif find_image("connect-wallet", 0)[0]:
        current_screen = "login"
        do_login()
    elif find_image("loading-screen", 0)[0]:
        current_screen = "loading"
    elif find_image("treasure-hunt-icon", 0)[0]:
        current_screen = "mode-selection"
        do_mode_selection()
    elif find_image("character-label", 0)[0]:
        current_screen = "hero-selection"
        do_hero_selection()
    elif find_image("your-chest-label", 0)[0]:
        current_screen = "chest"
        do_chest()

    if current_screen == "unknown":
        unknown_check = unknown_check + 1
    else:
        unknown_check = 0

    logger.log("Current Screen: " + current_screen.upper())

    if unknown_check >= cfg['threshold']['failsafe_threshold']:
        unknown_check = 0
        pyautogui.hotkey('ctrl', 'f5')
        logger.log("Refreshing page to try again", "error")

logger.log("Initializing target images...", "debug")
images = load_images("targets")

logger.log("Initialization complete!", "debug")

while True:
    process_current_screen()
    time.sleep(cfg['update']['poll_rate']);