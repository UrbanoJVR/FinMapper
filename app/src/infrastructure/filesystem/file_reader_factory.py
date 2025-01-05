from app.src.domain.file_type import FileType
from app.src.infrastructure.filesystem.csv_file_reader import CsvFileReader
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader


class FileReaderFactory:

    @staticmethod
    def get_reader(file_type: FileType) -> TransactionsFileReader:
        if file_type == FileType.DEFAULT:
            return CsvFileReader()
