__all__ = ('AerospikeRepository')

from aerospike import exception as ex

from app.datasources.aerospike_db import get_aerospike_client


class AerospikeRepository:
    def __init__(self):
        self.client = get_aerospike_client()
        self.namespace = "test"
        self.set_name = "users"

    def create_user(self, user_id: str, name: str):
        key = (self.namespace, self.set_name, user_id)
        self.client.put(key, {"name": name})
        return {"message": "User created", "user_id": user_id}

    def get_user(self, user_id: str):
        key = (self.namespace, self.set_name, user_id)
        try:
            _, _, record = self.client.get(key)
            return {"user_id": user_id, "data": record}
        except ex.RecordNotFound:
            return None

    def delete_user(self, user_id: str):
        key = (self.namespace, self.set_name, user_id)
        self.client.remove(key)
        return {"message": "User deleted", "user_id": user_id}
