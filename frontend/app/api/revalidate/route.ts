import { revalidatePath as nextRevalidatePath } from "next/cache";
import { NextRequest, NextResponse } from "next/server";

/**
 * API Route para revalidação ISR via webhook do Strapi
 * 
 * Uso: POST /api/revalidate
 * Body: { secret: string, path: string }
 * 
 * Strapi Webhook Configuration:
 * URL: https://aumivet.com.br/api/revalidate
 * Method: POST
 * Body: {"secret": "YOUR_SECRET", "path": "/blog/[slug]"}
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { secret, path } = body;

    // Validar secret
    if (!secret || secret !== process.env.REVALIDATE_SECRET) {
      return NextResponse.json(
        { message: "Invalid secret" },
        { status: 401 }
      );
    }

    // Validar path
    if (!path) {
      return NextResponse.json(
        { message: "Missing path parameter" },
        { status: 400 }
      );
    }

    // Revalidar path específico
    nextRevalidatePath(path);

    return NextResponse.json({
      revalidated: true,
      path,
      now: Date.now(),
    });
  } catch (error) {
    console.error("Revalidation error:", error);
    return NextResponse.json(
      { message: "Error revalidating", error: String(error) },
      { status: 500 }
    );
  }
}

// GET para teste (apenas desenvolvimento)
export async function GET(request: NextRequest) {
  if (process.env.NODE_ENV !== "development") {
    return NextResponse.json(
      { message: "GET method only available in development" },
      { status: 403 }
    );
  }

  const searchParams = request.nextUrl.searchParams;
  const secret = searchParams.get("secret");
  const path = searchParams.get("path") || "/";

  if (!secret || secret !== process.env.REVALIDATE_SECRET) {
    return NextResponse.json(
      { message: "Invalid secret" },
      { status: 401 }
    );
  }

  nextRevalidatePath(path);

  return NextResponse.json({
    revalidated: true,
    path,
    now: Date.now(),
  });
}
