import click
from aihubcli.creator import createProject


@click.group()
def cli():
    print("version = 1.0.0")
    pass

@cli.command()
@click.argument('name')
@click.option('-t','--template', default='default', help='name of the template to use')
def create(name, template):
    click.echo(f'creating project with name {name} and template file {template}')
    createProject(name, template)

@cli.command()
def list():
    click.echo('template name: default \n\nCurrently there is only one default template available. we can register more templates in the project')


if __name__ == '__main__':
    cli(prog_name="nextai")