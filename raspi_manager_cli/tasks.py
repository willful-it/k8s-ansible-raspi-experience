from crypt import METHOD_SHA512, crypt, mksalt

import nmap3
from colorama import Back, Fore, Style
from getmac import get_mac_address
from invoke import task

import persistence as db


def _sudo(c, cmd: str, msg: str, show_command=True) -> str:
    cmd_to_show = "" if not show_command else "=> " + cmd
    print(Fore.BLUE, ".", msg, Style.RESET_ALL + cmd_to_show)
    return c.sudo(cmd, hide=True).stdout.strip()


def _print_title(text: str):
    print(Back.YELLOW + Fore.BLACK, text + ": " + Style.RESET_ALL)


@task
def find_raspis(c):
    """
    Finds raspberry pi devices and adds them to the inventory
    """
    nmap = nmap3.NmapScanTechniques()
    map = nmap.nmap_ping_scan("192.168.1.0/24")

    for k in map.keys():
        if k in ("stats", "runtime"):
            print(f"ignoring {k}")
            continue

        hostname = map[k]['hostname'][0]['name']
        if "ubuntu" not in hostname and "raspberrypi" not in hostname:
            print(f"ignoring {hostname}")
            continue

        mac = get_mac_address(ip=k)
        print(f"handling {k} {mac} {hostname}")

        host = db.get_host_by_mac(mac)
        if host:
            print("host found in the inventory - ignoring")
            continue

        host = db.save_host(ip=k, mac=mac, hostname=hostname)


@task(help={"image-path": "The path to the original image file"})
def prepare_image(c,
                  image_path,
                  output_image_path,
                  mount_path="/mnt/sdcard",
                  ssh_public_key_file="~/.ssh/id_ed25519_pi.pub",
                  root_password_clear="1234567890",
                  user="ubuntu",
                  user_password_clear="1234567890"):
    """Prepares an image to be installed in the raspberry pi"""

    print(f"processing {image_path}")

    #
    # starting...
    #
    _print_title("starting")
    loop_base = _sudo(
        c, f"losetup --partscan --find --show {image_path}",
        "get image device")

    #
    # handling boot disk
    #
    _print_title("handling boot disk")
    try:
        _sudo(c, f"mount {loop_base}p1 {mount_path}", "mounting the boot disk")
        _sudo(c, f"touch '{mount_path}/ssh'", "activating ssh")
    except Exception as e:
        _sudo(c, f"losetup -d {loop_base}", "detaching devices")
        raise e
    finally:
        _sudo(c, f"umount {loop_base}p1", "unmounting the boot disk")

    #
    # handling root disk
    #
    _print_title("handling root disk")
    try:
        _sudo(c, f"mount {loop_base}p2 {mount_path}", "mounting the root disk")

        root_password = crypt(root_password_clear, mksalt(METHOD_SHA512))
        user_password = crypt(user_password_clear, mksalt(METHOD_SHA512))

        _sudo(
            c,
            f"sed -e 's#^root:[^:]\\+:#root:${root_password}:#' "
            f"{mount_path}/etc/shadow -i {mount_path}/etc/shadow",
            "setting root password")

        root_line = _sudo(
            c,
            f"sed -n '/root/ p' {mount_path}/etc/shadow",
            "copying root password line")

        user_line = root_line.replace("root", user)
        _sudo(
            c,
            f"sed '$a{user_line}' -i {mount_path}/etc/shadow",
            "adding user to passwords file")

        _sudo(
            c,
            f"sed -e 's#^{user}:[^:]\\+:#{user}:{user_password}:#' "
            f"{mount_path}/etc/shadow -i '{mount_path}/etc/shadow'",
            "setting user password")

        _sudo(
            c,
            "sed -e 's;^#PasswordAuthentication.*$;"
            "PasswordAuthentication no;g' "
            "-e 's;^PermitRootLogin .*$;PermitRootLogin no;g' "
            f"-i '{mount_path}/etc/ssh/sshd_config'",
            "prevent ssh with password authentication")

        _sudo(
            c,
            f"mkdir -p {mount_path}/home/{user}/.ssh",
            "create .ssh directory")

        _sudo(
            c,
            f"chmod 0700 {mount_path}/home/{user}/.ssh",
            "change .ssh directory permissions")

        _sudo(
            c,
            f"chown 1000:1000 {mount_path}/home/{user}/.ssh",
            "change .ssh directory ownership")

        _sudo(
            c,
            f"cat {ssh_public_key_file} > "
            f"{mount_path}/home/{user}/.ssh/authorized_keys",
            "create authorized_keys file with the ssh public key")

        _sudo(
            c,
            f"chmod 0600 {mount_path}/home/{user}/.ssh/authorized_keys",
            "change authorized_keys file permission")

        _sudo(
            c,
            f"chown 1000:1000 {mount_path}/home/{user}/.ssh/authorized_keys",
            "change authorized_keys file ownership")

    finally:
        _sudo(c, f"umount {loop_base}p2", "unmounting the boot disk")

    #
    # generating new image
    #
    _print_title("generating the new image")
    _sudo(
        c,
        f"cp -v {image_path} {output_image_path}",
        "creating the new image")

    #
    # finishing
    #
    _print_title("finishing")
    _sudo(c, f"losetup -d {loop_base}", "detaching devices")
