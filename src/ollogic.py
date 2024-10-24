import asyncio
import json
import http.client
import urllib.parse
import pathlib
from pathlib import Path
from typing import Dict, Optional, Set, Tuple, List, Union
from dataclasses import dataclass, field
from array import array
import struct
from struct import calcsize
import math
import time
import importlib.util
import sys
import os

@dataclass
class MemoryCell:
    """Represents a single addressable memory location"""
    value: bytes = b'\x00'  # Initialize with null byte

@dataclass
class MemorySegment:
    """Represents a segment of memory with nominative and intensive characteristics."""
    cells: Dict[int, MemoryCell] = field(default_factory=dict)

    def read(self, address: int) -> bytes:
        """Read a byte from the segment"""
        if address in self.cells:
            return self.cells[address].value
        return b'\x00'  # Default value for uninitialized cells

    def write(self, address: int, value: bytes):
        """Write a byte to the segment"""
        self.cells[address] = MemoryCell(value)

class VirtualMemoryFS:
    """
    Maps a hexadecimal word-addressed virtual memory to filesystem structure.
    Uses 16-bit addressing (0x0000 to 0xFFFF) split into:
    - Upper byte (0x00-0xFF): Directory address
    - Lower byte (0x00-0xFF): File address
    """
    WORD_SIZE = 2  # 16-bit addressing (two bytes)
    CELL_SIZE = 1  # 1 byte per cell
    BASE_DIR = "./app/"
    
    def __init__(self):
        """Initialize the virtual memory filesystem structure"""
        self.base_path = pathlib.Path(self.BASE_DIR)
        self._init_filesystem()
        self._memory_cache: Dict[int, MemoryCell] = {}
        self._segments: Dict[int, MemorySegment] = {addr: MemorySegment() for addr in range(0x100)}  # 256 segments
        
    def _init_filesystem(self):
        """Create the filesystem structure for virtual memory"""
        # Create base directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure (0x00-0xFF)
        for dir_addr in range(0x100):
            dir_path = self.base_path / f"{dir_addr:02x}"
            dir_path.mkdir(exist_ok=True)
            
            # Create __init__.py for the directory
            init_content = f"""
# Auto-generated __init__.py for virtual memory directory 0x{dir_addr:02x}
from dataclasses import dataclass, field
import array

@dataclass
class MemorySegment:
    data: array.array = field(default_factory=lambda: array.array('B', [0] * 256))
"""
            (dir_path / "__init__.py").write_text(init_content)
            
            # Create file structure (0x00-0xFF) within each directory
            for file_addr in range(0x100):
                file_path = dir_path / f"{file_addr:02x}"
                if not file_path.exists():
                    file_path.write_bytes(b'\x00')  # Initialize with null byte
                    
    def _address_to_path(self, address: int) -> pathlib.Path:
        """Convert a 16-bit address to filesystem path"""
        if not 0 <= address <= 0xFFFF:
            raise ValueError(f"Address {address:04x} out of range")
            
        dir_addr = (address >> 8) & 0xFF  # Upper byte
        file_addr = address & 0xFF        # Lower byte
        
        return self.base_path / f"{dir_addr:02x}" / f"{file_addr:02x}"
        
    def read(self, address: int) -> bytes:
        """Read a byte from the specified address"""
        if address in self._memory_cache:
            return self._memory_cache[address].value
            
        path = self._address_to_path(address)
        value = path.read_bytes()
        self._memory_cache[address] = MemoryCell(value)
        return value
        
    def write(self, address: int, value: bytes):
        """Write a byte to the specified address"""
        if len(value) != self.CELL_SIZE:
            raise ValueError(f"Value must be {self.CELL_SIZE} byte")
            
        path = self._address_to_path(address)
        path.write_bytes(value)
        self._memory_cache[address] = MemoryCell(value)

        # Update the corresponding memory segment
        segment_index = (address >> 8) & 0xFF  # Extract the upper byte for segment index
        self._segments[segment_index].write(address & 0xFF, value)  # Write to the segment
        
    def dump_segment(self, start_addr: int, length: int) -> bytes:
        """Dump a segment of memory"""
        result = bytearray()
        for addr in range(start_addr, start_addr + length):
            result.extend(self.read(addr))
        return bytes(result)

@dataclass
class MemoryWavefront:
    """
    Represents the propagating wavefront of memory traversal.
    Tracks both physical state and nominative properties.
    """
    position: int = 0x0000  # Current address position
    visited: Set[int] = field(default_factory=set)
    timestamps: Dict[int, float] = field(default_factory=dict)
    namespace_cache: Dict[str, object] = field(default_factory=dict)

