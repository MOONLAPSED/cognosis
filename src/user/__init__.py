#! \cognosis\src\user\venv\Scripts\python.exe
# A module for surgical replacement of elements within files of a directory tree,  
# and creating a forked copy in the process.  

# parent dir is '/home/' venv is virtually situated in cognosis `~`` which is synonymous in source-code with `/src/user/*`
# this is not a data dir, but it will have a mirror of the data dir via simlink farm and tillage
# cultivating the underlying filesystem /home/user/ (/home/user/.bashrc, /home/user/cognosis/requirements.txt, etc.) 
# the user dir, orchestrated by this __init__ and the runtime application, is /home/user/cognosis/src/user/ in source-code, and /home/user/cognosis/ in the filesystem
# Forked Copy (cpfs): The creation of a dynamically generated cpfs that serves as a mutable workspace derived from the original file system. 
