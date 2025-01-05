from dataclasses import dataclass

from werkzeug.datastructures import FileStorage

from app.src.domain.file_type import FileType


@dataclass
class ReadTransactionsFromFileCommand:
    file: FileStorage
    file_type: FileType