from datetime import datetime
import yaml
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

stream = open("config.yaml", 'r')
cfg = yaml.safe_load(stream)

log_webhook = DiscordWebhook(url=cfg['log']['discord_log_webhook'])
error_webhook = DiscordWebhook(url=cfg['log']['discord_error_webhook'], username="BCrypto Error", content="<@"+cfg['log']['discord_user_id']+">")
new_map_webhook = DiscordWebhook(url=cfg['log']['discord_new_map_webhook'], username="BCrypto New Map", content="<@"+cfg['log']['discord_user_id']+">")
chest_webhook = DiscordWebhook(url=cfg['log']['discord_chest_webhook'], username="BCrypto Chest", content="<@"+cfg['log']['discord_user_id']+">")

previous_log = None

SCREENSHOT_TYPE = {
    'ERROR': error_webhook,
    'NEW_MAP': new_map_webhook,
    'CHEST': chest_webhook
}

MESSAGE_TYPE = {
    'LOG': 'white',
    'ERROR': 'red',
    'SUCCESS': 'green',
    'WARNING': 'yellow',
    'DEBUG': 'grey'
}

DISCORD_EMBED_COLOR = {
    'LOG': 'ecf0f1',
    'ERROR': 'c0392b',
    'SUCCESS': '2ecc71',
    'WARNING': 'f1c40f',
    'DEBUG': 'bdc3c7'
}

COLOR = {
    'default': '\033[99m',
    'blue': '\033[94m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def date_formatted(format = "%d/%m/%Y %I:%M:%S%p"):
    return datetime.now().strftime(format)


def color_message(message, color="default"):
    return COLOR[color] + message + "\033[0m"


def send_screenshot_webhook(img_path, screenshot_type):

    if not cfg['log']['send_screenshot_to_discord']:
        return

    with open(img_path, "rb") as f:
        SCREENSHOT_TYPE[screenshot_type.upper()].add_file(file=f.read(), filename="image.png")

    response = SCREENSHOT_TYPE[screenshot_type.upper()].execute()


def log_to_local(message):

    if cfg['log']['save_log_to_file']:
        logger_file = open("logs.log", "a", encoding='utf-8')
        logger_file.write(message + '\n')
        logger_file.close()


def log_to_webhook(message, message_type):
    global previous_log

    if cfg['log']['save_log_to_discord'] and not cfg['log']['discord_log_webhook'] is None and message_type != "debug" and message != previous_log:
        embed = DiscordEmbed(title=message_type.upper(), description=message,
                            color=DISCORD_EMBED_COLOR[message_type.upper()])
        embed.set_author(name='Bomb Crypto Bot',
                        icon_url='https://scontent.fsin4-1.fna.fbcdn.net/v/t39.30808-6/269824394_138582198559813_7944985002468577710_n.jpg?_nc_cat=1&ccb=1-5&_nc_sid=973b4a&_nc_ohc=IBZk1OLcSzkAX8FGnP1&_nc_ht=scontent.fsin4-1.fna&oh=00_AT9yYvIlmxEtTnhAATbmAq-MGCPaByHGaTBXZvCUXUbFog&oe=61CB6AA8')
        embed.set_timestamp()
        log_webhook.add_embed(embed)
        response = log_webhook.execute(remove_embeds=True)

    if message_type != "debug":
        previous_log = message


def log(message, message_type="log", color="default"):

    if cfg['log']['log_level'] == "standard" and message_type == "debug":
        return

    formatted_raw_message = "[{}] [{}]: {}".format(date_formatted(),
                                               message_type.upper(),
                                               message)

    formatted_color_message = "[{}] [{}]: {}".format(color_message(date_formatted(), "grey"),
                                               color_message(message_type.upper(), MESSAGE_TYPE[message_type.upper()]),
                                               color_message(message, color))

    print(formatted_color_message)

    log_to_webhook(message, message_type)
    log_to_local(formatted_raw_message)
