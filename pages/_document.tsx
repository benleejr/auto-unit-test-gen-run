import Document, { Head, Main } from 'next/document'

class MyDocument extends Document {
  render() {
    return (
      <html lang="en">
        <Head>
          <link rel="icon" href="/mcneesefavicon.png" />
        </Head>
        <body>
          <Main />
        </body>
      </html>
    )
  }
}

export default MyDocument