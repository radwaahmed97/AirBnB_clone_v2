#!/usr/bin/python3
"""deletes outofdate archives"""


from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['34.229.71.81', '100.25.118.253']


def do_pack():
    """generates a .tgz archive from the contents of web_static"""
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(fname))
    if result.succeeded:
        return fname
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if exists(archive_path) is False:
        return False
    fname = archive_path.split('/')[-1]
    no_tgz = '/data/web_static/releases/' + "{}".format(fname.split('.')[0])
    tmp = "/tmp/" + fname

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    newarchive_path = do_pack()
    if exists(newarchive_path) is False:
        return False
    result = do_deploy(newarchive_path)
    return result


def do_clean(number=0):
    """
    Keep it cleanning the repositories
    """
    if number == 0 or number == 1:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +1 | xargs -d '\n' rm -rf")
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +1 | xargs -d '\n' rm -rf")
    else:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +{} | xargs -d '\n' rm -rf".format(number))
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
                    rev | head -n +{} | xargs -d '\n' rm -rf".format(number))
