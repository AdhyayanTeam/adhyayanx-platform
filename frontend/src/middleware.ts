import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const guestOnlyRoutes = ["/login", "/signup"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasRefreshToken = request.cookies.has("refresh_token");

  if (guestOnlyRoutes.includes(pathname) && hasRefreshToken) {
    return NextResponse.redirect(new URL("/console", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/login", "/signup"],
};
