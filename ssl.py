from OpenSSL import crypto
from datetime import datetime, timedelta
import os

def generate_ssl_cert_and_key(certfile, keyfile, days=365, bits=2048):
    # Generate a new private key
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, bits)

    # Generate a self-signed certificate
    cert = crypto.X509()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(days * 24 * 60 * 60)  # Valid for specified days
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    # Write the certificate and key to files
    with open(certfile, 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(keyfile, 'wb') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

# Example usage
if __name__ == "__main__":
    #if you dont find ssl files then
    folder = './'
    files = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    if 'scc.cert' not in files or 'scc.key' not in files:
        generate_ssl_cert_and_key('scc.cert', 'scc.key')

