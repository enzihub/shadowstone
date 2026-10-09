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

export default function TermsOfService() {
  const markdownContent = `
# Terms of Service

**Effective date:** [DATE]

> Template text. Replace every [BRACKETED] value and have it reviewed before you go live.

These Terms govern your use of [APP NAME] (the "Service"), run by [COMPANY] ("we").

## 1. Accounts
- You must give accurate information when you sign up and keep your login safe.
- Tell us at [SUPPORT EMAIL] if you think someone else is using your account.

## 2. Plans, trials and billing
- Paid plans renew each month or year until you cancel.
- New accounts may get a free trial. We tell you the length at checkout.
- Payments are processed by Stripe. You can cancel or change your plan from the billing portal.

## 3. Your content
- You keep all rights to the content you add to the Service.
- You let us store and process it only to run the Service for you.

## 4. Acceptable use
Do not misuse the Service, break the law with it, or try to access data that is not yours.

## 5. Third-party services
The Service links to third parties such as sign-in providers and Stripe. Their own terms apply.

## 6. Disclaimer and liability
The Service is provided "as is". To the extent the law allows, we are not liable for indirect or consequential loss.

## 7. Changes
We may update these Terms. We will tell you about material changes before they apply.

## 8. Contact
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