class MemoryHead:
    """
    Manages the propagation of memory access and modification through the virtual
    memory space while maintaining intensive (physical) and nominative (naming) properties.
    """
    def __init__(self, vmem: 'VirtualMemoryFS'):
        self.vmem = vmem
        self.wavefront = MemoryWavefront()
        self.module_cache: Dict[Tuple[int, int], object] = {}
        
    def _load_segment_module(self, segment_addr: int) -> object:
        """
        Dynamically loads the Python module corresponding to a memory segment.
        Creates a namespace bridge between memory and code.
        """
        dir_path = self.vmem.base_path / f"{segment_addr:02x}"
        module_path = dir_path / "__init__.py"
        
        # Check cache first
        cache_key = (segment_addr, module_path.stat().st_mtime)
        if cache_key in self.module_cache:
            return self.module_cache[cache_key]
            
        # Load module dynamically
        spec = importlib.util.spec_from_file_location(
            f"vmem.seg_{segment_addr:02x}",
            module_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        
        # Cache the loaded module
        self.module_cache[cache_key] = module
        return module
        
    def propagate(self, target_addr: int, max_steps: Optional[int] = None) -> List[int]:
        """
        Propagate the wavefront from current position to target address.
        Returns the path of addresses traversed.
        """
        path = []
        steps = 0
        
        while self.wavefront.position != target_addr:
            if max_steps and steps >= max_steps:
                break
                
            # Record current position
            current_addr = self.wavefront.position
            path.append(current_addr)
            
            # Mark as visited with timestamp
            self.wavefront.visited.add(current_addr)
            self.wavefront.timestamps[current_addr] = time.time()
            
            # Load corresponding segment module
            segment_addr = (current_addr >> 8) & 0xFF
            module = self._load_segment_module(segment_addr)
            
            # Create segment instance if needed
            if segment_addr not in self.vmem._segments:
                self.vmem._segments[segment_addr] = module.MemorySegment()
            
            # Determine next position (simple for now, can be made more sophisticated)
            if current_addr < target_addr:
                self.wavefront.position += 1
            else:
                self.wavefront.position -= 1
                
            steps += 1
            
        return path
        
    def read(self, address: int) -> bytes:
        """
        Read from memory while tracking wavefront propagation.
        """
        self.propagate(address)
        return self.vmem.read(address)
        
    def write(self, address: int, value: bytes):
        """
        Write to memory while tracking wavefront propagation.
        """
        self.propagate(address)
        self.vmem.write(address, value)
        
    def get_wavefront_info(self) -> dict:
        """
        Get current state of the wavefront.
        """
        return {
            'position': f"0x{self.wavefront.position:04x}",
            'visited_count': len(self.wavefront.visited),
            'current_segment': f"0x{(self.wavefront.position >> 8):02x}",
            'loaded_modules': len(self.module_cache)
        }

@dataclass
class EmbeddingCell(MemoryCell):
    """Extends MemoryCell to store embeddings and metadata"""
    embedding: Optional[array] = None
    metadata: Dict = field(default_factory=dict)
    
    def serialize(self) -> bytes:
        """Serialize embedding and metadata to bytes"""
        data = {
            'value': self.value.hex(),
            'embedding': list(self.embedding) if self.embedding is not None else None,
            'metadata': self.metadata
        }
        return json.dumps(data).encode()
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'EmbeddingCell':
        """Deserialize bytes back to EmbeddingCell"""
        parsed = json.loads(data)
        cell = cls(bytes.fromhex(parsed['value']))
        if parsed['embedding']:
            cell.embedding = array('f', parsed['embedding'])
        cell.metadata = parsed['metadata']
        return cell

class EmbeddingSegment(MemorySegment):
    """Extends MemorySegment to handle embeddings"""
    def __init__(self):
        super().__init__()
        self.embedding_index: Dict[int, array] = {}
        
    def write(self, address: int, value: bytes, embedding: Optional[array] = None):
        """Write value and optional embedding"""
        cell = EmbeddingCell(value, embedding)
        self.cells[address] = cell
        if embedding is not None:
            self.embedding_index[address] = embedding
            
    def search_similar(self, query_embedding: array, top_k: int = 5) -> List[tuple]:
        """Find most similar embeddings using cosine similarity"""
        if not self.embedding_index:
            return []
            
        def cosine_similarity(a: array, b: array) -> float:
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            return dot_product / (norm_a * norm_b)
            
        similarities = []
        for addr, emb in self.embedding_index.items():
            similarity = cosine_similarity(query_embedding, emb)
            similarities.append((addr, similarity))
            
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]

