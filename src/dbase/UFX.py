class UnixFilesystem:
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
        ctime,  
        links_count,  # Added
        blocks,  
        block_size,  # Added
    ):

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
        self.ctime = ctime
        self.links_count = links_count
        self.blocks = blocks
        self.block_size = block_size


    def __str__(self):
        """
        Returns a string representation of the UnixFilesystem object.

        Returns:
        str: A string representation of the UnixFilesystem object.
        """
        return f"{self.inode}: {self.pathname}"
