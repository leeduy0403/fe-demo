import React, { useState } from 'react';

export default function Light() {
    const [isOn, setIsOn] = useState(false);

    const toggleLight = () => {
        setIsOn(!isOn);
    };

    return (
        <div className='card-light'>
            <div className='card-inner-light'>
                <h3>LIGHT</h3>
                <button onClick={toggleLight}>
                    {isOn ? 'PRESS HERE' : 'PRESS HERE'}
                </button>
                <h1>{isOn ? 'ON' : 'OFF'}</h1>
            </div>
        </div>
    );
}