import inquirer
import typer
from savvihub.api.exceptions import InvalidParametersAPIException, DuplicateAPIException

from openapi_client import ResponseOrganization
from savvihub import SavviHubClient


def get_default_organization(client: SavviHubClient) -> ResponseOrganization:
    organizations = client.organization_list().organizations
    if len(organizations) == 0:
        region_list_resp = client.region_list()
        typer.echo('Create organization')
        while True:
            organization_name = inquirer.prompt([inquirer.Text(
                'organization_name',
                message="Organization name",
            )], raise_keyboard_interrupt=True).get('organization_name')
            region = inquirer.prompt([inquirer.List(
                'region',
                message="Select region",
                default=region_list_resp.default_region,
                choices=[(region.name, region.value) for region in region_list_resp.regions]
            )], raise_keyboard_interrupt=True).get('region')
            try:
                default_organization = client.organization_create(organization_name=organization_name, region=region)
                break
            except InvalidParametersAPIException:
                typer.echo('Invalid organization name. Please try again.')
            except DuplicateAPIException:
                typer.echo('Duplicate organization name exist. Please try again.')
    elif len(organizations) == 1:
        default_organization = organizations[0]
        typer.echo(f'Default organization is automatically set to `{default_organization.name}`.')
    else:
        default_organization = inquirer.prompt([inquirer.List(
            'default_organization',
            message='Select default organization',
            choices=[(ws.name, ws) for ws in organizations],
        )], raise_keyboard_interrupt=True).get('default_organization')

        typer.echo(f'Default organization is set to `{default_organization.name}`.')

    return default_organization


def find_from_inquirer(options, display, message):
    return inquirer.prompt([inquirer.List(
        "question",
        message=message,
        choices=[(f'[{i+1}] {display(option)}', option) for i, option in enumerate(options)],
    )], raise_keyboard_interrupt=True).get("question")


def parse_dataset(dataset_full_name):
    if '@' in dataset_full_name:
        dataset_name, dataset_version_name = dataset_full_name.split('@', 1)
    else:
        dataset_name = dataset_full_name
        dataset_version_name = 'latest'

    if '/' in dataset_name:
        organization_name, dataset_name = dataset_name.split('/', 1)
    else:
        organization_name = None

    return organization_name, dataset_name, dataset_version_name