class InferenceHead(MemoryHead):
    def __init__(self, vmem: 'VirtualMemoryFS', ollama_host: str = "localhost", ollama_port: int = 11434):
        super().__init__(vmem)
        self.ollama_host = ollama_host
        self.ollama_port = ollama_port
        self._init_embedding_segments()

    def _init_embedding_segments(self):
        """Initialize segments as EmbeddingSegments"""
        for addr in range(0x100):
            self.vmem._segments[addr] = EmbeddingSegment()

    async def generate_embedding(self, text: str, model: str = "llama3.1") -> array:
        """Generate embedding using Ollama API"""
        conn = http.client.HTTPConnection(self.ollama_host, self.ollama_port)
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"model": model, "prompt": text})
        
        conn.request("POST", "/api/embeddings", body, headers)
        response = conn.getresponse()
        embedding_data = json.loads(response.read().decode())
        conn.close()
        
        # Convert to standard library array instead of numpy
        return array('f', embedding_data['embedding'])

    async def infer(self, prompt: str, model: str = "llama3.1", context: Optional[List[bytes]] = None) -> str:
        """Run inference using Ollama API with optional context"""
        context_text = ""
        if context:
            context_text = "\n".join([bytes.decode('utf-8', errors='ignore') for bytes in context])
            
        full_prompt = f"{context_text}\n{prompt}" if context_text else prompt
        
        conn = http.client.HTTPConnection(self.ollama_host, self.ollama_port)
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"model": model, "prompt": full_prompt})
        
        conn.request("POST", "/api/generate", body, headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode())
        conn.close()
        
        return result['response']
       
    async def write_with_embedding(self, address: int, value: bytes, text: Optional[str] = None):
        """Write value with automatically generated embedding"""
        if text:
            embedding = await self.generate_embedding(text)
        else:
            embedding = await self.generate_embedding(value.decode('utf-8', errors='ignore'))
            
        segment_addr = (address >> 8) & 0xFF
        segment = self.vmem._segments[segment_addr]
        
        if isinstance(segment, EmbeddingSegment):
            segment.write(address & 0xFF, value, embedding)
        else:
            # Fallback to normal write if segment doesn't support embeddings
            segment.write(address & 0xFF, value)

    async def search_similar_across_segments(self, query_text: str, top_k: int = 5) -> List[tuple]:
        """Search for similar content across all segments"""
        query_embedding = await self.generate_embedding(query_text)
        results = []
        
        for segment_addr, segment in self.vmem._segments.items():
            if isinstance(segment, EmbeddingSegment):
                segment_results = segment.search_similar(query_embedding, top_k)
                results.extend([(segment_addr, addr, sim) for addr, sim in segment_results])
                
        return sorted(results, key=lambda x: x[2], reverse=True)[:top_k]

async def main():
    vmem = VirtualMemoryFS()
    inference_head = InferenceHead(vmem)
    query_count = 0
    max_queries = 10
    # Write some values while tracking propagation
    inference_head.write(0x1234, b'\x42')
    value = inference_head.read(0x1234)
    info = inference_head.get_wavefront_info()
    print(info)    
    test_prompts = [
        "What is memory?",
        "Describe a wave",
        "Tell me about embeddings",
        "How do neural networks work?",
        "Explain quantum computing"
    ]
    for prompt in test_prompts:
        if query_count >= max_queries:
            print(f"Reached maximum query limit of {max_queries}")
            break
        try:
            print(f"\nProcessing prompt: {prompt}")
            await inference_head.write_with_embedding(0x1234 + query_count, b'\x42', prompt)
            results = await inference_head.search_similar_across_segments(prompt)
            print(f"Results for {prompt}: {results}")
            query_count += 2  # Counts as 2 queries (embedding + search)
        except ConnectionRefusedError:
            print(f"Connection to Ollama failed on query {query_count + 1}")
            break
        except Exception as e:
            print(f"Error on query {query_count + 1}: {str(e)}")
            break
    print(f"\nCompleted {query_count} queries to Ollama")
    # Example async operations
    await inference_head.write_with_embedding(0x1234, b'\x42', "test text")
    results = await inference_head.search_similar_across_segments("query text")
    print(results)

if __name__ == "__main__":
    vmem = VirtualMemoryFS()
    # Write some test values
    vmem.write(0x1234, b'\x42')
    vmem.write(0x1235, b'\xFF')
    # Read values back
    print(f"Value at 0x1234: {vmem.read(0x1234).hex()}")
    print(f"Value at 0x1235: {vmem.read(0x1235).hex()}")
    # Dump a memory segment
    print(f"Memory segment 0x1234-0x1236: {vmem.dump_segment(0x1234, 2).hex()}")
    asyncio.run(main())