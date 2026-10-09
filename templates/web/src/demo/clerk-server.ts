// Demo stand-in for @clerk/nextjs/server. Only loaded when NEXT_PUBLIC_DEMO_MODE=1.
import { NextResponse, type NextFetchEvent, type NextRequest } from 'next/server';
import { DEMO_USER } from './user';

export type WebhookEvent = { type: string; data: any };

export const auth = async () => ({ userId: DEMO_USER.id, sessionId: 'sess_demo' });
export const currentUser = async () => DEMO_USER as any;

export function createRouteMatcher(patterns: string[]) {
  const res = patterns.map((p) => new RegExp('^' + p + '$'));
  return (req: NextRequest) => res.some((re) => re.test(req.nextUrl.pathname));
}

type Handler = (authFn: typeof auth, req: NextRequest, evt: NextFetchEvent) => Promise<Response | void> | Response | void;

export function clerkMiddleware(handler: Handler) {
  return async (req: NextRequest, evt: NextFetchEvent) => (await handler(auth, req, evt)) ?? NextResponse.next();
}
