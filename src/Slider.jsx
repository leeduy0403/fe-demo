import { useState } from 'react' 


export default function Slider() {
    const [fanSpeed, setfanSpeed] = useState(0);
    const handleChange = async (event) => {
        const newSpeed = event.target.value;
        setfanSpeed(newSpeed);

        try {
            const response = await fetch(`/api/fan?speed=${newSpeed}`, {
                method: 'POST',
            });
            const result = await response.json();
            console.log('Fan speed set to:', result.fan_speed);
        } catch (error) {
            console.error('Error setting fan speed:', error);
        }
    };


    return (
        <div className='card-slider'>
            <div className='card-inner-slider'>
                <h3>FAN SPEED</h3>
                
                <input 
                className='slider'
                type="range" 
                min='0'
                max='100'
                value={fanSpeed}
                onChange={handleChange}        
                />
                <h1> {fanSpeed} </h1>
            </div>
        </div>
    );
}