import dns.resolver

# Set the IP address of a public DNS server
real_name_server = '8.8.8.8'  # Google public DNS server

# Create a list of domain names to query - use the same list from the DNS Server
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']

# Define a function to query the public DNS server for the IP address or MX record of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]  # Use public DNS server IP
    answers = resolver.resolve(domain, question_type)  # Provide the domain and question type
    
    if question_type == 'MX':
        # Return MX records in "preference hostname" format as a single string
        return ", ".join(f"{r.preference} {r.exchange.to_text()}" for r in answers)
    else:
        # For A, AAAA, or other records, return the result as a single string
        return ", ".join(answer.to_text() for answer in answers)

# Define a function to print the results from querying the public DNS server for each domain name
def external_DNS_output(question_type):    
    print("Public DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

# Define a function to compare the results with the public DNS server
def compare_dns_servers(domainList, question_type):
    public_ip_addresses = {}
    for domain_name in domainList:
        public_ip_address = query_dns_server(domain_name, question_type)
        public_ip_addresses[domain_name] = public_ip_address
    return public_ip_addresses

# Define a testing function for part 2
def exfiltrate_info(domain, question_type):
    data = query_dns_server(domain, question_type)
    return data

if __name__ == '__main__':
    # Set the type of DNS query to be performed
    question_type = 'A'  # Change to 'MX', 'AAAA' (IPv6), etc., based on test requirements

    # Call the function to print results from the public DNS server
    external_DNS_output(question_type)

    # Get consistency of DNS results and print the results
    dns_results = compare_dns_servers(domainList, question_type)
    print("\nDNS results from the public server for all domains:")
    for domain, ip in dns_results.items():
        print(f"{domain}: {ip}")

    # Test exfiltrate_info function for 'nyu.edu.'
    exfiltrated_data = exfiltrate_info('nyu.edu.', question_type)
    print(f"\nExfiltrated data for 'nyu.edu.': {exfiltrated_data}")
