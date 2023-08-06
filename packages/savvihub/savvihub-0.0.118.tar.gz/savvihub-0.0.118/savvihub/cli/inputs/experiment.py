import os
from typing import Optional

import inquirer
import typer

from savvihub.api.exceptions import NotFoundAPIException
from savvihub.api.uploader import Uploader
from savvihub.api.zipper import Zipper
from savvihub.cli.commands.volume import parse_remote_volume_path
from savvihub.cli.constants import PROJECT_TYPE_CLI_DRIVEN, PROJECT_TYPE_VERSION_CONTROL
from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context


def message_callback(ctx: Context, message: str) -> str:
    if message:
        return message

    inquirer_message = ""
    if ctx.project.type == PROJECT_TYPE_VERSION_CONTROL:
        inquirer_message = "Experiment message(set to commit message if you passed empty)"
    elif ctx.project.type == PROJECT_TYPE_CLI_DRIVEN:
        inquirer_message = "Experiment message"

    return inquirer.prompt([inquirer.Text(
        'message',
        message=inquirer_message,
        default=""
    )], raise_keyboard_interrupt=True).get('message')

