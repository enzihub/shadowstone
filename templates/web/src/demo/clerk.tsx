'use client';
// Demo stand-in for @clerk/nextjs. Only loaded when NEXT_PUBLIC_DEMO_MODE=1.
import Link from 'next/link';
import React from 'react';
import { DEMO_USER } from './user';

type Props = { children?: React.ReactNode; [key: string]: unknown };

export const ClerkProvider = ({ children }: Props) => <>{children}</>;
export const SignedIn = ({ children }: Props) => <>{children}</>;
export const SignedOut = (_: Props) => null;
export const UserButton = () => (
  <span className='grid h-8 w-8 place-items-center rounded-full bg-violet-600 text-sm text-white'>AP</span>
);
export const UserProfile = () => null;
const Pass = ({ children }: Props) => <Link href='/dashboard'>{children}</Link>;
export const SignInButton = Pass;
export const SignUpButton = Pass;
export const SignOutButton = ({ children }: Props) => <Link href='/login'>{children}</Link>;

function DemoAuthCard({ title }: { title: string }) {
  return (
    <div className='mx-auto mt-8 w-full max-w-md rounded-2xl border border-white/10 bg-white/5 p-8 text-left backdrop-blur-md'>
      <h1 className='font-display text-4xl text-white'>{title}</h1>
      <p className='mt-2 text-gray-300'>Demo mode is on, so Clerk is replaced by a local stand-in.</p>
      <div className='mt-6 rounded-xl bg-white/5 p-4 text-sm text-gray-300'>
        Signed in as <b className='text-white'>{DEMO_USER.fullName}</b> ({DEMO_USER.primaryEmailAddress.emailAddress})
      </div>
      <Link href='/dashboard' className='mt-6 block rounded-2xl bg-[#0059FF] px-3 py-3 text-center text-lg font-medium text-white hover:bg-blue-500'>
        Continue
      </Link>
    </div>
  );
}
export const SignIn = (_: Props) => <DemoAuthCard title='Sign in' />;
export const SignUp = (_: Props) => <DemoAuthCard title='Create your account' />;

export const useUser = () => ({ isLoaded: true, isSignedIn: true, user: DEMO_USER as any });
export const useAuth = () => ({
  isLoaded: true,
  isSignedIn: true,
  userId: DEMO_USER.id,
  sessionId: 'sess_demo',
  getToken: async () => 'demo-token',
});
export const useClerk = () => ({ signOut: async () => { window.location.href = '/login'; } });
