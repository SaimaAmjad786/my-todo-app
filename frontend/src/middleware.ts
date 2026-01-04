import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const publicPaths = ["/signin", "/signup", "/"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if the path is public
  const isPublicPath = publicPaths.some((path) => pathname === path);

  // For protected routes, we rely on client-side auth context
  // Server-side token validation would require additional setup
  // The AuthProvider will redirect unauthenticated users

  if (pathname.startsWith("/dashboard") || pathname.startsWith("/api")) {
    // These paths require authentication - handled by client
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
