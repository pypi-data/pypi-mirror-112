from abc import ABC
from typing import Optional
from heaobject import root


class FileSystem(root.AbstractDesktopObject, ABC):
    """
    Represents a filesystem, which controls how data is stored and retrieved. In HEA, all filesystems are either
    databases or network file storage.
    """
    pass


class MongoDBFileSystem(FileSystem):
    """
    MongoDB-based filesystem.
    """

    def __init__(self):
        super().__init__()
        self.__connection_string: Optional[str] = None

    @property  # type: ignore
    def connection_string(self) -> Optional[str]:
        """The MongoDB connection string."""
        return self.__connection_string

    @connection_string.setter
    def connection_string(self, connection_string_: Optional[str]):
        self.__connection_string = str(connection_string_) if connection_string_ is not None else None


class Volume(root.AbstractDesktopObject):
    """
    A single accessible storage area that stores a single filesystem. Some volumes may require providing credentials in
    order to access them.
    """
    def __init__(self):
        super().__init__()
        self.__file_system_name: Optional[str] = None
        self.__credentials_id: Optional[str] = None

    @property  # type: ignore
    def file_system_name(self) -> Optional[str]:
        """
        The unique name of this volume's filesystem (a FileSystem object).
        """
        return self.__file_system_name

    @file_system_name.setter  # type: ignore
    def file_system_name(self, file_system_name_: Optional[str]) -> None:
        self.__file_system_name = str(file_system_name_) if file_system_name_ is not None else None

    @property  # type: ignore
    def credentials_id(self) -> Optional[str]:
        """
        The id of this volume's credentials required for access (a Credentials object).
        """
        return self.__credentials_id

    @credentials_id.setter  # type: ignore
    def credentials_id(self, credentials_id_: Optional[str]) -> None:
        self.__credentials_id = str(credentials_id_) if credentials_id_ is not None else None
