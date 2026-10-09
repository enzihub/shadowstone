// Calls the FastAPI core. POST /welcome queues a welcome message for this phone number.
export const sendWelcomeMessage = async (phone: string) => {
  const base = process.env.NEXT_PUBLIC_CORE_API_URL;
  if (!base) return { queued: false, reason: 'NEXT_PUBLIC_CORE_API_URL is not set' };
  const res = await fetch(`${base}/welcome`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};
