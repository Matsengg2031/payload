// Deno Deploy compatible server using Deno.serve()
import { handleChunks } from "./api/chunks.ts";
import { handleDecode } from "./api/decode.ts";

function handler(req: Request): Response | Promise<Response> {
  const url = new URL(req.url);
  const path = url.pathname;

  // Relaxed UA check untuk Deno Deploy
  const ua = req.headers.get("user-agent") || "";
  // Block only obvious manual testing tools
  if (ua.includes("curl") && ua.includes("Deno")) {
      return new Response("Not Found", { status: 404 });
  }

  // Routing
  if (path.startsWith("/api/chunks")) {
    return handleChunks(req);
  }
  
  if (path.startsWith("/api/decode")) {
    return handleDecode(req);
  }

  if (path === "/api/v1/update") {
     // Decoy endpoint
     return new Response(JSON.stringify({ 
         status: "up-to-date", 
         version: "1.0.5",
         timestamp: new Date().toISOString()
     }), {
         headers: { "content-type": "application/json" }
     });
  }

  // Health check endpoint untuk Deno Deploy
  if (path === "/health") {
    return new Response(JSON.stringify({ 
        status: "ok",
        service: "update-server"
    }), {
        headers: { "content-type": "application/json" }
    });
  }

  // Fallback
  return new Response("Service Online", { 
      status: 200,
      headers: { "content-type": "text/plain" }
  });
}

// Use Deno.serve() - the modern, Deno Deploy compatible API
Deno.serve({ port: 8000 }, handler);
