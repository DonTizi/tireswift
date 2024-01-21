import { Inter, Lexend } from 'next/font/google'
import clsx from 'clsx'

import '@/styles/tailwind.css'
import { type Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'


export const metadata: Metadata = {
  title: {
    template: '%s - TireSwift',
    default: 'TireSwift - Optimize your schedule and your income in real time.',
  },
  description:
  "Maintain a real-time schedule to be sure to be available and optimal for your customers, prioritizing being able to make as many places and services available as possible.",
}

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const lexend = Lexend({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-lexend',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
    <html
      lang="en"
      className={clsx(
        'h-full scroll-smooth bg-white antialiased',
        inter.variable,
        lexend.variable,
      )}
    >
      <body className="flex h-full flex-col">{children}</body>
    </html>
    </ClerkProvider>

  )
}
