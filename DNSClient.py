import dns.resolver
import subprocess

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = '209.18.47.63'  # Local DNS server IP
real_name_server = '8.8.8.8'  # Public DNS server IP (Google DNS)

# Create a list of domain names to query
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']

# Helper function to perform a `dig` query as a fallback
def dig_query(domain):
    try:
        result = subprocess.run(['dig', f'@{local_host_ip}', domain, '+short'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error with dig command: {e}")
        return None

# Query the local DNS server with retries and dig fallback for persistent timeouts
def query_local_dns_server(domain, question_type, retries=3):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [local_host_ip]
    resolver.timeout = 10
    resolver.lifetime = 20

    for attempt in range(retries):
        try:
            answers = resolver.resolve(domain, question_type)
            if question_type == 'MX':
                return f"{answers[0].preference} {answers[0].exchange.to_text()}"
            else:
                return answers[0].to_text()
        except dns.resolver.LifetimeTimeout:
            print(f"Timeout on attempt {attempt + 1} for {domain} using local DNS.")
            
    # If retries are exhausted, fallback to `dig` for this query
    print(f"Falling back to `dig` for {domain}")
    return dig_query(domain)

# Query the public DNS server for the I
