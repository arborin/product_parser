import paramiko
from threading import Thread
import time




class Device:

    conn = ''

    def __init__(self, ip, user, password, port=22):

        self.ip = ip
        self.user = user
        self.password = password
        self.port = port

        self.connect()

    
    def connect(self):
        
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(self.ip, username=self.user, password=self.password, port=self.port, timeout=3)
        time.sleep(1)
        # remote_conn_pre.connect("73.215.176.112", username = "nkobaidze", password = "nikakobaidze1", port=4010, look_for_keys = False, allow_agent = False)# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


    def command(self, command_list):

        for command in command_list:
            print(">> {}".format(command))
            self.connect()

            stdin, stdout, stderr = self.conn.exec_command("{}\n".format(command))
            time.sleep(.5)
            resp = ''.join(stdout)
            print( resp )
    




if __name__ == "__main__":
    
    print("\n==============================CISCO========================================\n")

    cisco = Device("73.215.176.112", "nkobaidze", "nikakobaidze", 4009)
    
    # COMMAND LIST
    command_list = ["show version", "show ip int br"]
    cisco.command(command_list)


    print("\n==============================JUNIPER======================================\n")

    juniper = Device("73.215.176.112", "nkobaidze", "nikakobaidze1", 4010)

    # COMMAND LIST
    command_list = ["show version", "show version"]
    juniper.command(command_list)

    print("\n================================END========================================\n")