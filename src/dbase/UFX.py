import typer
app = typer.Typer()

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
    @staticmethod
    @app.command()
    def write(
        inode: int,
        pathname: str,
        filetype: str,
        permissions: int,
        owner: int,
        group_id: int,
        PID: int,
        unit_file: str,
        unit_file_addr: str,
        size: int,
        mtime: int,
        atime: int,
        ctime: int,
        links_count: int,
        blocks: int,
        block_size: int,
        filename: Optional[str] = typer.Option(None, "--file", "-f"),
    ):
        """
        Writes the UFS data structure to a binary file.
    
        Parameters:
        filename (str, optional): The name of the file to write to.
        """
        ufs = UnixFilesystem(
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
            links_count,
            blocks,
            block_size,
        )
    
        with open(filename, "wb") if filename else sys.stdout.buffer as fp:
            fp.write(ufs.inode.to_bytes(8, "big"))
            fp.write(ufs.pathname.encode('utf-8'))
            fp.write(ufs.filetype.encode('utf-8'))
            fp.write(ufs.permissions.to_bytes(8, "big"))
            fp.write(ufs.owner.to_bytes(8, "big"))
            fp.write(ufs.group_id.to_bytes(8, "big"))
            fp.write(ufs.PID.to_bytes(8, "big"))
            fp.write(ufs.unit_file.encode('utf-8'))
            fp.write(ufs.unit_file_addr.encode('utf-8'))
            fp.write(ufs.size.to_bytes(8, "big"))
            fp.write(ufs.mtime.to_bytes(8, "big"))
            fp.write(ufs.atime.to_bytes(8, "big"))
            fp.write(ufs.ctime.to_bytes(8, "big"))
            fp.write(ufs.links_count.to_bytes(8, "big"))
            fp.write(ufs.blocks.to_bytes(8, "big"))
            fp.write(ufs.block_size.to_bytes(8, "big"))
