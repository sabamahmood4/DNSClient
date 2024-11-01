import dns.resolver

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = '127.0.0.1'  # Localhost IP for the local DNS server
real_name_server = '8.8.8.8'  # Google public DNS server

# Create a list of domain names to query - use the same list from the DNS Server
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']

# Define a function to query the local DNS server for the IP address of a given domain name
def query_local_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [local_host_ip]  # Use local DNS server IP
    answers = resolver.resolve(domain, question_type)  # Provide the domain and question type
    ip_address = answers[0].to_text()  # Extract IP address from the first answer record
    return ip_address

# Define a function to query a public DNS server for the IP address of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]  # Use public DNS server IP
    answers = resolver.resolve(domain, question_type)  # Provide the domain and question type
    ip_address = answers[0].to_text()  # Extract IP address from the first answer record
    return ip_address

# Define a function to compare the results from the local and public DNS servers for each domain name in the list
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)
        if local_ip_address != public_ip_address:
            return False
    return True

# Define a function to print the results from querying both the local and public DNS servers for each domain name in the domainList
def local_external_DNS_output(question_type):    
    print("Local DNS Server")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

    print("\nPublic DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

# Testing method for part 2
def exfiltrate_info(domain, question_type):
    data = query_local_dns_server(domain, question_type)
    return data

if __name__ == '__main__':
    
    # Set the type of DNS query to be performed
    question_type = 'A'  # 'A' record for IPv4 addresses

    # Call the function to print the results from querying both DNS servers
    local_external_DNS_output(question_type)
    
    # Call the function to compare the results from both DNS servers and print the result
    comparison_result = compare_dns_servers(domainList, question_type)
    print(f"\nDNS consistency between servers for all domains: {comparison_result}")

    # Query the local DNS server specifically for 'nyu.edu.'
    result = query_local_dns_server('nyu.edu.', question_type)
    print(f"\nResult from local DNS for 'nyu.edu.': {result}")

    # Test exfiltrate_info function for 'nyu.edu.'
    exfiltrated_data = exfiltrate_info('nyu.edu.', question_type)
    print(f"\nExfiltrated data for 'nyu.edu.': {exfiltrated_data}")
