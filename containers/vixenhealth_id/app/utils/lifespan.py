import contextlib

from storages.cdn.cdn import init_minio
from storages.database.database import get_session
from utils.seeder import run_seeder

get_session_contextmanager = contextlib.asynccontextmanager(get_session)


@contextlib.asynccontextmanager
async def lifespan(_):
    init_minio()
    async with get_session_contextmanager() as sess:
        await run_seeder("deployment/seeder.yaml", sess)
    yield
