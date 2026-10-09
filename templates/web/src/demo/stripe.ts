// Demo stand-in for the Stripe Node SDK. Only loaded when NEXT_PUBLIC_DEMO_MODE=1.
// Plans come from DEMO_STRIPE_PLANS, which `ss create` writes from the tiers you chose.
type Plan = { id: string; product: string; description: string; amount: number; interval: 'month' | 'year' };

function plans(): Plan[] {
  try {
    return JSON.parse(process.env.DEMO_STRIPE_PLANS || '[]');
  } catch {
    return [];
  }
}

function toPrice(p: Plan) {
  return {
    id: p.id,
    object: 'price',
    active: true,
    currency: 'usd',
    unit_amount: p.amount,
    interval: p.interval,
    recurring: { interval: p.interval, interval_count: 1 },
    product: { id: `prod_demo_${p.product.toLowerCase()}`, name: p.product, description: p.description, active: true },
  };
}

class DemoStripe {
  constructor(..._args: unknown[]) {}
  prices = {
    list: async () => ({ data: plans().map(toPrice) }),
    retrieve: async (id: string) => toPrice(plans().find((p) => p.id === id) ?? plans()[0]),
  };
  checkout = { sessions: { create: async () => ({ id: 'cs_demo', url: '/dashboard?checkout=demo' }) } };
  billingPortal = { sessions: { create: async () => ({ url: '/settings?portal=demo' }) } };
  customers = { retrieve: async () => ({ id: 'cus_demo', email: 'ada@example.com' }) };
  subscriptions = { retrieve: async (id: string) => ({ id, status: 'trialing', items: { data: [] } }) };
  webhooks = { constructEvent: () => { throw new Error('Webhooks are disabled in demo mode'); } };
}

export const Stripe = DemoStripe;
export default DemoStripe;
