import os
import subprocess


def get_app(uuid, app_id, version, url, platform):
    app_dir = make_app_dir(app_id, url)
    result = compile_app(app_dir)
    return result


def make_app_dir(app_id, url):
    builds_dir = "data/builds/"
    app_dir = builds_dir + app_id

    if os.path.exists(builds_dir):
        if os.path.exists(app_dir):
            pull(app_dir=app_dir)
        else:
            clone(url=url, app_id=app_id, builds_dir=builds_dir)
    else:
        os.makedirs(builds_dir)
        clone(url=url, app_id=app_id, builds_dir=builds_dir)

    return app_dir


def compile_app(app_dir_name):
    app_dir_size = get_size(app_dir_name)
    return app_dir_size


def get_size(app_dir_name):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(app_dir_name):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def clone(builds_dir, url, app_id):
    command = "git clone " + url + ' ' + app_id
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=builds_dir)
    stdout, stderr = p.communicate()
    print("communicate", stdout, stderr, p.poll())


def pull(app_dir):
    command = "git pull"
    subprocess.Popen(command, cwd=app_dir)

