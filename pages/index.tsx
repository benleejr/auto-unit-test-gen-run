//app/page.tsx
"use client"
import React, { useState } from 'react';
import axios from 'axios';
import { LinearProgress, CircularProgress } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import Head from 'next/head'
import Layout from '../components/Layout';

const Home = () => {
  const [apiKey, setApiKey] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [pdfLink, setPdfLink] = useState('');
  const [zipLink, setZipLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [pdfLoaded, setPdfLoaded] = useState(false);

  const [selectedFileNames, setSelectedFileNames] = useState<string[]>([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: '.py' as any,
    onDrop: (acceptedFiles: File[]) => {
      setFiles(acceptedFiles);
      const fileNames = acceptedFiles.map(file => file.name);
      setSelectedFileNames(fileNames);
    }
  });

  async function handleGenerateClick() {
    setLoading(true);
    if (!files) {
      alert('Please upload a file first.');
      setLoading(false);
      return;
    }
    setPdfLink('');
    setPdfLoaded(false);

    const uploadPromises = [];
    const url = process.env.NODE_ENV === 'production' ? 'https://auto-unit-test-gen-run.vercel.app/api/upload' : 'http://127.0.0.1:8000/api/upload';

    for (let i = 0; i < files.length; i++) {
      if (files[i].name.endsWith('.py')) {
        const uploadPromise = new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = function(e: any) {
            const content = e.target.result;
            axios.post(url, { file_content: content, file_name: files[i].name, api_key: apiKey }, {
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then(resolve)  // Resolve the Promise when upload is done
            .catch(reject); // Reject the Promise on error
          };
          reader.readAsText(files[i]);
        });

        uploadPromises.push(uploadPromise);
      }
    }

    // Wait for all uploads to complete
    await Promise.all(uploadPromises);

    // Now make the run_tests request
    const fileName = files[0].name
    const reader = new FileReader();
    reader.onload = async function(e: any) {
      const content = e.target.result;
      const runTestsUrl = process.env.NODE_ENV === 'production' ? 'https://auto-unit-test-gen-run.vercel.app/api/run_tests' : 'http://127.0.0.1:8000/api/run_tests';

      let response = await fetch(runTestsUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        //body: JSON.stringify({ file_content: content, file_name: fileName }),
      });

      console.log(response);

      const result = await response.json();

      if (result.path) {
        setPdfLink(`/reports/${result.path}`);
      }

      if(result.zip) {
        setZipLink(`/output/${result.zip}`);
      }
    };

    reader.readAsText(files[0]);
  }

  return (
    <Layout>
    
    <main className="flex min-h-screen p-5">
      <div className="flex flex-col w-1/4 p-4 justify-center align-top">
        {/* Instructions */}
        <div>
          <h1 style={{fontSize: '2em', fontWeight: 'bold'}}>How to Use:</h1>
          <div style={{ height: '20px' }}></div>
          <ol>
            <li>1. Input your API key from OpenAI into the textbox labelled: &apos;OpenAI API Key&apos;.</li>
            <li>2. Drag and drop or click the icon and select the files or folder that you would like to have unit tests generated for.</li>
            <li>3. After the relevant files have been uploaded, click on &apos;Run Tests &amp; Generate PDF&apos;.</li>
          </ol>
        </div>

        <div style={{ height: '20px' }}></div>

        {/* API Key Input */}
        <div>
          <label htmlFor="apiKey" style={{fontWeight: 'bold'}}>OpenAI API Key:</label>
          <input
            type="password"
            id="apiKey" 
            placeholder="Enter OpenAI API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="mt-1 p-2 border rounded"
          />
        </div>

        <div style={{ height: '20px' }}></div>

        {/* Display Selected File Names */}
        <div>
          {selectedFileNames.length > 0 && (
            <div>
              <strong>Selected Files:</strong>
              <ul>
                {selectedFileNames.map((name, index) => (
                  <li key={index}>{name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        
        {/*Drag and Drop Box*/}
        <div {...getRootProps()} style={{ border: '2px solid black', padding: '20px', borderRadius: '5px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', marginBottom: '20px', cursor: 'pointer' }}>
          <input {...getInputProps()} />
          <i className="upload-icon" style={{fontSize: '50px'}}>📤</i>
          <p>Upload</p>
        </div>

        {/*Run Program*/}
        <button onClick={handleGenerateClick} className="uploadButton" style={{
          padding: '10px 15px',
          backgroundColor: '#007BFF',
          color: '#FFF',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          display: 'inline-block',
          marginBottom: '10px',
          transition: 'background-color 0.3s ease',
          }}>
          Run Tests &amp; Generate PDF
        </button>

        {/* Animated Status Bar */}
        {loading && !pdfLoaded && <LinearProgress className="w-1/2" style={{
          width: '100%',
          height: '5px',
        }}
        />}

        {/* Download Button */}
        {zipLink && (
            <button
              className="uploadButton"
              onClick={() => window.open(`${process.env.NODE_ENV === 'production' ? 'https://auto-unit-test-gen-run.vercel.app/' : 'http://127.0.0.1:3000/'}${zipLink}`, '_blank')}
              style={{
                padding: '10px 15px',
                backgroundColor: '#007BFF',
                color: '#FFF',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'inline-block',
                marginBottom: '10px',
                transition: 'background-color 0.3s ease',
              }}
            >
              Download Results
            </button>
          )}
      </div>

      {/* Right Side: PDF Viewer */}
      {loading && pdfLoaded ? (
          <div className="flex items-center justify-end align-top">
            <CircularProgress />
          </div>
      ) : pdfLink && (
          <div className="w-3/4 justify-end align-top"> 
            <iframe
              src={`${process.env.NODE_ENV === 'production' ? 'https://auto-unit-test-gen-run.vercel.app/' : 'http://127.0.0.1:3000/'}${pdfLink}`}
              style={{ width: '100%', height: '85vh' }} 
              frameBorder="0"
              onLoad={() => {
                setLoading(false);
                setPdfLoaded(true);
              }}
            ></iframe>

            {/* Explanation Text */}
            <div style={{ marginTop: '20px' }}>
            <h1 style={{fontSize: '2em', fontWeight: 'bold'}}>Understanding Your Results:</h1>
              <p>You will be given a PDF report detailing your submitted files after the tests are generated and run. You will also be able to download a ZIP file containing a copy of your PDF report as well as the generated tests files.</p>
            <h1 style={{fontSize: '2em', fontWeight: 'bold'}}>Reading the Report:</h1>
              <h2 style={{fontSize: '1.5em', fontWeight: 'bold'}}>Each table&apos;s title is the name of the file that you submitted. Below is a quick explanation of each column of the table:</h2>
              <ul>
                <li><b>Total Tests Run -</b> This is the total number of tests run for your file.</li>
                <li><b>Tests Passed -</b> This is the number of tests that passed without issue.</li>
                <li><b>Total Errors -</b> This is the number of tests which produced errors.</li>
                <li><b>Runtime -</b> This is how long it took to generate, run, and record the results for the tests.</li>
                <li><b>Pass/Fail Ratio -</b> This is the total number of passed tests divided by the number of total tests. Higher is better.</li>
                <li><b>Coverage -</b> This is how much, line by line, of your original code was covered during testing. For example: if a test did not enter an if statement the lines in that if statement would not be covered. Higher is better.</li>
              </ul>
              <h2 style={{fontSize: '1.5em', fontWeight: 'bold'}}>Error Box - This final box contains the error messages produced, if any. It has some of its own information broken down below:</h2>
              <ul>
                <li><b>Test:</b> This is the test file and test name of the test that produced an error.</li>
                <li><b>Error Type:</b> This is the type of error encountered.</li>
                <li><b>Error Info:</b> This is the traceback it includes the test file, line number, and what the given and expected values were.</li>
              </ul>
            </div>
          </div>
          
        )}      
      
    <style jsx>{`
      .uploadButton:hover {
        background-color: #0056b3;
      }
      
      .uploadButton:active {
        background-color: #003f80; 
      }

      .align-top {
        align-self: flex-start;
      }
    `}</style>

    </main>
    </Layout>
  );  
}
export default Home;
