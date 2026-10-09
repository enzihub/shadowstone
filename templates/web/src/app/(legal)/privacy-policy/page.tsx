import React from 'react';
import ReactMarkdown from 'react-markdown';

const markdownComponents = {
  h1: ({ children }: any) => (
    <h1 className='mb-8 text-center text-3xl font-medium tracking-tight text-gray-100 md:text-4xl'>
      {children}
    </h1>
  ),
  h2: ({ children }: any) => (
    <h2 className='mb-4 border-b border-gray-700 pb-2 text-xl font-medium tracking-tight text-gray-200 md:text-2xl'>
      {children}
    </h2>
  ),
  h3: ({ children }: any) => (
    <h3 className='mb-3 text-lg font-medium tracking-tight text-gray-300 md:text-xl'>
      {children}
    </h3>
  ),
  p: ({ children }: any) => (
    <p className='mb-6 text-sm leading-relaxed text-gray-400 md:text-base'>
      {children}
    </p>
  ),
  ul: ({ children }: any) => (
    <ul className='mb-6 ml-4 list-outside list-disc text-sm text-gray-400 md:text-base'>
      {children}
    </ul>
  ),
  ol: ({ children }: any) => (
    <ol className='mb-6 ml-4 list-outside list-decimal text-sm text-gray-400 md:text-base'>
      {children}
    </ol>
  ),
  li: ({ children }: any) => <li className='mb-2'>{children}</li>,
  hr: () => <hr className='my-8 border-gray-700' />,
};

export default function PrivacyPolicy() {
  const markdownContent = `
# Privacy Policy

**Effective date:** [DATE]

> Template text. Replace every [BRACKETED] value and have it reviewed before you go live.

This policy explains what [APP NAME] collects and why.

## 1. What we collect
- **Account data:** name, email address and profile picture from your sign-in provider.
- **Preferences:** the details you add in Settings, such as a phone number and time zone.
- **Billing data:** handled by Stripe. We store your Stripe customer and subscription ids, not card numbers.
- **Usage data:** basic logs such as browser type and timestamps.

## 2. How we use it
To run the Service, send the messages you ask for, handle billing and keep the Service secure.

## 3. Who we share it with
Service providers that run parts of the Service (authentication, payments, hosting, email). We do not sell personal data.

## 4. Retention and your rights
We keep data while your account is open. You can ask for a copy, a correction or deletion at [SUPPORT EMAIL].

## 5. Contact
[COMPANY] · [ADDRESS] · [SUPPORT EMAIL]
  `;

  return (
    <div className='w-full bg-black'>
      <div className='mx-auto max-w-3xl px-4 md:px-6'>
        <div className='mb-16 mt-16 rounded-lg'>
          <div className='scrollbar-thin scrollbar-thumb-gray-700 hover:scrollbar-thumb-gray-600 scrollbar-track-transparent overflow-y-auto px-6 py-8 md:px-8'>
            <div className='prose prose-invert max-w-none'>
              <ReactMarkdown components={markdownComponents}>
                {markdownContent}
              </ReactMarkdown>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
