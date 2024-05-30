import React, { useState } from 'react' 


export default function Slider() {
    const [fanSpeed, setfanSpeed] = useState(50);
    const handleChange = (event) => {
        setfanSpeed(event.target.value);
    };

    return (
        <div className='card-slider'>
            <div className='card-inner-slider'>
                <h3>FAN SPEED</h3>
                
                <input 
                className='slider'
                type="range" 
                ming='0'
                max='100'
                fanSpeed={fanSpeed}
                onChange={handleChange}        
                />
                <h1> {fanSpeed}</h1>
            </div>
        </div>
    );
}