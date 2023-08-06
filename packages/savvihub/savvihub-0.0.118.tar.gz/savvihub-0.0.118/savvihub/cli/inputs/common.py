from typing import List

import inquirer
import typer

from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context
from savvihub.cli.utils import find_from_inquirer


def image_url_callback(ctx: Context, image_url: str) -> str:
    assert ctx.params['organization_name'] and ctx.params['processor_type']

    images = ctx.authenticated_client.kernel_image_list(ctx.params['organization_name']).results
    images = [i for i in images if i.processor_type == ctx.params['processor_type']]
    if image_url:
        for image in images:
            if image.image_url == image_url:
                return image_url
        else:
            raise ExitException(f'Image not found: {image_url}')

    return find_from_inquirer(
        images,
        lambda x: f'{x.image_url} ({x.name})',
        "Please choose a kernel image"
    ).image_url

def env_vars_callback(ctx: Context, env_vars: List[str]) -> List[str]:
    ctx.store['env_vars'] = []
    for env_var in env_vars:
        try:
            env_key, env_value = env_var.split("=", 1)
            ctx.store['env_vars'].append({
                'key': env_key,
                'value': env_value,
            })
        except ValueError:
            raise ExitException(f'Cannot parse environment variable: {env_var}')

    return env_vars


def cluster_name_callback(ctx: Context, cluster_name: str) -> str:
    assert ctx.params['organization_name']

    clusters = [c for c in ctx.authenticated_client.cluster_list(ctx.params['organization_name']).clusters
                if c.status == 'connected']
    if cluster_name:
        for cluster in clusters:
            if cluster.name == cluster_name.strip():
                ctx.store['cluster'] = cluster
                return cluster.name
        else:
            raise ExitException(f'Cluster not found: {cluster_name.strip()}')

    elif len(clusters) == 1:
        typer.echo(f'The cluster is automatically set to `{clusters[0].name}{" (SavviHub)" if clusters[0].is_savvihub_managed else f" (Custom)"}`.')
        ctx.store['cluster'] = clusters[0]
        return clusters[0].name

    else:
        selected_cluster = find_from_inquirer(
            clusters,
            lambda x: f'{x.name}{" (SavviHub)" if x.is_savvihub_managed else f" ({x.name})"}',
            "Please choose a cluster"
        )
        ctx.store['cluster'] = selected_cluster

    return selected_cluster.name

def start_command_callback(start_command: str) -> str:
    if start_command:
        return start_command

    return inquirer.prompt([inquirer.Text(
        'start_command',
        message="Start command",
        default="python main.py",
    )], raise_keyboard_interrupt=True).get('start_command')
