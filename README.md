

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

- [ ] 0. Better POST request parameter handling/passing:
    Allow users to pass values with variables as place holders for POST requests e.g loginurl=&username=^USER^&password=^PASS^

- [ ] 1. Dynamic Parameter Handling:

    Allow the script to accept custom data parameters for different forms and authentication mechanisms. This can be achieved by accepting parameters as key-value pairs or a JSON object.

- [ ] 2. Enhanced Authentication Support:

    Add support for various authentication mechanisms such as OAuth, JWT, Basic Auth, etc., making the script versatile across different authentication schemes.

- [ ] 3. Adaptive Request Types:

    Besides GET and POST, consider supporting other HTTP methods like PUT, DELETE, PATCH, etc., as some web applications might use these for authentication or session management.

- [ ] 4. Improved Success and Failure Detection:

    Instead of relying solely on success or failure text, consider checking HTTP status codes, redirection URLs, specific headers, or even the presence/absence of certain HTML elements (requires parsing the response body).

- [ ] 5. Custom Header Support:

    Allow custom headers to be added to requests. This is crucial for applications that use tokens, custom authentication headers, or require specific header configurations.

- [ ] 6. Proxy Rotation and User-Agent Spoofing:

    Implement proxy rotation and user-agent spoofing to avoid detection and blocking by the target application. This helps in mimicking real-world traffic more closely.

- [ ] 7. Timeout and Retry Mechanisms:

    Implement timeouts and automatic retries for requests that fail due to network issues or server errors, making the script more robust in unstable network conditions.

- [ ] 8. Rate Limiting and Throttling:

    Introduce rate limiting or request throttling to avoid overwhelming the target server or triggering anti-scraping mechanisms.

- [ ] 9. Logging and Verbose Output:

    Implement detailed logging for requests and responses, including errors, which can help in debugging and understanding the application's behavior.

- [ ] 10. Session Handling:
- Maintain session persistence across requests if the web application requires it, using session objects or cookies.

- [ ] 11. CSRF Token Handling:
- Fetch and include CSRF tokens in requests if the target web application employs CSRF protection.

- [ ] 12. Multi-threading or Asynchronous Requests:
- Consider implementing multi-threading or asynchronous requests to improve the speed of your brute-forcing efforts, ensuring it's done responsibly to not harm the target server.

- [ ] 13. Captcha Recognition and Handling:
- While defeating CAPTCHA programmatically is against many service terms and can be ethically questionable, being able to detect its presence and pause/notify for manual intervention can be useful.

- [ ] 14. Extensibility and Modular Design:
- Design the script with extensibility in mind, allowing for easy updates and additions of new features or authentication mechanisms.

This project is open-source and available under the MIT License.

