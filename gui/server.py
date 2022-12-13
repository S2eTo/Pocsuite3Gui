import os
import json
import traceback
from prettytable import PrettyTable

from flask import request

from pocsuite3.lib.core.data import kb
from pocsuite3.api import POCBase, logger
from pocsuite3.lib.core.poc import Output
from pocsuite3.lib.core.option import init
from pocsuite3.lib.core.common import set_paths
from pocsuite3.lib.core.datatype import AttribDict
from pocsuite3.lib.core.option import init_options
from pocsuite3.lib.parse.cmd import cmd_line_parser
from pocsuite3.lib.core.common import index_modules
from pocsuite3.lib.core.register import load_file_to_module

from pocsuite3.gui.main import app, socketio
from pocsuite3.gui.log.filter import ExecuteFilter
from pocsuite3.gui.log.hooks.websocket import WebSocketHook
from pocsuite3.gui.common import POC_DIR, get_file_path, get_info, set_options, check_requirement

first = True


@app.route("/")
def index():
    return "123"


@socketio.on('connect', namespace='/ws')
def test_connect():
    global first

    if first:
        first = False
        socketio.emit('message', {'action': 'clear_logger'}, namespace='/ws')
        logger.info("控制台连接正常.")


@app.route('/run', methods=['POST', 'GET'])
def run():
    try:
        data = json.loads(request.get_data().decode())
        poc = data['poc']
        mode = data['mode']

        socketio.emit('message', {'action': 'logger', 'data': {
            "levelname": -1,
            "levelno": -1,
            "msg": f">>> python cli.py -r {poc} --{mode}"
        }}, namespace='/ws')

        module: POCBase = kb.registered_pocs.get(f"pocs_{poc}")
        if module is None:
            logger.info(f"Not found {poc} mode")
            return "False"

        set_options(module, data['options'])

        if not check_requirement(module.global_options, module.options):
            return "False"

        logger.info("running poc:'{0}' target '{1}'".format(module.name, module.global_options.get("target").value))

        output = None
        module.target = module.getg_option("target")
        module.url = module.build_url()
        try:
            if mode == "verify":
                output = getattr(module, "_verify")()
            elif mode == "attack":
                output = getattr(module, "_attack")()
            elif mode == "shell":
                output = getattr(module, "_shell")()
        except Exception as e:
            socketio.emit('message', {'action': 'logger', 'data': {
                "levelname": -2,
                "levelno": -2,
                "msg": traceback.format_exc()
            }}, namespace='/ws')

            traceback.print_exc()
            return "False"

        logger.info("Scan completed,ready to print")
        module.target = module.global_options.get("target")

        if output is None:
            output = Output(module)
            output.fail('target is not vulnerable')

        result_status = "success" if output.is_success() else "failed"

        output.show_result()
        output = output.to_dict()
        output["target"] = module.getg_option("target")
        output = AttribDict(output)

        if output:
            output.params = module.params

        results_table = PrettyTable(["target-url", "poc-name", "poc-id", "component", "version", "status"],
                                    encoding="UTF-8")
        results_table.align["target-url"] = "l"
        results_table.padding_width = 2
        results_table.add_row([
            output.target.strip(),
            output.poc_attrs.get("name"),
            output.poc_attrs.get("vulID"),
            output.poc_attrs.get("appName"),
            output.poc_attrs.get("appVersion"),
            result_status
        ])

        results_table_string = results_table.get_string(sortby="status", reversesort=True)
        print(results_table_string)
        socketio.emit('message', {'action': 'logger', 'data': {
            "levelname": -3,
            "levelno": -3,
            "msg": results_table_string
        }}, namespace='/ws')

        return "ok"
    except SystemExit:
        return "False"


@app.route('/poc_detailed')
def poc_detailed():
    poc = request.args.get("poc")

    if not kb.registered_pocs.get(f"pocs_{poc}"):
        load_file_to_module(get_file_path(poc))

    module: POCBase = kb.registered_pocs.get(f"pocs_{poc}")

    return get_info(module, is_get_options=True)


@app.route('/poc_list')
def poc_list():
    module_list = []

    for module in kb.registered_pocs:
        item = kb.registered_pocs[module]
        module_list.append(get_info(item, append={"path": module.replace("pocs_", "").strip()}))

    return module_list


def module_path():
    from pocsuite3 import cli
    return os.path.dirname(os.path.realpath(cli.__file__))


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "your system does not properly handle non-ASCII paths. "
        err_msg += "Please move the pocsuite's directory to the other location"
        logger.critical(err_msg)
        raise SystemExit


def load_modules():
    modules = index_modules(POC_DIR)
    for tmp_module in modules:
        found = get_file_path(tmp_module)
        load_file_to_module(found)


if __name__ == "__main__":
    logger_filter = ExecuteFilter()
    logger_filter.add_hook(WebSocketHook())

    logger.addFilter(logger_filter)

    check_environment()
    set_paths(module_path())

    init_options(cmd_line_parser().__dict__)

    init()

    load_modules()

    socketio.run(app, debug=True, host='127.0.0.1', port=8888)
