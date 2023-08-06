from typing import List

from openapi_client import ProtoVolumeMountRequest, ProtoVolumeMountRequestSourceDataset, \
    ProtoVolumeMountRequestSourceVolume
from savvihub.api.exceptions import NotFoundAPIException
from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context
from savvihub.cli.utils import parse_dataset


def dataset_mount_callback(ctx: Context, dataset_mounts: List[str]) -> List[str]:
    client = ctx.authenticated_client
    organization_name = ctx.params['organization_name']
    ctx.store['dataset_mounts'] = []
    for dataset_mount in dataset_mounts:
        splitted = dataset_mount.split(':')
        if len(splitted) != 2:
            raise ExitException(f'Invalid dataset mount format: {dataset_mount}. '
                                f'You should specify both mount path and dataset name.\n'
                                f'ex) /input/dataset1:mnist@3d1e0f91c')

        mount_path, dataset_full_name = splitted
        organization_name_override, dataset_name, dataset_version_name = parse_dataset(dataset_full_name)
        if organization_name_override:
            organization_name = organization_name_override

        dataset = client.dataset_read(organization_name, dataset_name)
        if dataset_version_name != 'latest':
            try:
                client.dataset_version_read(dataset.volume_id, dataset_version_name)
            except NotFoundAPIException:
                raise ExitException(f'Invalid dataset dataset_version: {dataset_full_name}\n'
                                    f'Please check your dataset and dataset_version exist in organization `{organization_name}`.')

        ctx.store['dataset_mounts'].append(ProtoVolumeMountRequest(
            mount_type='dataset',
            mount_path=mount_path,
            dataset=ProtoVolumeMountRequestSourceDataset(
                dataset_id=dataset.id,
                dataset_version_name=dataset_version_name,
            ),
        ))

    return dataset_mounts


def volume_file_mount_callback(ctx: Context, volume_file_mounts: List[str]) -> List[str]:
    ctx.store['volume_file_mounts'] = []
    for volume_file_mount in volume_file_mounts:
        splitted = volume_file_mount.split(':')
        if len(splitted) != 2:
            raise ExitException(f'Invalid volume file mount format: {volume_file_mount}. '
                                f'You should specify both mount path and volume file.\n'
                                f'Volume file can be notated with volume id and subpath.'
                                f'ex) /input/model.pt:1#subPath=f72fca375e812/model.pt')

        mount_path, volume_id = splitted
        if '#subPath=' in volume_id:
            volume_id, sub_path = volume_id.split('#subPath=')
        else:
            sub_path = ''

        try:
            volume_id = int(volume_id)
        except ValueError:
            raise ExitException(f'Volume id should be an integer.')

        try:
            ctx.authenticated_client.volume_read(volume_id)
        except NotFoundAPIException:
            raise ExitException(f'Volume not found: {volume_id}')

        ctx.store['volume_file_mounts'].append(ProtoVolumeMountRequest(
            mount_type='volume',
            mount_path=mount_path,
            volume=ProtoVolumeMountRequestSourceVolume(
                volume_id=volume_id,
                sub_path=sub_path,
            )
        ))

    return volume_file_mounts
