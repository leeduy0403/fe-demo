import React, { useState } from 'react';
import Camera from './Camera'; // Make sure the import path is correct for your project structure

const MainContainer = () => {
    const [isCameraOpen, setIsCameraOpen] = useState(false);

    const toggleCamera = () => {
        setIsCameraOpen(prevState => !prevState);
    };

    return (
        <main className='main-container'>
            <div className='main-title'>
                <h3>AI CAMERA</h3>
            </div>
            <button onClick={toggleCamera}>
                {isCameraOpen ? 'Close Camera' : 'Open Camera'}
            </button>
            {isCameraOpen && (
                <div>
                    <Camera />
                </div>
            )}
        </main>
    );
};

export default MainContainer;