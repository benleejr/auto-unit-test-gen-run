// components/Layout.tsx
import React, { ReactNode } from 'react';
import Head from 'next/head';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      <Head>
        <title>Unit Test Generator and Runner</title>
        <link rel="icon" href="/mcneesefavicon.png" /> 
      </Head>
      <div className="w-full bg-blue-500 text-white text-center py-4 mb-8">
        <h1 style={{fontSize: '1.5em'}}>Automatic Unit Test Generator and Runner</h1>
      </div>
      {children}
    </>
  );
};

export default Layout;