import boto3
import logging
import os

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

# Create and configure logger
logging.basicConfig(filename="send_ssh_key.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


def generate_key_pair() -> str:
    logger.info('Generating SSH key-pair...')

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=4096
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    logger.info('Writing private SSH key to file...')
    priv_filename = "temp_key.pem"
    file = open(priv_filename, 'w')
    file.write(str(private_key, 'utf-8'))
    file.close()

    priv_key_path = os.path.abspath(priv_filename)
    logger.info('Generated private SSH key: ' + priv_key_path)

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    logger.info('Writing public SSH key to file...')
    pub_filename = "temp_key.pub"
    file = open(pub_filename, 'w')
    file.write(str(public_key, 'utf-8'))
    file.close()

    pub_key_path = os.path.abspath(pub_filename)
    logger.info('Generated public SSH key: ' + pub_key_path)

    return pub_key_path, priv_key_path
    # Credits:
    # https://stackoverflow.com/a/39126754


instance_connect = boto3.client('ec2-instance-connect')
