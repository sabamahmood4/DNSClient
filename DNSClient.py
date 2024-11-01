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
                # Return all MX records as a single comma-separated string
                return ", ".join(f"{r.preference} {r.exchange.to_text()}" for r in answers)
            else:
                return answers[0].to_text()
        except dns.resolver.LifetimeTimeout:
            print(f"Timeout on attempt {attempt + 1} for {domain} using local DNS.")

    # If retries are exhausted, fallback to `dig` for this query
    print(f"Falling back to `dig` for {domain}")
    return dig_query(domain)


# Query the public DNS server for the IP address or MX record of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]
    answers = resolver.resolve(domain, question_type)
    if question_type == 'MX':
        # Return all MX records as a single comma-separated string
        return ", ".join(f"{r.preference} {r.exchange.to_text()}" for r in answers)
    else:
        return answers[0].to_text()


# Compare results from the local and public DNS servers for each domain
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)
        if local_ip_address != public_ip_address:
            print(f"Mismatch for {domain_name}: Local DNS: {local_ip_address}, Public DNS: {public_ip_address}")
            return False
    return True


# Print results from both local and public DNS servers for each domain name
def local_external_DNS_output(question_type):
    print("Local DNS Server")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        if ip_address is not None:
            print(f"The IP address of {domain_name} is {ip_address}")
        else:
            print(f"No response from local DNS for {domain_name}")

    print("\nPublic DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")


# Testing function
def exfiltrate_info(domain, question_type):
    return query_local_dns_server(domain, question_type)


if __name__ == '__main__':
    # Set the DNS query type
    question_type = 'A'  # Change to 'MX', 'AAAA' as needed for testing

    # Print results from both DNS servers
    local_external_DNS_output(question_type)

    # Compare results from both DNS servers
    comparison_result = compare_dns_servers(domainList, question_type)
    print(f"\nDNS consistency between servers: {comparison_result}")

    # Query local DNS specifically for 'nyu.edu.'
    result = query_local_dns_server('nyu.edu.', question_type)
    print(f"\nResult from local DNS for 'nyu.edu.': {result}")

    # Test exfiltrate_info function for 'nyu.edu.'
    exfiltrated_data = exfiltrate_info('nyu.edu.', question_type)
    print(f"\nExfiltrated data for 'nyu.edu.': {exfiltrated_data}")
