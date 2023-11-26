import typer, sys

app = typer.Typer()
class UnixFilesystem_:
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
        links_count,
        blocks,  
        block_size,
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

    @app.command()
    def write(self,
        fp: typer.Option(None, "--file", "-f"),
    ):
        while fp.readable():
            """
            Writes the UFS data structure to a binary file.

            Parameters:
            fp (file object): The file object to write to.
            """
            fp.write(self.inode.to_bytes(8, "big"))
            fp.write(self.pathname.encode('utf-8'))
            fp.write(self.filetype.encode('utf-8'))
            fp.write(self.permissions.to_bytes(8, "big"))
            fp.write(self.owner.to_bytes(8, "big"))
            fp.write(self.group_id.to_bytes(8, "big"))
            fp.write(self.PID.to_bytes(8, "big"))
            fp.write(self.unit_file.encode('utf-8'))
            fp.write(self.unit_file_addr.encode('utf-8'))
            fp.write(self.size.to_bytes(8, "big"))
            fp.write(self.mtime.to_bytes(8, "big"))
            fp.write(self.atime.to_bytes(8, "big"))
            fp.write(self.ctime.to_bytes(8, "big"))
            fp.write(self.links_count.to_bytes(8, "big"))
            fp.write(self.blocks.to_bytes(8, "big"))
            fp.write(self.block_size.to_bytes(8, "big"))

if __name__ == "__main__":
    exit() & exit(app())
