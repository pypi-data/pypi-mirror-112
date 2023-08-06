from datetime import datetime
from typing import List

import typer
from terminaltables import AsciiTable

from openapi_client import (
    ModelEnvVars,
    ModelKernelResourceSpecField,
    ModelParameter,
    ModelRange,
    ModelSweepObjective,
    ModelSweepSearchSpace,
    ProtoVolumeMountRequest,
    ProtoVolumeMountRequestSourceCLIDrivenProject,
    ProtoVolumeMountRequestSourceProject,
    ProtoVolumeMountRequestSourceVersionControlProject,
    ProtoVolumeMountRequests,
)
from savvihub.cli.constants import WEB_HOST, PROJECT_TYPE_VERSION_CONTROL, PROJECT_TYPE_CLI_DRIVEN
from savvihub.cli.exceptions import ExitException
from savvihub.cli.formatter import TreeFormatter
from savvihub.cli.inputs.common import (
    cluster_name_callback,
    env_vars_callback,
    image_url_callback,
    start_command_callback,
)
from savvihub.cli.inputs.git import (
    git_branch_callback,
    git_diff_callback,
    git_ref_callback,
)
from savvihub.cli.inputs.organization import organization_name_option
from savvihub.cli.inputs.project import project_name_option
from savvihub.cli.inputs.resource import (
    cpu_limit_callback,
    gpu_limit_callback,
    gpu_type_callback,
    memory_limit_callback,
    processor_type_callback,
    resource_name_callback,
)
from savvihub.cli.inputs.sweep import sweep_config_file_callback
from savvihub.cli.inputs.volume import dataset_mount_callback, volume_file_mount_callback
from savvihub.cli.typer import Context, Typer
from savvihub.common.utils import parse_time_to_ago

sweep_app = Typer()


@sweep_app.callback()
def main():
    """
    Run a hyperparameter optimization with sweep
    """


@sweep_app.command(user_required=True)
def list(
    ctx: Context,
    organization_name: str = organization_name_option,
    project_name: str = project_name_option,
):
    """
    Display a list of sweeps
    """
    sweeps = ctx.authenticated_client.sweep_list(organization_name, project_name).results
    if not sweeps:
        raise ExitException(f'There is no sweep in `{project_name}` project.')

    table = AsciiTable([
        ['NAME', 'STATUS', 'STATUS_REASON', 'CREATED', 'CREATED_BY', 'EXPERIMENT_COUNT'],
        *[[s.name, s.status, s.status_reason, parse_time_to_ago(s.created_dt), s.created_by.display_name,
           f'{s.experiment_summary.total}/{s.max_experiment_count}']
          for s in sweeps],
    ])
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)


@sweep_app.command(user_required=True)
def describe(
    ctx: Context,
    organization_name: str = organization_name_option,
    project_name: str = project_name_option,
    sweep_name: str = typer.Argument(..., help="The unique sweep name"),
):
    """
    Describe the sweep in details
    """
    sweep = ctx.authenticated_client.sweep_read(organization_name, project_name, sweep_name)
    timezone = datetime.now().astimezone().tzinfo

    root = TreeFormatter()
    root.add_child(f'Name: {sweep.name}',
                   f'Description: {sweep.description}',
                   f'Created: {sweep.created_dt.astimezone(timezone)}',
                   f'Updated: {sweep.created_dt.astimezone(timezone)}',
                   f'Status: {sweep.status}',
                   f'Status updated: {sweep.status_last_updated.astimezone(timezone)}',
                   f'Status reason: {sweep.status_reason}',
                   f'Organization: {sweep.organization.name}',
                   f'Project: {sweep.project.name}')

    # Objective description
    objective_desc = TreeFormatter('Objective:')
    objective_desc.add_child(f'Type: {sweep.objective.type}',
                             f'Metric: {sweep.objective.metric}',
                             f'Goal: {sweep.objective.goal}')
    root.add_child(objective_desc)

    # Algorithm description
    root.add_child(f'Algorithm: {sweep.algorithm}')

    # Search Space
    if sweep.search_space.parameters:
        search_space_desc = TreeFormatter('Search space:')
        for param in sweep.search_space.parameters:
            search_space_desc.add_child(f'{param}')
        root.add_child(search_space_desc)

    # Experiment trials
    root.add_child(f'Max experiment count: {sweep.max_experiment_count}')
    root.add_child(f'Parallel experiment count: {sweep.parallel_experiment_count}')
    root.add_child(f'Max failed experiment count: {sweep.max_failed_experiment_count}')

    # Suggestion histories
    if sweep.suggestion_histories.histories:
        suggestion_desc = TreeFormatter('Suggestions:')
        for history in sweep.suggestion_histories.histories:
            params = []
            for param in history.parameters:
                params.append(f'{param.name}: {param.val}')
            suggestion_desc.add_child(f'{", ".join(params)}')
        root.add_child(suggestion_desc)

    typer.echo(root.format())


