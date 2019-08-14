import paramiko
from .unit import logger
import sys
import traceback


# TODO: pkey may need password
def ssh_exec(cmd, host, server_dict):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if "pkey" in server_dict:
        private_key = paramiko.RSAKey.from_private_key_file(server_dict['pkey'])
        ssh_client.connect(hostname=host, port=server_dict['port'], username=server_dict['user'],
                           timeout=server_dict['timeout'], pkey=private_key)
    else:

        ssh_client.connect(hostname=host, port=server_dict['port'], username=server_dict['user'],
                           timeout=server_dict['timeout'], password=server_dict['password'])

    stdin, stdout, stderr = ssh_client.exec_command(cmd, timeout=server_dict['timeout'])

    stdout_out = stdout.read()
    stderr_out = stderr.read()
    return stdout_out, stderr_out


def show_result(stdout, stderr):
    stdout_data = 'stdout:\n'
    stderr_data = 'stderr:\n'
    for line in stdout.strip().split(b'\n'):
        stdout_data += "\t" + line.decode() + '\n'

    for line in stderr.strip().split(b'\n'):
        stderr_data += '\t' + line.decode() + '\n'
    return stdout_data + stderr_data


def run_cmd(cmd, host, server_dict):
    try:
        stdout, stderr = ssh_exec(cmd, host, server_dict)
        ret_data = show_result(stdout, stderr)
    except Exception as e:
        data = traceback.format_exc(0)  # TODO: not good
        ret_data = data.split('\n')[1]

    return ret_data
