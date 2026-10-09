// The invented user every demo session is signed in as.
export const DEMO_USER = {
  id: 'user_demo_ada',
  firstName: 'Ada',
  lastName: 'Park',
  fullName: 'Ada Park',
  imageUrl: '',
  primaryEmailAddress: { emailAddress: 'ada@example.com' },
  emailAddresses: [{ emailAddress: 'ada@example.com' }],
  hasVerifiedEmailAddress: true,
  createdAt: new Date('2025-03-14T09:00:00Z'),
  externalAccounts: [
    { provider: 'google', verification: { strategy: 'oauth_google', status: 'verified' }, destroy: async () => {} },
  ],
  createExternalAccount: async () => ({ verification: { status: 'verified' } }),
};
