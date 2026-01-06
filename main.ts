import { serve } from "https://deno.land/std@0.140.0/http/server.ts";
import { handleChunks } from "./api/chunks.ts";
import { handleDecode } from "./api/decode.ts";

// Get port from environment (Deno Deploy sets PORT)
const PORT = parseInt(Deno.env.get("PORT") || "8000");

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const path = url.pathname;
  
  // DEBUG: Log untuk development saja
  // console.log(`Request: ${req.method} ${path}`);

  // Relaxed UA check untuk Deno Deploy
  const ua = req.headers.get("user-agent") || "";
  // Allow semua UA di production (kecuali curl yang jelas-jelas manual)
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

// Untuk development, log port
if (Deno.env.get("DENO_DEPLOYMENT_ID")) {
  console.log(`Deno Deploy Server starting on port ${PORT}`);
} else {
  console.log(`Local development server on http://localhost:${PORT}`);
}

// Start server
serve(handler, { port: PORT });
