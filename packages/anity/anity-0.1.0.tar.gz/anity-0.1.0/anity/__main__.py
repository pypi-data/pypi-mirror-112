import base64
import os
import sys

import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('api-key')
@click.option('--dev', is_flag=True, help='run against the staging api')
def update(path, api_key, dev):
    url = _url(f'scheduler/v1/suite/{api_key}', dev)

    with open(path, 'rb') as f:
        resp = requests.put(url, data=base64.b64encode(f.read()))
        if resp.status_code != 200:
            print(f'failed to update tests [{resp.status_code}]')


@cli.command()
@click.argument('api-key')
@click.option('--dev', is_flag=True, help='run against the staging api')
def invoke(api_key, dev):
    url = _url(f'scheduler/v1/invoke/{api_key}', dev)
    resp = requests.post(url)
    if resp.status_code != 200:
        print(f'failed to invoke api [{resp.status_code}]')
    results = resp.json()
    print(results)
    ok = True
    for t in results:
        if t['status'] != 'pass':
            ok = False
        print(f"{t['service_name']} {t['test_name']} {t['timestamp']} {t['runtime']} {t['status']}")

    if not ok:
        sys.exit(-1)


@cli.command()
@click.argument('api-key')
@click.option('--dev', is_flag=True, help='run against the staging api')
def invoke_async(api_key, dev):
    url = _url(f'scheduler/v1/invoke/{api_key}/async', dev)
    resp = requests.post(url)
    if resp.status_code != 200:
        print(f'failed to invoke api [{resp.status_code}]')


def _url(path, dev):
    domain = 'api2.dev.anity.io' if dev else 'api2.anity.io'
    return f'https://{domain}/{path}'
