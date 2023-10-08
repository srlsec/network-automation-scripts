from pypsexec.client import Client
import csv

# pip install pypsexec
# pip install python-csv
# reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f

def banner():
    # https://patorjk.com/software/taag/#p=testall&f=Graffiti&t=cobratoxin
    banner="""
  ______ _______ _______  _____  _______ _______ _     _ _______ _______
 |_____/ |______ |  |  | |     |    |    |______  \___/  |______ |      
 |    \_ |______ |  |  | |_____|    |    |______ _/   \_ |______ |_____ v23.06.25                                                                         
 Developed by: Sarathlal_Srl | GitHub: @srlsec                  
        """
    print(banner)

banner()

command = input("Enter the command : ")

with open('hosts.csv', newline='') as csvfile:
 data = csv.DictReader(csvfile)
 for row in data:

    hostname = row['ip']
    user = row['user']
    pas = row['pass']

    print(hostname, user, pas)

    try:
        # c = Client(hostname, username=user, password=pas)
        c = Client(hostname, username=user, password=pas, encrypt=False)

        c.connect()
        try:
            c.create_service()

            if command == 'shutdown':
                stdout, stderr, rc = c.run_executable("cmd.exe", arguments="/c shutdown /s /t 0")
            elif command == 'restart':
                stdout, stderr, rc = c.run_executable("cmd.exe", arguments="/c shutdown /r /t 0")


        finally:
            c.remove_service()
            c.disconnect()
    except:
       pass