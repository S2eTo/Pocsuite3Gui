import os

from pocsuite3 import cli
from pocsuite3.api import logger
from pocsuite3.lib.core.common import get_local_ip
from pocsuite3.lib.core.enums import CUSTOM_LOGGING

self_path = os.path.dirname(__file__)
cli_path = os.path.dirname(cli.__file__)

BASE_DIR = None
if self_path.startswith(cli_path):
    BASE_DIR = cli_path
else:
    BASE_DIR = self_path.rsplit(os.path.sep, 1)[0]

POC_DIR = os.path.join(BASE_DIR, "pocs")
last_ip = [item for item in get_local_ip(all=True)]


def get_file_path(name):
    found = os.path.join(POC_DIR, name + ".py")
    if not os.path.exists(found):
        found = os.path.join(POC_DIR, name + ".yaml")

    return found


def get_options(options):
    lists = []

    for opt_name, opt in options:
        item = {
            "name": opt_name,
            "value": opt.value,
            "type": opt.type,
            "require": opt.require,
            "description": opt.description,
        }

        if opt.type == "Dict":
            item["default"] = opt.default

        lists.append(item)

    return lists


def get_info(module, append={}, is_get_options=False):
    options = []

    if is_get_options:
        options.extend(get_options(module.global_options.items()))
        options.extend(get_options(module.options.items()))
        options.extend(get_options(module.payload_options.items()))

    return {**{
        "name": module.name,
        "vulID": module.vulID,
        "author": module.author,
        "vulDate": module.vulDate,
        "options": options,
        "references": module.references,
        "desc": module.desc,
        "vulType": module.vulType,
        "appVersion": module.appVersion
    }, **append}


def command_set(module, *args, **kwargs):
    key, _, value = args[0].partition(" ")
    if key in module.options:
        module.set_option(key, value)
        logger.info("{} => {}".format(key, value))
    elif key in module.global_options:
        module.setg_option(key, value)
        logger.info("{} => {}".format(key, value))
    elif key in module.payload_options:
        if value.isdigit() and key != "lport":
            iindex = int(value)
            if iindex >= len(last_ip):
                logger.warning("Index out of range")
                return
            value = last_ip[iindex]
        module.setp_option(key, value)
        logger.info("{} => {}".format(key, value))
    else:
        logger.error("You can't set option '{}'.".format(key))


def check_requirement(*args):
    for option in args:
        for k, v in option.items():
            if v.require and v.value == "":
                logger.log(CUSTOM_LOGGING.ERROR, "参数 '{key}' 必须设置, 不能为空！'".format(key=k))
                return False
    return True


def set_options(module, options):
    for option in options:
        n, v = option.split(" ", 1)

        # 为空不设置
        if v == '':
            continue

        if n == "content_type" and v == "null":
            continue

        # 没变化不设置
        if n in module.options:
            if str(module.get_option(n)) == str(v):
                continue
        elif n in module.global_options:
            if str(module.getg_option(n)) == str(v):
                continue
        elif n in module.payload_options:
            if str(module.payload_options.get(n).value) == str(v):
                continue

        command_set(module, option)
