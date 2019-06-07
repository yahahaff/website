import paramiko


class SSHConnectException(Exception):
    """自定义SSH连接错误捕获"""
    pass

class SSHRrmote(object):
    def __init__(self, hostname, username='root', port=22):
        self.hostname = hostname
        self.username = username
        self.port = port
        # pravie_key_path = '/root/.ssh/id_rsa'
        pravie_key_path = '/tmp/id_rsa'
        key = paramiko.RSAKey.from_private_key_file(pravie_key_path)
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.hostname, port=int(self.port), pkey=key, username=self.username)
        except Exception as e:
            raise SSHConnectException(e)
        print('建立连接成功')

    def Run_Cmmond(self, cmd):
        """

        :param cmd:
        :return: (stdout,stderr,exit_status)
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status() #获取命令执行状态返回吗
        print(exit_status)
        return (stdout.read().decode('utf-8'), stderr.read().decode('utf-8'), exit_status)

    def file_pull(self):
        #有待改进，因为连接多个主机时，会覆盖文件
        print('开始下载')
        try:
            trans = paramiko.Transport(self.hostname,int(self.port))
            trans.connect(username=self.username,password=self.passwd)
            print('hello')
        except Exception as e:
            print("连接失败")
        else:
            sftp = paramiko.SFTPClient.from_transport(trans)
            cmd = self.cmd.split()[1:]
            if len(cmd)==2:
                sftp.get(cmd[0], cmd[1])
                print("下载文件%s成功，并保存为%s" %(cmd[0],cmd[1]))
            else:
                print("参数有误")
            trans.close()
    def file_put(self):

        print("开始上传")   #注意你使用的用户是否为kiosk
        try:
            trans = paramiko.Transport(self.hostname, int(self.port))
            trans.connect(username=self.username, password=self.passwd)

        except Exception as e:
            print("连接失败")
        else:
            sftp = paramiko.SFTPClient.from_transport(trans)
            cmd = self.cmd.split()[1:]
            if len(cmd) == 2:
                sftp.put(cmd[0],cmd[1])
                print("上传文件%s成功，并保存为%s" %(cmd[0], cmd[1]))
            else:
                print("参数有误")
            trans.close()


