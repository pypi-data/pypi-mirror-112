import os
from typing import Optional

import yaml

from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context


def sweep_config_file_callback(ctx: Context, filepath: str) -> Optional[str]:
    if not filepath:
        return

    if not os.path.isfile(filepath):
        raise ExitException(f'File does not exists: {filepath}')

    try:
        configs = yaml.safe_load(filepath)
    except yaml.YAMLError:
        raise ExitException(f'Invalid YAML: {filepath}')

    with open(filepath, 'r') as stream:
        configs = yaml.load(stream, Loader=yaml.FullLoader)

    ctx.store['objective'] = configs['objective']
    ctx.store['algorithm'] = configs['algorithm']
    ctx.store['search_space'] = configs['search_space']['parameters']
    ctx.store['parallel_experiment_count'] = configs['parallel_experiment_count']
    ctx.store['max_experiment_count'] = configs['max_experiment_count']
    ctx.store['max_failed_experiment_count'] = configs['max_failed_experiment_count']
    return
