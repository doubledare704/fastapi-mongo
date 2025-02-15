from fastapi import APIRouter, HTTPException, Depends

from app.repositories.aerospike_repository import AerospikeRepository

router = APIRouter(prefix="/aerospike", tags=["aerospike"])


def get_repository():
    return AerospikeRepository()


@router.post("/user/{user_id}")
def create_user(user_id: str, name: str, repo: AerospikeRepository = Depends(get_repository)):
    return repo.create_user(user_id, name)


@router.get("/user/{user_id}")
def get_user(user_id: str, repo: AerospikeRepository = Depends(get_repository)):
    user = repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/user/{user_id}")
def delete_user(user_id: str, repo: AerospikeRepository = Depends(get_repository)):
    return repo.delete_user(user_id)
