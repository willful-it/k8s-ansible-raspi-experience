from crypt import METHOD_SHA512, crypt, mksalt
from pathlib import Path

import nmap3
from colorama import Back, Fore, Style
from getmac import get_mac_address
from invoke import task

from persistence import PersistenceService


def _sudo(c, cmd: str, msg: str, show_command=False) -> str:
    cmd_to_show = "" if not show_command else "=> " + cmd
    print(Fore.BLUE, ".", msg, Style.RESET_ALL + cmd_to_show)
    return c.sudo(cmd, hide=True).stdout.strip()


def _print_title(text: str):
    print(Back.YELLOW + Fore.BLACK + text + Style.RESET_ALL)


@task
def find_raspis(c):
    """
    Finds raspberry pi devices and adds them to the inventory
    """
    db = PersistenceService()

    _print_title("scanning for raspberry pi devices...")
    nmap = nmap3.NmapScanTechniques()
    map = nmap.nmap_ping_scan("192.168.1.0/24")

    for k in map.keys():
        if k in ("stats", "runtime"):
            print(f"ignoring {k} section")
            continue

        hostname = map[k]['hostname'][0]['name']
        if "ubuntu" not in hostname and \
                "raspberrypi" not in hostname and \
                "worker" not in hostname and \
                "master" not in hostname:
            print(f"ignoring {k} ({hostname})")
            continue

        mac = get_mac_address(ip=k)
        host = db.get_host_by_mac(mac)
        if host:
            print(f"ignoring {k} ({hostname}) "
                  "because it is already in inventory")
            continue

        print(f"saving {k} ({hostname})")
        host = db.create_host(ip=k, mac=mac, hostname=hostname, role="")


@task(help={"image-path": "The path to the original image file"})
def prepare_image(c,
                  image_path,
                  output_image_path,
                  mount_path="/mnt/sdcard",
                  ssh_public_key_file="~/.ssh/id_ed25519_pi.pub",
                  user="ubuntu",
                  root_password_clear="1234567890",
                  user_password_clear="1234567890",
                  role="worker"):
    """Prepares an image to be installed in the raspberry pi"""

    print(f"processing {image_path}")

    #
    # generating new image
    #
    _print_title("generating the new image")
    _sudo(
        c,
        f"rm -f {output_image_path}",
        "delete previouslly generate image")

    _sudo(
        c,
        f"cp -v {image_path} {output_image_path}",
        "creating the new image")

    _sudo(
        c,
        f"chmod 777 {output_image_path}",
        "changing permissions of the new image")

    #
    # starting...
    #
    _print_title("starting")
    loop_base = _sudo(
        c, f"losetup --partscan --find --show {output_image_path}",
        "get image device")

    #
    # handling boot disk
    #
    _print_title("handling boot disk")
    try:
        _sudo(c, f"mount {loop_base}p1 {mount_path}", "mounting the boot disk")
        _sudo(c, f"touch '{mount_path}/ssh'", "activating ssh")

        user_password = crypt(user_password_clear, mksalt(METHOD_SHA512))
        root_password = crypt(root_password_clear, mksalt(METHOD_SHA512))

        with open(Path(ssh_public_key_file).expanduser(), 'r') as ssh_file:
            ssh_public_key_content = ssh_file.read()

        with open('user-data-template', 'r') as userdata_file:
            template = userdata_file.read()
            content = template.replace("<user>", user)
            content = content.replace("<user_password>", user_password)
            content = content.replace("<root_password>", root_password)
            content = content.replace(
                "<ssh_public_key>", ssh_public_key_content)
            content = content.replace("<raspi_role>", role)

            with open('.new-user-data', 'w') as new_userdata_file:
                new_userdata_file.write(content)

        _sudo(
            c,
            f"cp .new-user-data {mount_path}/user-data",
            "customizing user-data")

        _sudo(
            c,
            "rm .new-user-data",
            "remove temporary user-data file")

    except Exception as e:
        _sudo(c, f"losetup -d {loop_base}", "detaching devices")
        raise e
    finally:
        _sudo(c, f"umount {loop_base}p1", "unmounting the boot disk")

    #
    # finishing
    #
    _print_title("finishing")
    _sudo(c, f"losetup -d {loop_base}", "detaching devices")
