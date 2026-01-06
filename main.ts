import { serve } from "https://deno.land/std@0.140.0/http/server.ts";
import { handleChunks } from "./api/chunks.ts";
import { handleDecode } from "./api/decode.ts";

function handler(req: Request): Promise<Response> | Response {
  const url = new URL(req.url);
  const path = url.pathname;
  console.log(`[DEBUG] Request received: ${req.method} ${path}`);

  // 1. Anti-Analysis: Fake Delay (Reduced for local test)
  // const delay = Math.floor(Math.random() * 400) + 100;
  // await new Promise(resolve => setTimeout(resolve, delay));


  // 2. Anti-Analysis: Header Check
  // In a real scenario, use more subtle checks.
  const ua = req.headers.get("user-agent") || "";
  console.log(`[DEBUG] UA: ${ua}`); // Log UA for debugging

  // Relaxed check for testing: Allow python-requests
  if (ua.includes("curl")) { 
      return new Response("Not Found", { status: 404 });
  }

  // 3. Routing
  if (path.startsWith("/api/chunks")) {
    return handleChunks(req);
  }
  
  if (path.startsWith("/api/decode")) {
    return handleDecode(req);
  }

  if (path === "/api/v1/update") {
     // Decoy endpoint
     return new Response(JSON.stringify({ status: "up-to-date", version: "1.0.5" }), {
         headers: { "content-type": "application/json" }
     });
  }

  // Fallback to static serving for public (if any) or 404
  return new Response("Not Found", { status: 404 });
}

console.log("Listening on http://localhost:8000");
serve(handler);
