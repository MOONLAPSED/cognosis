import asyncio
import importlib.util
import logging
import os
import shutil
import subprocess
import sys
import venv
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

@dataclass
class RuntimeConfig:
    """Configuration for user runtime environment"""
    user_id: str
    runtime_dir: Path
    packages: List[str] = field(default_factory=list)
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}"
    environment_vars: Dict[str, str] = field(default_factory=dict)

class UserRuntimeManager:
    """Manages isolated user runtime environments with separate dependency management"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.runtimes: Dict[str, RuntimeConfig] = {}
        self.logger = logging.getLogger(__name__)

    def create_runtime(self, config: RuntimeConfig) -> None:
        """Create a new isolated runtime environment for a user"""
        runtime_path = self.base_dir / config.user_id
        
        # Create runtime directory structure
        runtime_path.mkdir(parents=True, exist_ok=True)
        (runtime_path / "src").mkdir(exist_ok=True)
        (runtime_path / "libs").mkdir(exist_ok=True)
        
        # Create virtual environment
        venv.create(runtime_path / "venv", with_pip=True)
        
        # Store runtime configuration
        self.runtimes[config.user_id] = config
        
        # Initialize runtime with base files
        self._initialize_runtime(config)

    def _initialize_runtime(self, config: RuntimeConfig) -> None:
        """Initialize runtime with necessary files and structure"""
        runtime_path = self.base_dir / config.user_id
        
        # Create __init__.py files
        for dir_path in runtime_path.rglob("**/"):
            if dir_path.is_dir() and not (dir_path / "__init__.py").exists():
                (dir_path / "__init__.py").touch()

        # Create runtime launcher
        launcher_path = runtime_path / "launcher.py"
        launcher_content = """
import asyncio
import importlib.util
import sys
from pathlib import Path

async def launch_user_main():
    try:
        # Add user's lib directory to path
        user_lib_path = Path(__file__).parent / "libs"
        sys.path.insert(0, str(user_lib_path))
        
        # Import user's main module
        spec = importlib.util.spec_from_file_location(
            "user_main", 
            Path(__file__).parent / "src" / "main.py"
        )
        if spec and spec.loader:
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)
            
            if hasattr(user_module, 'main'):
                await user_module.main()
            else:
                print("No main function found in user module")
    except Exception as e:
        print(f"Error in user runtime: {e}")

if __name__ == "__main__":
    asyncio.run(launch_user_main())
"""
        launcher_path.write_text(launcher_content)

    @contextmanager
    def runtime_context(self, user_id: str):
        """Context manager for executing code within a user's runtime environment"""
        if user_id not in self.runtimes:
            raise ValueError(f"No runtime found for user {user_id}")
            
        config = self.runtimes[user_id]
        runtime_path = self.base_dir / user_id
        
        # Store original sys.path
        original_path = sys.path.copy()
        original_env = os.environ.copy()
        
        try:
            # Modify Python path to include user's libraries
            sys.path.insert(0, str(runtime_path / "libs"))
            
            # Set environment variables
            os.environ.update(config.environment_vars)
            
            yield runtime_path
            
        finally:
            # Restore original state
            sys.path = original_path
            os.environ = original_env

    async def install_packages(self, user_id: str, packages: List[str]) -> bool:
        """Install packages in the user's runtime environment"""
        if user_id not in self.runtimes:
            raise ValueError(f"No runtime found for user {user_id}")
            
        config = self.runtimes[user_id]
        runtime_path = self.base_dir / user_id
        venv_pip = runtime_path / "venv" / "bin" / "pip"
        
        try:
            for package in packages:
                self.logger.info(f"Installing {package} for user {user_id}")
                process = await asyncio.create_subprocess_exec(
                    str(venv_pip),
                    "install",
                    package,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    self.logger.error(f"Failed to install {package}: {stderr.decode()}")
                    return False
                    
            # Update runtime configuration
            config.packages.extend(packages)
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing packages: {e}")
            return False

    async def execute_user_code(self, user_id: str, code: str) -> Any:
        """Execute code in user's runtime environment"""
        if user_id not in self.runtimes:
            raise ValueError(f"No runtime found for user {user_id}")
            
        with self.runtime_context(user_id) as runtime_path:
            try:
                # Create a temporary module for execution
                module_name = f"user_code_{user_id}"
                spec = importlib.util.spec_from_loader(module_name, loader=None)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    exec(code, module.__dict__)
                    
                    # If there's an async main function, run it
                    if hasattr(module, 'main') and asyncio.iscoroutinefunction(module.main):
                        return await module.main()
                    return None
                    
            except Exception as e:
                self.logger.error(f"Error executing user code: {e}")
                raise

    def cleanup_runtime(self, user_id: str) -> None:
        """Clean up a user's runtime environment"""
        if user_id not in self.runtimes:
            return
            
        runtime_path = self.base_dir / user_id
        try:
            shutil.rmtree(runtime_path)
            del self.runtimes[user_id]
        except Exception as e:
            self.logger.error(f"Error cleaning up runtime: {e}")

# Example usage
async def main():
    # Create runtime manager
    manager = UserRuntimeManager(Path("./user_runtimes"))
    
    # Create a runtime for a user
    config = RuntimeConfig(
        user_id="user123",
        runtime_dir=Path("./user_runtimes/user123"),
        packages=["requests", "pandas"],
        environment_vars={"USER_ENV": "development"}
    )
    
    manager.create_runtime(config)
    
    # Install some packages
    await manager.install_packages("user123", ["numpy", "scipy"])
    
    # Execute some user code
    user_code = """
import numpy as np

async def main():
    arr = np.array([1, 2, 3])
    return arr.mean()
"""
    
    result = await manager.execute_user_code("user123", user_code)
    print(f"Execution result: {result}")
    
    # Clean up
    manager.cleanup_runtime("user123")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())