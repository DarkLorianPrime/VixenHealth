import re
import uuid
from datetime import datetime
from typing import Optional, Any

from sqlalchemy import TypeDecorator, String, Dialect
from sqlalchemy.sql.type_api import _T

from storages.cdn.cdn import get_minio

file_type_regex: re.Pattern = re.compile(r"(\.[0-9a-z]+)$")


class File(TypeDecorator):
    cache_ok = True
    impl = String

    def __init__(self, bucket_name: str, is_need_folder: bool = False):
        super().__init__()
        self.bucket_name = bucket_name
        self.is_need_folder = is_need_folder
        self.cdn = get_minio()

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value == "default.png":
            return value

        if not value:
            return

        folder: str = (
            "" if not self.is_need_folder else datetime.now().strftime("%Y%m%d")
        )

        file_name: str = str(uuid.uuid4())
        file_type = file_type_regex.search(value.filename)

        if file_type:
            file_name += file_type.group(0)

        self.cdn.put_object(
            bucket_name=self.bucket_name,
            object_name=f"{folder}/{file_name}",
            data=value.file,
            length=-1,
            part_size=10485760,
        )

        return file_name
