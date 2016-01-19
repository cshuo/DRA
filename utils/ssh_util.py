import paramiko
from openstack import conf 

class SshTool:

    def __init__(self, hostname, port, username = conf.HOST_USERNAME, password = conf.HOST_PASSWORD):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname, port, username, password)


    def remote_cmd(self, command):
        stdin, stdout, stderr = self.sshclient.exec_command(command)

        #print "remote command: " + command + "\n"
        #print "stdout: " + stdout.read() + "\n"
        #print "stderr: " + stderr.read() + "\n"

        return {"stdin" : stdin,
                "stdout" : stdout,
                "stderr" : stderr}

    def close(self):
        self.sshclient.close()

if __name__=="__main__":
    cmd = "nova %s live-migration --block-migrate 8387a836-1a28-4061-8c25-e5a57ff170e8 compute1" % conf.PARAMS
    ssh = SshTool("20.0.1.11",22,"root","cshuo")
    print ssh.remote_cmd(cmd)['stderr'].read()
    ssh.close()
