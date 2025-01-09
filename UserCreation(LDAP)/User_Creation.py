import csv
import random
import string
import logging
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# Configuration
AD_SERVER = 'ldap://10.108.162.64'
AD_USER = 'CN=Administrator,CN=Users,DC=monkey,DC=local'
AD_PASSWORD = 'Kode1234!'
BASE_DN = 'CN=Users,DC=monkey,DC=local'
LOG_FILE = 'UserCreation(LDAP)\\ad_user_log.txt'

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to generate a readable random password
def generate_password(length=12):
    # Define the character sets for readability
    letters = string.ascii_letters  # Uppercase and lowercase letters
    digits = string.digits          # Numbers
    symbols = "!@#$%&*"             # A small set of special characters

    # Ensure the password includes at least one of each type
    all_characters = random.choice(letters) + random.choice(digits) + random.choice(symbols)
    # Fill the rest of the password with a mix of readable characters
    all_characters += ''.join(random.choice(letters + digits) for _ in range(length - 3))

    # Shuffle to make the password random
    password = ''.join(random.sample(all_characters, len(all_characters)))
    return password

# Function to generate an anonymized username
def anonymize_username(first_name, last_name):
    return f"user_{first_name[0].lower()}{last_name[0].lower()}{random.randint(1000, 9999)}"

# Function to add a user to the Active Directory
def add_user_to_ad(connection, username, first_name, last_name, full_name, initials, password):
    dn = f"CN={username},{BASE_DN}"
    attributes = {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        'cn': username,
        'sn': last_name,
        'givenName': first_name,
        'displayName': full_name,
        'initials': initials,
        'userPrincipalName': f"{username}@monkey.local",
        'sAMAccountName': username,
    }
    connection.add(dn, attributes=attributes)
    if not connection.result['description'] == 'success':
        raise Exception(f"Failed to add user {username}: {connection.result['message']}")

    # Enable account and set password
    connection.extend.microsoft.modify_password(dn, password)
    connection.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, [512])]})  # Enable account
    return True

# Main function
def main():
    # Connect to the AD server
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)

    # Read users from the CSV file
    with open('.\\UserCreation(LDAP)\\users.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row['FirstName']
            last_name = row['LastName']
            full_name = row['FullName']
            initials = row['Initials']
            username = anonymize_username(first_name, last_name)
            password = generate_password()

            try:
                add_user_to_ad(conn, username, first_name, last_name, full_name, initials, password)
                logging.info(f"Anonymized User {username} (Original: {full_name}) added successfully with password: {password}")
                print(f"Added user: {username} (Original: {full_name})")
            except Exception as e:
                logging.error(f"Failed to add user {full_name}: {e}")
                print(f"Failed to add user {full_name}: {e}")

    conn.unbind()

if __name__ == '__main__':
    main()