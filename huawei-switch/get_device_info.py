import time
import warnings
import re
import pandas as pd
import paramiko


warnings.filterwarnings('ignore')


j_user = 'jump_host_user'
j_pass =  'jump_host_pwd'
j_host =  'jump_host_ip'

SW3 = {'ip': '10.11.71.141', 'username': 'admin', 'password': 'admin1'}
SW2 = {'ip': '10.11.72.15', 'username': 'admin', 'password': 'admin1'}
SW1 = {'ip': '10.11.72.17', 'username': 'admin', 'password': 'admin1'}


all_devices = [SW1,SW2,SW3]

tablelist = []
for device in all_devices:
    sw_user = device.get('username')
    sw_pass = device.get('password')
    sw_ip = device.get('ip')
    print(f"Connecting to {sw_ip}")
    vm = paramiko.SSHClient()
    vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    vm.connect(j_host, username=j_user, password=j_pass)
    vmtransport = vm.get_transport()
    dest_addr = (sw_ip, 22) #edited
    local_addr = (j_host, 22) #edited
    vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
    jhost = paramiko.SSHClient()
    jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jhost.connect(sw_ip, username=sw_user, password=sw_pass, sock=vmchannel)

    # Request an interactive shell session on this channel.
    commands = jhost.invoke_shell()  
    print(f"Connected to {sw_ip}")     

    # Send command to device
    # commands.send("display version\n")  
    # output = commands.recv(65535)   
    # output = output.decode("utf-8") 

    # with open('version_file', 'w') as f:
    #     print(output, file=f)

    commands.send("display elabel slot 0\n")    
    commands.send("y\n\n\n") 
    time.sleep(10)
    output = commands.recv(65535)   
    output = output.decode("utf-8")  

    with open('.tmp', 'w') as f:
        print(output, file=f)
    
    

    sn_re = 'BarCode'
    boardtype_re = 'BoardType'
    manufactured_re = 'Manufactured'
    vendor_re = 'VendorName'
    version = 'Software      Version'

    # for line in open('version_file', 'r'):
    #         if re.search(version, line):
    #              l = line
    #              c = re.findall('\((.*?)\)', l)
    #              c = c[-1]
    #              print(c)
    
    for line in open('.tmp', 'r'):
            if re.search(sn_re, line):
                l = line
                switch_sn = l[8:]
            if re.search(boardtype_re, line):
                l = line
                board_type = l[10:]
            if re.search(manufactured_re, line):
                l = line
                manufactured = l[13:]
            if re.search(vendor_re, line):
                l = line
                vendor = l[11:]
    
    data = {
                        "switch_ip": sw_ip,
                        "switch_sn": switch_sn,
                        "board_type": board_type,
                        "manufactured": manufactured,
                        "vendor": vendor,
                    }
    print(data)
        
        # print(data)
    tablelist.append(data)
df = pd.DataFrame(tablelist)
df.to_excel('output.xlsx', header=True)



jhost.close()
vm.close()