import paramiko
import argparse


def main():
    parser = argparse.ArgumentParser(description='patch vCenter')
    parser.add_argument('--vcenter', help="vCenter to patch")
    parser.add_argument('--root_password', help="vCenter root password")

    args = parser.parse_args()
    vcenter = args.vcenter
    root_password = args.root_password

    ssh = connect_to_vcenter(vcenter, root_password)
    stage_url(ssh)
    ssh.close()

    ssh = connect_to_vcenter(vcenter, root_password)
    install_staged(ssh)
    ssh.close()


def connect_to_vcenter(vcenter, root_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vcenter, 22, 'root', root_password)
    return ssh


def stage_url(ssh):
    print("""############ STAGING VCENTER PATCHES FROM VMWARE URL ############""")
    stdin, stdout, stderr = ssh.exec_command("software-packages stage --url --acceptEulas")
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")


def install_staged(ssh):
    print("""\n############ INSTALLING VCENTER PATCHES ############""")
    stdin, stdout, stderr = ssh.exec_command("software-packages install --staged")
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")


if __name__ == "__main__":
    main()