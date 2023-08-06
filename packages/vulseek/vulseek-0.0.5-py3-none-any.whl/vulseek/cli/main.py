import getpass
import json
from pathlib import Path

import click
import requests
import requests_cache

#requests_cache.install_cache('/tmp/vulseek_requests.sqlite', expire_after=300)

session_data = {}

session_file = Path('~/.vulseek/session.json').expanduser()
session_file.parent.mkdir(exist_ok=True)


identity_mapping = {
    'ip': 'address',
    'network': 'address',
    'domain': 'name',
    'hostname': 'name',
    'web': 'identity',
}


class VulseekSession():
    pass

def load_session():
    session_data = {}
    if session_file.is_file():
        session_data = json.load(session_file.open())
    return session_data


def save_session(session_data):
    with session_file.open('w') as outfile:
        outfile.write(json.dumps(session_data, indent=4))


@click.group()
@click.pass_context
def cli(ctx):

    ctx.obj = VulseekSession()
    ctx.obj.data = load_session()
    ctx.obj.requests = requests.Session()

    if ctx.obj.data:
        ctx.obj.requests.headers.update({
            'Authorization': f'Bearer {ctx.obj.data["access_token"]}'
        })


@cli.command(help='List current sessions')
@click.pass_obj
def session(session):

    if not session.data:
        click.echo('Not logged in')
        return False

    click.echo(json.dumps(dict(
        username=session.data['username'],
        endpoint=session.data['endpoint'],
    ), indent=4))


@cli.command(help='Create new session')
@click.argument('endpoint', default='http://localhost:8080')
def login(endpoint):

    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')

    save_session({})

    r = requests.post(endpoint + '/user/login', data=dict(username=username, password=password))
    if r.status_code != 200:
        click.echo('Invalid credentials', err=True)
        return False

    access_token = r.json()['access_token']

    session_data = {
        'endpoint': endpoint,
        'username': username,
        'access_token': access_token,
    }

    save_session(session_data)


@cli.command(help="Logout")
def logout():
    save_session({})



def get_objects(session, object_type):

    response = session.requests.get('{}/{}/'.format(session.data['endpoint'], object_type))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return []
    return response.json()


def url_from_service(service):
    if service['application'] != 'http':
        return None

    if service['tls']:
        scheme = 'https'
    else:
        scheme = 'http'

    if service['hostname']:
        hostname = service['hostname']
    else:
        hostname = service['ip']

    if service['path']:
        path = service['path']
    else:
        path = '/'

    port = None

    if scheme == 'http' and service['port'] != 80:
        port = service['port']
    elif scheme == 'https' and service['port'] != 443:
        port = service['port']

    if port:
        url = f'{scheme}://{hostname}:{port}{path}'
    else:
        url = f'{scheme}://{hostname}{path}'

    return url


@cli.command(help='List objects')
@click.argument('object_type', type=click.Choice(['domain', 'finding', 'hostname', 'ip', 'network', 'service', 'web', 'dump']))
@click.pass_obj
def ls(session, object_type):

    db = {}
    db['ip'] = get_objects(session, 'ip')

    if object_type == 'ip':

        for ip in sorted(db['ip'], key=lambda x: x['vpr'], reverse=True):
            print(f'{ip["vpr"]:.0f} - {ip["max_score"]} - {ip["address"]}')

    elif object_type == 'service':
        print('{:>10} - {:>5} - {}'.format('VPR', 'Max', 'IP/Protocol/Port'))
        for ip in sorted(db['ip'], key=lambda x: x['vpr'], reverse=True):
            for service in sorted(ip['service'], key=lambda x: x['vpr'], reverse=True):
                if service['port']:
                    print(f'{service["vpr"]:>10.0f} - {service["max_score"]:>5} - {ip["address"]}/{service["protocol"]}/{service["port"]}')

    elif object_type == 'finding':
        finding_list = []
        for ip in db['ip']:
            for service in ip['service']:
                for finding in service['finding']:
                    if service['port']:
                        if service['url']:
                            finding_list.append(f'{finding["score"]:>4} - {finding["title"]} - {service["url"]}')
                        else:
                            finding_list.append(f'{finding["severity"]} - {finding["score"]:>4} - {finding["title"]} - {ip["address"]}/{service["protocol"]}/{service["port"]}')
                    else:
                        finding_list.append(f'{finding["score"]:>4} - {finding["title"]} - {ip["address"]}')

        for finding in sorted(finding_list, reverse=True):
            print(finding)

    elif object_type == 'web':
        web_list = []
        for ip in db['ip']:
            for service in ip['service']:
                if service['url']:
                    web_list.append(service['url'])

        for web in sorted(web_list):
            print(web)

    elif object_type == 'hostname':
        hostname_list = []
        for ip in db['ip']:
            for hostname in ip['hostname']:
                hostname_list.append((hostname['name'], ip['address']))

        for hostname, ip in sorted(hostname_list, key=lambda x: x[0]):
            print(f'{hostname} {ip}')

    elif object_type == 'network':
        db['network'] = get_objects(session, 'network')
        for network in db['network']:
            print(network['address'])

    elif object_type == 'domain':
        db['domain'] = get_objects(session, 'domain')
        for domain in db['domain']:
            print(domain['name'])

    elif object_type == 'dump':
        print(json.dumps(db['ip'], indent=4))