@sweep_app.command(user_required=True)
def create(
    ctx: Context,
    organization_name: str = organization_name_option,
    project_name: str = project_name_option,
    file: str = typer.Option(None, "--file", "-f", callback=sweep_config_file_callback, help="sweep config file"),
):
    """
    Create a sweep
    """
    sweep = ctx.authenticated_client.sweep_create(
        organization=organization_name,
        project=project_name,
        objective=ModelSweepObjective(
            type=ctx.store['objective']['type'],
            goal=str(ctx.store['objective']['goal']),
            metric=str(ctx.store['objective']['metric']),
        ),
        algorithm=ctx.store['algorithm'],
        search_space=ModelSweepSearchSpace(
            parameters=[ModelParameter(
                name=p['name'],
                range=ModelRange(
                    max=p['range']['max'],
                    min=p['range']['min'],
                    step=p['range']['step'],
                    list=[str(elem) for elem in p['range']['list']],
                ),
                type=p['type'],
            ) for p in ctx.store['search_space']]
        ),
        parallel_experiment_count=ctx.store['parallel_experiment_count'],
        max_experiment_count=ctx.store['max_experiment_count'],
        max_failed_experiment_count=ctx.store['max_failed_experiment_count'],
    )

    typer.echo(
        f'Sweep {sweep.name} is created. Check the sweep status at below link\n'
        f'{WEB_HOST}/{organization_name}/{project_name}/sweeps/{sweep.name}'
    )


