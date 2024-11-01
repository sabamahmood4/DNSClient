#Saba Mahmood
#DNSClient Lab
import dns.resolver

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = '127.0.0.1'  # Localhost for a potential local DNS server
real_name_server = '8.8.8.8'  # Google's public DNS server

# Create a list of domain names to query
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']

# Define a function to query a public DNS server for the IP address of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]  # Use public DNS server IP
    answers = resolver.resolve(domain, question_type)  # Provide domain and question type
    ip_address = answers[0].to_text()  # Extract IP address
    return ip_address

# Define a function to print the results from querying the public DNS server for each domain
def external_DNS_output(question_type):
    print("Public DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)  # Public DNS query
        print(f"The IP address of {domain_name} is {ip_address}")

# Define a function to check consistency of DNS results with the public DNS server
def compare_dns_servers(domainList, question_type):
    public_ip_addresses = {}
    for domain_name in domainList:
        public_ip_address = query_dns_server(domain_name, question_type)
        public_ip_addresses[domain_name] = public_ip_address
    return public_ip_addresses

# Testing function for part 2
def exfiltrate_info(domain, question_type):
    data = query_dns_server(domain, question_type)
    return data

if __name__ == '__main__':
    # Define the query type
    question_type = 'A'

    # Call the function to print results from the public DNS server
    external_DNS_output(question_type)

    # Get consistency of DNS results and print the results
    dns_results = compare_dns_servers(domainList, question_type)
    print("\nDNS results from the public server for all domains:")
    for domain, ip in dns_results.items():
        print(f"{domain}: {ip}")

    # Test exfiltrate_info function
    exfiltrated_data = exfiltrate_info('nyu.edu.', question_type)
    print(f"\nExfiltrated data for 'nyu.edu.': {exfiltrated_data}")