def print_finding_count(session):
    response = session.requests.get('{}/{}'.format(session.data['endpoint'], 'statistic/finding-count'))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return False

    data = response.json()

    for key in ['critical', 'high', 'medium', 'low']:
        print(f'{key.upper():<12}{data[key]}')

    print('')





def print_asset_count(session):
    response = session.requests.get('{}/{}'.format(session.data['endpoint'], 'statistic/asset-count'))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return False

    data = response.json()

    for key in ['ip', 'service', 'domain', 'web']:
        print(f'{key.upper():<12}{data[key]}')

    print('')


def print_top(name, session):
    """Obtiene y muestra un top (cve, cwe, service)"""
    if name not in ['cve', 'cwe', 'service', 'product']:
        return False

    response = session.requests.get('{}/{}'.format(session.data['endpoint'], f'statistic/top-{name}'))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        top = []
    else:
        top = response.json()

    max_length = 0

    for entry in top:
        if len(entry['key']) > max_length:
            max_length = len(entry['key'])

    max_length += 3

    for entry in top:
        print('{key:<{max_length}}{bar} {count}'.format(key=entry['key'], max_length=max_length, bar='#'*entry['count'], count=entry['count']))


@cli.command(help='Print a Dashboard')
@click.pass_obj
def dash(session):

    print('FINDING COUNT')
    print_finding_count(session)

    print('ASSET COUNT')
    print_asset_count(session)


    for name in ['cve', 'cwe', 'service', 'product']:
        print('TOP {}'.format(name.upper()))
        print_top(name, session)
        print('')

    """
    response = session.requests.get('{}/{}'.format(session.data['endpoint'], 'statistic/top-service'))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return []
    print('top-service:', response.json())

    response = session.requests.get('{}/{}'.format(session.data['endpoint'], 'statistic/finding-count'))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return []
    print('finding-count:', response.json())
    """



@cli.command(help="Add object")
@click.argument('object_type', type=click.Choice(['domain', 'hostname', 'ip', 'network', 'web']))
@click.argument('identity')
@click.pass_obj
def add(session, object_type, identity):

    payload = { identity_mapping.get(object_type) : identity }
    #response = session.requests.post('{}/{}/'.format(session.data['endpoint'], object_type), json=dict(identity=identity))
    response = session.requests.post('{}/{}/'.format(session.data['endpoint'], object_type), json=payload)
    if response.status_code != 200:
        click.echo('{}: {}'.format(response.status_code, response.content.decode()), err=True)
        return False

    click.echo(json.dumps(response.json(), indent=4))


@cli.command(help="Delete object")
@click.argument('object_type', type=click.Choice(['domain', 'hostname', 'ip', 'network', 'web']))
@click.argument('identity')
@click.pass_obj
def delete(session, object_type, identity):

    # Object Identity Attribute
    oia = identity_mapping.get(object_type)

    response = session.requests.get('{}/{}/'.format(session.data['endpoint'], object_type))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return False

    object_id = None
    for obj in response.json():
        if obj[oia] == identity:
            object_id = obj['id']

    if not object_id:
        click.echo('404: Not found')
        return False

    response = session.requests.delete('{}/{}/{}'.format(session.data['endpoint'], object_type, object_id))
    if response.status_code != 200:
        click.echo(response.content.decode(), err=True)
        return False


@cli.command(help='Upload files')
@click.argument('files', nargs=-1, type=click.Path())
@click.pass_obj
def upload(session, files):

    for filename in files:

        try:
            data = open(filename).read()
        except Exception as e:
            click.echo(f'{filename}: {e}')
            continue

        response = session.requests.post(session.data['endpoint'] + '/upload/', files=dict(file_obj=data))

        if response.status_code == 200:
            click.echo(f'{filename}: OK')
        else:
            click.echo('{filename}: {error}'.format(filename=filename, error=response.content.decode()))


@cli.command(help="Export data")
@click.argument('fmt', type=click.Choice(['fast']), default='fast')
@click.pass_obj
def export(session, fmt):

    #response = session.requests.get(f'export/{fmt}/')#.format(session.data['endpoint'], object_type), json=dict(identity=identity))
    response = session.requests.get(session.data['endpoint'] + '/export/' + fmt)
    if response.status_code != 200:
        click.echo('{}: {}'.format(response.status_code, response.content.decode()), err=True)
        return False

    click.echo(json.dumps(response.json(), indent=4))


if __name__ == '__main__':
    cli()
