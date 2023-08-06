import getpass
import os
import sys

import click

import mask_in_situ.core as core


def get_key(env_var):
    key = ''
    if env_var:
        key = os.environ.get(env_var, '')
    if not key:
        key = getpass.getpass("Encryption key:").strip()
    return key


@click.group()
def cli():
    pass


@click.command(help="Randomly generate a new encryption key")
def generate_key():
    click.echo(core.generate_key())


@click.command(help="Hide the secrets in a file")
@click.option('-e', '--env-var')
@click.argument('infile', type=click.File(mode='r'), default=sys.stdin)
@click.argument('outfile', type=click.File(mode='w'), default=sys.stdout)
def encrypt(env_var, infile, outfile):
    key = get_key(env_var)

    for line in infile:
        outfile.write(core.encrypt_string(line, key))


@click.command(help="Reveal the secrets in a file")
@click.option('-e', '--env-var')
@click.argument('infile', type=click.File(mode='r'), default=sys.stdin)
@click.argument('outfile', type=click.File(mode='w'), default=sys.stdout)
def decrypt(env_var, infile, outfile):
    key = get_key(env_var)

    for line in infile:
        outfile.write(core.decrypt_string(line, key))


@click.command(help="Hide the secrets in every file in a directory")
@click.option('-e', '--env-var')
@click.argument('indir', type=click.Path())
@click.argument('outdir', type=click.Path())
def encrypt_dir(env_var, indir, outdir):
    key = get_key(env_var)

    os.makedirs(outdir, exist_ok=True)

    for root, subdirs, files in os.walk(indir):
        for file in files:
            with open(os.path.join(root, file), 'r') as infile:

                relpath = os.path.relpath(root, indir)
                os.makedirs(os.path.join(outdir, relpath), exist_ok=True)

                with open(os.path.join(outdir, relpath, file), 'w') as outfile:
                    for line in infile:
                        outfile.write(core.encrypt_string(line, key))


@click.command(help="Hide the secrets in every file in a directory")
@click.option('-e', '--env-var')
@click.argument('indir', type=click.Path())
@click.argument('outdir', type=click.Path())
def decrypt_dir(env_var, indir, outdir):
    key = get_key(env_var)

    os.makedirs(outdir, exist_ok=True)

    for root, subdirs, files in os.walk(indir):
        for file in files:
            with open(os.path.join(root, file), 'r') as infile:
                relpath = os.path.relpath(root, indir)
                os.makedirs(os.path.join(outdir, relpath), exist_ok=True)

                with open(os.path.join(outdir, relpath, file), 'w') as outfile:
                    for line in infile:
                        outfile.write(core.decrypt_string(line, key))


cli.add_command(generate_key)

cli.add_command(encrypt)
cli.add_command(decrypt)

cli.add_command(encrypt_dir)
cli.add_command(decrypt_dir)

if __name__ == '__main__':
    cli()
