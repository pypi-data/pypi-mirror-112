import click
from aihubcli.creator import createProject


@click.group()
def cli():
    print("version = 1.0.1")
    pass

@cli.command()
@click.argument('name')
@click.option('-f','--file', default=None, help='number of greetings')
def create(name, file):
    click.echo(f'creating project with name {name} and template file {file}')
    createProject(name)

@cli.command()
def describe():
    click.echo('Describe strcture of projects')


if __name__ == '__main__':
    cli(prog_name="aihubcli")