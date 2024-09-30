// server.ts
import { serve } from "bun";
import { existsSync, readFileSync } from "fs";

// Create a MIME type map for serving different file types
const mimeType: { [key: string]: string } = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".py": "text/python",  // Serve Brython Python code as well
  ".json": "application/json",
};

// Serve files from the dist directory
serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url);
    let path = url.pathname === "/" ? "/index.html" : url.pathname;
    const fullPath = `./dist${path}`;
    
    // If the file exists, serve it
    if (existsSync(fullPath)) {
      const file = readFileSync(fullPath);
      const ext = path.substring(path.lastIndexOf("."));
      const type = mimeType[ext] || "application/octet-stream";
      return new Response(file, { headers: { "Content-Type": type } });
    }

    // Handle not found
    return new Response("Not Found", { status: 404 });
  },
});

console.log("Server running at http://localhost:3000");

// Expose TypeScript functions to the window object
if (typeof window !== "undefined") {
  (window as any).tsFunction = function() {
    const output = document.getElementById("py-output");
    if (output) {
      output.textContent = "Hello from TypeScript 'tsFunction'!";
    }
  };

  (window as any).tsGreet = function() {
    const output = document.getElementById("py-output");
    if (output) {
      output.textContent = "Greetings from TypeScript 'tsGreet'!";
    }
  };
}
