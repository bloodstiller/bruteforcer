

# Web Application Brute Forcer for Tomcat and Jenkins

This Python script is crafted to conduct credential brute-forcing attacks on web applications such as Tomcat's manager or host-manager pages, and Jenkins. It attempts authentication using combinations of usernames and passwords from provided files.

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

Provide the script with the target's URL, the application path (for Tomcat's either `/manager` or `/host-manager` for Jenkins `/login`), and the paths to your username and password lists. A proxy is optional.

`python bruteforcer.py -U <URL> -P <Path> -u <UsernamesFile> -p <PasswordsFile> [--proxy <ProxyAddress>]`

#### Arguments

    -U, --url: The URL to the target Tomcat page.
    -P, --path: The path to the manager,host-manager or login on the target site.
    -u, --usernames: The file containing the list of usernames to attempt.
    -p, --passwords: The file containing the list of passwords to attempt.
    --proxy: (Optional) The proxy address to route traffic through, e.g., http://127.0.0.1:8080.

### Example
- **Tomcat**:
  - `python bruteforcer.py -U http://example.com -P /manager -u usernames.txt -p passwords.txt --proxy http://127.0.0.1:8080`
- **Jenkins**:
  - `python bruteforcer.py -U http://example.com:8000 -P /login -u usernames.txt -p passwords.txt --proxy http://127.0.0.1:8080`


## Disclaimer

This tool is intended for security research and penetration testing activities. Use it only on systems you have permission to test. Unauthorized access to computer systems is illegal and punishable by law.
License

## TODO 
- [ ] Allow users to add headers from file. 
- [ ] Improve logic for success/failure.
- [ ] Improve way to pass additional POST arguments

This project is open-source and available under the MIT License.

