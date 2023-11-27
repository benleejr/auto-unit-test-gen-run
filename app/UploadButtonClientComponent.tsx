//UploadButtonClientComponent
'use client';
import React from 'react';
import OpenAI from "openai";

const UploadButtonClientComponent = ({ inputId, apiKey }: { inputId: string, apiKey: string}) => {
    const processFile = () => {
        const fileInput = document.getElementById(inputId) as HTMLInputElement;
        const files = fileInput.files;
        if (!files) return;
    
        for (let i = 0; i < files.length; i++) {
          if (files[i].name.endsWith('.py')) { // only process Python files
            const reader = new FileReader();
            reader.onload = function(event) {
              const fileContent = event.target?.result;
    
              if (fileContent && typeof fileContent === 'string') {
                const openai = new OpenAI({
                    apiKey: apiKey,
                    dangerouslyAllowBrowser: true
                });
    
                openai.chat.completions.create({
                  model: "gpt-3.5-turbo-16k",
                  messages: [
                    {
                      "role": "system",
                      "content": "You will be receiving programming files in Python that may be part of a larger project.\nYour goal is to write unit tests for the files given to you.\nONLY give unit test code as a response that can be run.\nDO NOT give any other prompts or descriptions.\nAdd comments to the code as you see necessary."
                    },
                    {
                      "role": "user",
                      "content": fileContent
                    }
                  ],
                  temperature: 1,
                  max_tokens: 16000,
                  top_p: 1,
                  frequency_penalty: 0,
                  presence_penalty: 0,
                }).then(apiResponse => {
                  console.log('GPT-3 response:', apiResponse);
                }).catch(error => {
                  console.error('GPT-3 error:', error);
                });
              }
            };
            reader.readAsText(files[i]);
          }
        } 
  };

  return (
    <button onClick={processFile}>
      Process Files
    </button>
  );
};

export default UploadButtonClientComponent;
