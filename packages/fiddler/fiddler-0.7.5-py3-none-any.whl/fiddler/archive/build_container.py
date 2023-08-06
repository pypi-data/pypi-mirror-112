import os
import shutil
import subprocess
import tempfile
from pathlib import Path

fiddler_core_version = '0.7.5'


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def dockerfile(args):
    return f'''
    # syntax=docker/dockerfile:1
    FROM fiddlerai/fiddler-core:{fiddler_core_version}

    RUN mkdir /app/{args.org}
    RUN mkdir /app/{args.org}/{args.project}
    RUN mkdir /app/{args.org}/{args.project}/{args.model}

    COPY . /app/{args.org}/{args.project}/{args.model}

    RUN pip install -r /app/{args.org}/{args.project}/{args.model}/requirements.txt

    ENV FAR_MODEL_PATH {args.org}/{args.project}/{args.model}
    ENV SERVICE_RUN_MODE local
    ENV AUTHORIZATION_ENABLED False

    CMD ["/bin/bash", "/app/runit.sh"]
    '''


def call_cmd(cmd, cwd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        cwd=cwd,
    )

    return_code = None

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            for output in process.stderr.readlines():
                print(output.strip())
            break

    if return_code == 0:
        print('cmd successful')
    else:
        raise ValueError('cmd failed')


def build_cmd(args):
    print('building archive for ', args.org, ' ', args.project, ' ', args.model)

    source = Path(args.source)
    if not source.is_dir():
        raise ValueError('soruce is not a directory')
    if not Path(source, 'package.py').is_file():
        raise ValueError(f'package.py not found in {source}')
    if not Path(source, 'model.yaml').is_file():
        raise ValueError(f'model.yaml not found in {source}')
    if not Path(source, 'dataset.csv').is_file():
        raise ValueError(f'dataset.csv not found in {source}')
    if not Path(source, 'dataset.yaml').is_file():
        raise ValueError(f'dataset.yaml not found in {source}')
    if not Path(source, 'requirements.txt').is_file():
        raise ValueError(f'requirements.txt not found in {source}')

    with tempfile.TemporaryDirectory() as tmp:
        copytree(source, Path(tmp))
        docker_template = dockerfile(args)
        with open(tmp / Path('Dockerfile'), 'w') as output:
            output.write(docker_template)

        print(os.listdir(tmp))
        name = f'{args.org}-{args.project}-{args.model}'

        cmd = ['docker', 'build', '--file=Dockerfile', f'--tag={name}', '.']
        call_cmd(cmd, tmp)
        return 'done'


def run_cmd(args):
    name = f'{args.org}-{args.project}-{args.model}'

    cmd = [
        'docker',
        'run',
        '-d',
        '--rm',
        '--publish=5100:5100',
        f'--name={name}',
        f'{name}:latest',
    ]

    call_cmd(cmd, '.')
