import aerospike

from app.config.config import settings

app_config = settings()

config = {
    'hosts': [(app_config.AEROSPIKE_HOST, app_config.AEROSPIKE_PORT)]
}

client = aerospike.client(config).connect()


def get_aerospike_client():
    return client
