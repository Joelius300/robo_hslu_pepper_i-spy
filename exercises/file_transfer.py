import paramiko


class FileTransfer:
    def __init__(self, robot):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(robot.configuration.Ip, username=robot.configuration.Username, password=robot.configuration.Password)

    # copies the file from the remote location to the local file (path or file like)
    # and then deletes the file from the remove
    def get(self, remote_path, local_path_or_fl):
        sftp = self.ssh.open_sftp()
        if isinstance(local_path_or_fl, str):
            sftp.get(remote_path, local_path_or_fl)
        else:
            sftp.getfo(remote_path, local_path_or_fl)
        sftp.remove(remote_path)
        sftp.close()

    def close(self):
        self.ssh.close()
