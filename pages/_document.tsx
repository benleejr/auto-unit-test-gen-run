import { Document, Metadata } from 'next/document'

class MyDocument extends Document {
  render() {
    return (
      <html lang="en">
        <Metadata>
          <link rel="icon" href="/mcneesefavicon.png" />
        </Metadata>
        <body>
          <Main />
        </body>
      </html>
    )
  }
}

export default MyDocument