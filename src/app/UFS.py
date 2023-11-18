from main import Kerneltuple_

# entity --> UFS ... entity --> bridge <-- UFS ... <--entity

class UnixFilesystem(Kerneltuple_):
    """
    The UnixFilesystem class represents a Unix filesystem.

    Attributes:
    inode (int): The inode of the filesystem.
    pathname (str): The pathname of the filesystem.
    filetype (str): The type of the filesystem.
    permissions (str): The permissions of the filesystem.
    owner (str): The owner of the filesystem.
    group_id (str): The group ID of the filesystem.
    PID (int): The PID of the filesystem.
    unit_file (str): The unit file of the filesystem.
    unit_file_addr (str): The address of the unit file.
    size (int): The size of the filesystem.
    mtime (int): The modification time of the filesystem.
    atime (int): The access time of the filesystem.
    """
    def __init__(
        self,
        inode,
        pathname,
        filetype,
        permissions,
        owner,
        group_id,
        PID,
        unit_file,
        unit_file_addr,
        size,
        mtime,
        atime,
    ):
        """
        The constructor for the UnixFilesystem class.

        Parameters:
        inode (int): The inode of the filesystem.
        pathname (str): The pathname of the filesystem.
        filetype (str): The type of the filesystem.
        permissions (str): The permissions of the filesystem.
        owner (str): The owner of the filesystem.
        group_id (str): The group ID of the filesystem.
        PID (int): The PID of the filesystem.
        unit_file (str): The unit file of the filesystem.
        unit_file_addr (str): The address of the unit file.
        size (int): The size of the filesystem.
        mtime (int): The modification time of the filesystem.
        atime (int): The access time of the filesystem.
        """
        super().__init__(Kerneltuple_, "Unix filesystem")
        self.inode = inode
        self.pathname = pathname
        self.filetype = filetype
        self.permissions = permissions
        self.owner = owner
        self.group_id = group_id
        self.PID = PID
        self.unit_file = unit_file
        self.unit_file_addr = unit_file_addr
        self.size = size
        self.mtime = mtime
        self.atime = atime

    def __str__(self):
        """
        Returns a string representation of the UnixFilesystem object.

        Returns:
        str: A string representation of the UnixFilesystem object.
        """
        return f"{self.inode}: {self.pathname}"
