from app.src.domain.file_type import FileType
from app.src.infrastructure.filesystem.csv_file_reader import CsvFileReader
from app.src.infrastructure.filesystem.money_manager_file_reader import MoneyManagerFileReader
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader


class FileReaderFactory:

    @staticmethod
    def get_reader(file_type: FileType) -> TransactionsFileReader:
        if file_type == FileType.DEFAULT:
            return CsvFileReader()

        if file_type == FileType.MONEY_MANAGER_APP:
            return MoneyManagerFileReader()
