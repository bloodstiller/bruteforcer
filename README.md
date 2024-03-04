

# Tomcat Manager/Host-Manager Brute Forcer

This Python script is designed to perform credential brute-forcing attacks against Tomcat's manager or host-manager pages. It systematically attempts to authenticate using combinations of usernames and passwords provided in separate files.

## Features

- Command-line argument parsing for dynamic usage
- Support for custom proxy settings for routing traffic through tools like Burp Suite
- Dynamic progress indicator showing the current attempt
- Efficient handling of username and password lists

## Prerequisites

Before you run the script, ensure you have Python installed on your system along with the following Python libraries:
- `requests`
- `argparse`

You can install the required libraries using pip:


`pip install requests argparse`

### Usage

To use the script, you need to provide it with the URL of the Tomcat page you wish to target, the specific path to either the manager or host-manager, and the file paths for the username and password lists. Optionally, you can specify a proxy.

`python tomcat_bruteforcer.py -U <URL> -P <Path> -u <UsernamesFile> -p <PasswordsFile> [--proxy <ProxyAddress>]`

#### Arguments

    -U, --url: The URL to the target Tomcat page.
    -P, --path: The path to the manager or host-manager on the target site.
    -u, --usernames: The file containing the list of usernames to attempt.
    -p, --passwords: The file containing the list of passwords to attempt.
    --proxy: (Optional) The proxy address to route traffic through, e.g., http://127.0.0.1:8080.

### Example

`python tomcat_bruteforcer.py -U http://example.com -P /manager -u usernames.txt -p passwords.txt --proxy http://127.0.0.1:8080`

This command will attempt to brute force the login at http://example.com/manager/html using the usernames and passwords listed in usernames.txt and passwords.txt, respectively, routing traffic through the proxy at http://127.0.0.1:8080.

## Disclaimer

This tool is intended for security research and penetration testing activities. Use it only on systems you have permission to test. Unauthorized access to computer systems is illegal and punishable by law.
License

This project is open-source and available under the MIT License.

