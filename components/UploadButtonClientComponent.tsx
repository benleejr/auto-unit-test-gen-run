//UploadButtonClientComponent
'use client';
import React from 'react';

const UploadButtonClientComponent = ({ inputId }: { inputId: string}) => {
    const processFile = () => {
        const fileInput = document.getElementById(inputId) as HTMLInputElement;
        const files = fileInput.files;
        if (!files) return;      

  return (
    <button onClick={processFile}>
      Process Files
    </button>
  );
};
}

export default UploadButtonClientComponent;
