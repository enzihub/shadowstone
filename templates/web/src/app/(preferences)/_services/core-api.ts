import { currentUser } from '@clerk/nextjs/server';

const DEFAULT_API_URL = process.env.NEXT_PUBLIC_CORE_API_URL;

type SendToCoreOptions = {
  apiUrl?: string;
};

export const sendToCore = async (
  userToken: string,
  userId: string,
  email: string,
  options: SendToCoreOptions = {},
) => {
  const apiUrl = options.apiUrl || DEFAULT_API_URL;

  const response = await fetch(`${apiUrl}/send-newsletter?email=${encodeURIComponent(email)}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${userToken}`,
    },
    body: JSON.stringify({ userId, email }),
  });

  if (!response.ok) throw new Error(await response.text());
  return response.json();
};
