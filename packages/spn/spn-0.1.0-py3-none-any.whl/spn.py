#!/usr/bin/env python3

import sys
import time
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
        while True:
            r = super().request(method, url, *args, **kwargs)
            if r.status_code == 429:
                time.sleep(10)
            else:
                break
        r.raise_for_status()
        return r

    def save(self, url, **kwargs):
        return self.post('save', data={'url': url, **kwargs}).json()

    def status(self, job_id):
        return self.get(f'save/status/{job_id}').json()

    def await_status(self, job_id):
        while True:
            status = self.status(job_id)
            if status['status'] != 'pending':
                return status
            time.sleep(10)


@click.command()
@click.argument('urls', nargs=-1)
@click.option('--access-key', required=True)
@click.option('--secret-key', required=True)
@click.option('--stdin', is_flag=True)
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
def cli(urls, access_key, secret_key, stdin, verify, **kwargs):
    spn = SPN(access_key, secret_key)
    rv = []
    if stdin:
        def url_generator():
            for url in sys.stdin:
                yield url.rstrip()
        urls = url_generator()
    for url in urls:
        click.secho('capture:', nl=False, fg='blue')
        click.echo(url)
        r = spn.save(url, **kwargs)
        if verify:
            rv.append(r)
        if 'message' in r:
            click.secho(r['message'], fg='red')
    for r in rv:
        click.secho('verify:', nl=False, fg='blue')
        click.echo(r['url'] + ':', nl=False)
        status = spn.await_status(r['job_id'])
        status = r['status'] = status['status']
        click.secho(status, fg={'success': 'green'}.get(status, 'red'))
    sys.exit(any([r['status'] != 'success' for r in rv]))


def main():
    cli(auto_envvar_prefix='SPN')


if __name__ == '__main__':
    main()