@sweep_app.command(user_required=True)
def run(
    ctx: Context,
    organization_name: str = organization_name_option,
    project_name: str = project_name_option,
    sweep_name: str = typer.Argument(..., help="The unique sweep name"),
    start_command: str = typer.Option(None, "--start-command", callback=start_command_callback, help="Start command"),
    cluster_name: str = typer.Option(None, "--cluster", "-c", callback=cluster_name_callback, help="Cluster name"),
    resource_name: str = typer.Option(None, "--resource", "-r", callback=resource_name_callback,
                                      help="Resource name (for savvihub-managed cluster)"),
    processor_type: str = typer.Option(None, "--processor-type", callback=processor_type_callback,
                                       help="cpu or gpu (for custom cluster)"),
    cpu_limit: float = typer.Option(0, "--cpu-limit", callback=cpu_limit_callback,
                                    help="Number of vCPUs (for custom cluster)"),
    memory_limit: str = typer.Option(None, "--memory-limit", callback=memory_limit_callback,
                                     help="Memory capacity (ex: 4Gi, 500Mi)"),
    gpu_type: str = typer.Option(None, "--gpu-type", callback=gpu_type_callback,
                                 help="GPU product name such as Tesla-K80 (for custom cluster)"),
    gpu_limit: int = typer.Option(0, "--gpu-limit", callback=gpu_limit_callback,
                                  help="Number of GPU cores (for custom cluster)"),
    image_url: str = typer.Option(None, "--image", "-i", callback=image_url_callback, help="Kernel docker image URL"),
    dataset_mounts: List[str] = typer.Option([], "--dataset", "-d", callback=dataset_mount_callback,
                                             help="Dataset mounted path"),
    volume_file_mounts: List[str] = typer.Option([], "--volume-file", callback=volume_file_mount_callback, hidden=True),
    ignore_git_diff: bool = typer.Option(False, "--ignore-git-diff", help="Ignore git diff flag"),
    git_branch: str = typer.Option(None, "--git-branch", callback=git_branch_callback, help="Git branch name"),
    git_ref: str = typer.Option(None, "--git-ref", callback=git_ref_callback, help="Git commit SHA"),
    git_diff_arg: str = typer.Option(None, "--git-diff", callback=git_diff_callback, help="Git diff file URL"),
    env_vars: List[str] = typer.Option([], "-e", callback=env_vars_callback, help="Environment variables"),
    output_dir: str = typer.Option("/output/", "--output-dir",
                                   help="A directory to which the experiment result output files to be stored."),
    working_dir: str = typer.Option(None, "--working-dir", help="If not present, use `/work/{project_name}`."),
    root_volume_size: str = typer.Option(None, "--root-volume-size", help="Root volume size"),
):
    """
    Run the sweep
    """
    resource_spec = resource_spec_id = None
    if ctx.store['cluster'].is_savvihub_managed:
        resource_spec_id = ctx.store['resource_spec_id']
    else:
        resource_spec = ModelKernelResourceSpecField(
            processor_type=processor_type,
            cpu_type='Any',
            cpu_limit=cpu_limit,
            memory_limit=memory_limit,
            gpu_type=gpu_type,
            gpu_limit=gpu_limit,
        )

    project_volume_mount = ProtoVolumeMountRequestSourceProject(
        project_id=ctx.project.id,
    )
    project_mount_path = "/work/"
    if ctx.project.type == PROJECT_TYPE_VERSION_CONTROL:
        project_volume_mount.project_type = PROJECT_TYPE_VERSION_CONTROL
        project_volume_mount.version_control_project = ProtoVolumeMountRequestSourceVersionControlProject(
            project_branch=git_branch,
            project_git_ref=git_ref,
            project_git_diff=ctx.store.get('git_diff_uploaded_path')
        )
        project_mount_path += f"{project_name}"
    elif ctx.project.type == PROJECT_TYPE_CLI_DRIVEN:
        project_volume_mount.project_type = PROJECT_TYPE_CLI_DRIVEN
        project_volume_mount.cli_driven_project = ProtoVolumeMountRequestSourceCLIDrivenProject(
            local_project=ctx.store.get('local_project_uploaded_path')
        )

    sweep = ctx.authenticated_client.sweep_run(
        organization=organization_name,
        project=project_name,
        sweep_name=sweep_name,
        image_url=image_url,
        resource_spec_id=resource_spec_id,
        resource_spec=resource_spec,
        cluster_name=cluster_name,
        volume_mounts=ProtoVolumeMountRequests(
            root_volume_size=root_volume_size,
            working_dir=working_dir,
            requests=ctx.store['dataset_mounts'] + ctx.store['volume_file_mounts'] + [
                ProtoVolumeMountRequest(
                    mount_type='empty-dir',
                    mount_path='/work/'
                ),
                ProtoVolumeMountRequest(
                    mount_type='output',
                    mount_path=output_dir,
                ),
                ProtoVolumeMountRequest(
                    mount_type='project',
                    mount_path=project_mount_path,
                    project=project_volume_mount,
                ),
            ],
        ),
        env_vars=ModelEnvVars(env_vars),
        start_command=start_command,
    )

    typer.echo(
        f'Sweep {sweep.name} is running. Check the experiment status at below link\n'
        f'{WEB_HOST}/{organization_name}/{project_name}/sweeps/{sweep.name}'
    )
