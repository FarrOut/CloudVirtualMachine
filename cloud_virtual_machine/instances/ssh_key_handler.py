import boto3
import logging
import os

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


# Create and configure logger
logging.basicConfig(filename="send_ssh_key.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)



def generate_public_key() -> str:
    logger.info('Generating SSH Public key...')

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    logger.info('Writing pulic SSH key to file...')
    filename = "temp_key.pub"
    file = open(filename, 'w')
    file.write(str(public_key,'utf-8'))
    file.close()

    key_path = os.path.abspath(filename)
    logger.info('Generated public SSH key: ' + key_path)

    return key_path
    # Credits:
    # https://stackoverflow.com/a/39126754


instance_connect = boto3.client('ec2-instance-connect')
