#!/usr/bin/env python3

import time
import sys
import urllib.parse

import click
import requests


class SPN(requests.Session):
    base_url = 'https://web.archive.org/'

    def __init__(self, access_key, secret_key, base_url=base_url):
        super().__init__()
        self.base_url = base_url
        self.headers['accept'] = 'application/json'
        self.headers['authorization'] = f'LOW {access_key}:{secret_key}'

    def request(self, method, url, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url)
        r = super().request(method, url, *args, **kwargs)
        r.raise_for_status()
        return r

    def save(self, url, **kwargs):
        return self.post('save', data={'url': url, **kwargs}).json()

    def status(self, job_id):
        return self.get(f'save/status/{job_id}').json()


@click.command()
@click.argument('urls', nargs=-1)
@click.option('--access-key', required=True)
@click.option('--secret-key', required=True)
@click.option('--verify', is_flag=True)
@click.option('--capture-all', type=int, is_flag=True)
@click.option('--capture-outlinks', type=int, is_flag=True)
@click.option('--capture-screenshot', type=int, is_flag=True)
@click.option('--delay-wb-availability', type=int, is_flag=True)
@click.option('--force-get', type=int, is_flag=True)
@click.option('--skip-first-archive', type=int, is_flag=True)
@click.option('--if-not-archived-within')
@click.option('--outlinks-availability', type=int, is_flag=True)
@click.option('--email-result', type=int, is_flag=True)
@click.option('--js-behavior-timeout', type=int)
@click.option('--capture-cookie')
@click.option('--target-username')
@click.option('--target-password')
def main(urls, access_key, secret_key, verify, **kwargs):
    spn = SPN(access_key, secret_key)
    rv = []
    for url in urls:
        click.echo(url)
        delay = 0
        while True:
            time.sleep(delay)
            try:
                r = spn.save(url, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    delay = min(delay + 1, 30)
                else:
                    raise
            else:
                if verify:
                    rv.append(r)
                break
        if 'message' in r:
            click.secho(r['message'], fg='red')
    for r in rv:
        click.echo('verify:' + r['url'] + ':', nl=False)
        delay = 0
        while True:
            time.sleep(delay)
            status = spn.status(r['job_id'])
            if status['status'] != 'pending':
                break
            delay = min(delay + 1, 30)
        r['status'] = status['status']
        click.secho(r['status'], fg={'success': 'green'}.get(r['status'], 'red')) # noqa
    sys.exit(any([r['status'] != 'success' for r in rv]))


if __name__ == '__main__':
    main(auto_envvar_prefix='SPN')
