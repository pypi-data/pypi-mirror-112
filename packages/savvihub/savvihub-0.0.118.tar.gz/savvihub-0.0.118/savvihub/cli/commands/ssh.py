import os
import urllib.parse
from pathlib import Path

import inquirer
import paramiko
import typer

from savvihub.cli.commands.ssh_keys import ssh_keys_app
from savvihub.cli.exceptions import ExitException
from savvihub.cli.inputs.organization import organization_name_option
from savvihub.cli.inputs.ssh import ssh_private_key_path_callback
from savvihub.cli.typer import Typer, Context
from savvihub.common.utils import parse_time_to_ago

ssh_app = Typer()
ssh_app.add_typer(ssh_keys_app, name='keys')


@ssh_app.callback()
def main():
    """
    Manage ssh keys and connect to workspaces
    """


@ssh_app.command(user_required=True)
def connect(
    ctx: Context,
    organization_name: str = organization_name_option,
    ssh_private_key_path: str = typer.Option(None, '--key-path', callback=ssh_private_key_path_callback, help='SSH private key path.'),
):
    """
    Connect to a running workspace.
    """
    workspace_list_response = ctx.authenticated_client.workspace_list(organization_name, 'running')
    running_workspaces = workspace_list_response.results
    if len(running_workspaces) == 0:
        raise ExitException('There is no running workspace.')

    if len(running_workspaces) == 1:
        workspace = running_workspaces[0]
    else:
        workspace = inquirer.prompt([inquirer.List(
            'question',
            message='Select workspace',
            choices=[(f'{w.name} (created {parse_time_to_ago(w.created_dt)})', w) for w in running_workspaces],
        )], raise_keyboard_interrupt=True).get('question')

    ssh_endpoint = urllib.parse.urlparse(workspace.endpoints.ssh.endpoint)
    ssh_private_key_option = f' -i {ssh_private_key_path}' if ssh_private_key_path else ''
    os.system(f'ssh -p {ssh_endpoint.port}{ssh_private_key_option} {ctx.user.username}@{ssh_endpoint.hostname}')


@ssh_app.command(user_required=True)
def vscode(
    ctx: Context,
    organization_name: str = organization_name_option,
    ssh_private_key_path: str = typer.Option(None, '--key-path', callback=ssh_private_key_path_callback,
                                             help='SSH private key path.'),
):
    """
    Update .ssh/config file for VSCode Remote-SSH plugin
    """
    workspace_list_response = ctx.authenticated_client.workspace_list(organization_name, 'running')
    running_workspaces = workspace_list_response.results
    if len(running_workspaces) == 0:
        raise ExitException('There is no running workspace.')

    ssh_config = paramiko.SSHConfig()
    ssh_config.parse(open(f'{Path.home()}/.ssh/config'))
    hostname_set = ssh_config.get_hostnames()

    for workspace in running_workspaces:
        hostname = f'{workspace.name}-{int(workspace.created_dt.timestamp())}'
        if hostname in hostname_set:
            continue

        ssh_endpoint = urllib.parse.urlparse(workspace.endpoints.ssh.endpoint)
        config_value = f'''
Host {hostname}
    User {ctx.user.username}
    Hostname {ssh_endpoint.hostname}
    Port {ssh_endpoint.port}
    StrictHostKeyChecking accept-new
    CheckHostIP no
'''
        if ssh_private_key_path:
            config_value += f'    IdentityFile {ssh_private_key_path}\n'

        with open(f'{Path.home()}/.ssh/config', 'a') as f:
            f.write(config_value)

    typer.echo(f'Successfully updated {Path.home()}/.ssh/config')
