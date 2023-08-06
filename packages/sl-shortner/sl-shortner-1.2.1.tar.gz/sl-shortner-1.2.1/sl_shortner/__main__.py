import requests
import sys
import os
import time

name = """\033[1;30;40m
___________________________________________________________
\033[1;36;40m  


\033[1;38;40m _  _ ___ _       __  _  _  __  ___ _____ ___ __  _ ___ ___  
\033[1;31;40m| || | _ \ |    /' _/| || |/__\| _ \_   _| __|  \| | __| _ \ 
\033[1;32;40m| \/ | v / |_   `._`.| >< | \/ | v / | | | _|| | ' | _|| v /
\033[1;37;40m \__/|_|_\___|  |___/|_||_|\__/|_|_\ |_| |___|_|\__|___|_|_\ 
 
\033[1;30;40m
 ____________________________________________________________ 
\033[1;31;40m      creat by [÷] shehan lahiru
\033[1;31;40m      git hub [÷]https://github.com/shehan-9909
\033[1;37;40m
"""

# account credentials
username = "shehan9909"
password = "n2NZUJ4L3@knrMV"
print(name, "")
# the URL you want to shorten
url = input("Enter url :-   ")

def main():

# get the access token
    auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
    if auth_res.status_code == 200:
    # if response is OK, get the access token
        access_token = auth_res.content.decode()
        print("[!] successfully sent requests")
    else:
        print("[!] requests not sent, retrying...")
        main()

# construct the request headers with authorization
    headers = {"Authorization": f"Bearer {access_token}"}

# get the group UID associated with our account
    groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
    if groups_res.status_code == 200:
    # if response is OK, get the GUID
        groups_data = groups_res.json()['groups'][0]
        guid = groups_data['guid']
    else:
        print("[!] Cannot get GUID, retrying...")
        main()

# make the POST request to get shortened URL for `url`
    shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": url}, headers=headers)
    if shorten_res.status_code == 200:
    # if response is OK, get the shortened URL
        link = shorten_res.json().get("link")
        print("Shortened URL:", link)
    else:
        print("Try again")
        main()

if __name__ == "__main__":
    main()
