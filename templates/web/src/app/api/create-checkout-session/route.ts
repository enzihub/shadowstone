import { NextResponse } from 'next/server';
import { type NextRequest } from 'next/server';
import Stripe from 'stripe';
import { eq } from 'drizzle-orm';
import { db } from '@/db/db';
import { subscriptions, users } from '@/db/schema';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2024-12-18.acacia',
});

interface RequestBody {
  priceId: string;
  email: string;
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const { priceId, email }: RequestBody = await request.json();

    if (process.env.NEXT_PUBLIC_DEMO_MODE === '1') {
      // Demo mode: no Stripe. Record a 7-day trial in the real database, as the webhook would.
      const [user] = await db.select().from(users).where(eq(users.email, email)).limit(1);
      const now = new Date();
      const trialEnd = new Date(now.getTime() + 7 * 86400000);
      await db
        .insert(subscriptions)
        .values({ id: `sub_demo_${user?.id ?? 'guest'}`, userId: user?.id ?? null, email, status: 'trialing',
          priceId, quantity: 1, trialStart: now, trialEnd, currentPeriodStart: now, currentPeriodEnd: trialEnd })
        .onConflictDoUpdate({ target: subscriptions.id, set: { priceId, status: 'trialing', updatedAt: now } });
      return NextResponse.json({ sessionId: 'cs_demo' });
    }

    const session = await stripe.checkout.sessions.create({
      customer_email: email,
      mode: 'subscription',
      payment_method_collection: 'if_required',
      payment_method_types: ['card'],
      billing_address_collection: 'auto',
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      allow_promotion_codes: true,
      // success_url: `${request.headers.get('origin')}/success?session_id={CHECKOUT_SESSION_ID}`,
      success_url: `${request.headers.get('origin')}/dashboard`,
      cancel_url: `${request.headers.get('origin')}/pricing`,
      ui_mode: 'hosted',
      subscription_data: {
        trial_period_days: 7,
      },
    });

    return NextResponse.json({ sessionId: session.id });
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: 'Error creating checkout session' },
      { status: 500 },
    );
  }
}
