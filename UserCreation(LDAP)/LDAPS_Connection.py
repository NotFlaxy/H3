from ldap3 import Server, Connection, Tls, ALL
import ssl

# TLS Configuration
tls_configuration = Tls(validate=ssl.CERT_NONE)

# Server Details
server = Server('10.108.162.69', port=636, use_ssl=True, get_info=ALL, tls=tls_configuration)

try:
    # LDAP Connection
    conn = Connection(server, user='CN=Administrator,CN=Users,DC=monkey,DC=local', password='Kode1234!', auto_bind=True)
    print("Connection established successfully!")
except Exception as e:
    print(f"LDAP connection failed: {e}")