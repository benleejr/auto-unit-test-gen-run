//app/layout.tsx
import './globals.css'
import { Inter } from 'next/font/google'
import Head from 'next/head'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <Head>
        <link rel="icon" href="/mcneesefavicon.png" /> 
      </Head>
      <body>{children}</body>
    </html>
  )
}
