'use client';
import { Inter } from 'next/font/google';
import localFont from 'next/font/local';
import { dark } from '@clerk/themes';
import './globals.css';
import { GoogleAnalytics, GoogleTagManager } from '@next/third-parties/google';
import Navbar from '@/shared/components/Navbar';
import Footer from '@/shared/components/Footer';
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs';
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});
const geistSans = localFont({
  src: '../../public/fonts/GeistVF.woff',
  variable: '--font-geist-sans',
  weight: '100 900',
});

const geistMono = localFont({
  src: '../../public/fonts/GeistMonoVF.woff',
  variable: '--font-geist-mono',
  weight: '100 900',
});

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          colorPrimary: '#0059FF',
          colorText: 'white',
          colorBackground: '#000000',
          colorTextOnPrimaryBackground: 'white',
          fontFamily: 'var(--font-inter)',
          fontSize: '1rem',
          fontWeight: { normal: 400, medium: 500, bold: 700 },
        },
        layout: {},
        elements: {
          formButtonPrimary:
            'bg-[#0059FF] hover:bg-blue-500 text-xl text-white text-lg font-medium rounded-2xl px-3 py-2 font-sans',
          formFieldErrorText: 'text-red-500 text-sm',
          formFieldLabel: 'text-white text-xl mb-2 hidden font-medium',
          formFieldHintText: 'text-gray-100 text-sm',
          formFieldInput:
            'bg-[#333333] text-white h-[52px] font-normal text-lg font-sans px-3 py-5 rounded-lg w-full',
          formHeaderSubtitle: 'text-white text-2xl font-bold font-display',
          headerTitle: 'text-white text-3xl font-bold font-display',
          headerSubtitle: 'text-base font-medium font-inter mt-2',
          footerText: 'text-white text-sm font-normal font-inter',
          footerActionLink:
            'text-[#0059FF] hover:underline font-bold font-sans',
          footerActionText: 'text-white text-sm font-normal font-inter',
        },
      }}
    >
      <html lang='en'>
        <body
          className={`${geistSans.variable} ${geistMono.variable} ${inter.variable}`}
        >
          <div className='flex min-h-screen flex-col bg-black font-inter'>
            <Navbar />
            <main className='mt-28 flex flex-1 items-center justify-center'>
              {' '}
              {/* Added here for navbar h-16 */}
              {children}
            </main>
            <Footer />
          </div>
          {process.env.NEXT_PUBLIC_GA_ID && (
            <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA_ID} />
          )}
          {process.env.NEXT_PUBLIC_GTM_ID && (
            <GoogleTagManager gtmId={process.env.NEXT_PUBLIC_GTM_ID} />
          )}
        </body>
      </html>
    </ClerkProvider>
  );
}
