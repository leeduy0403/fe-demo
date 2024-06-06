import { useEffect, useState } from 'react'
import io from 'socket.io-client'
import 
{ BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill}
 from 'react-icons/bs'

const Air = () => {
    const [data, setData] = useState({temperature: '', humidity: '', light: '', message: 'Hello'})

    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const response = await fetch('/api/env')
    //             const result = await response.json()
    //             setData(result)
    //         }
    //         catch (error) {
    //             console.log('Error fetching air data:', error)
    //         }
    //     }

    //     fetchData()
    // }, [])

    useEffect(() => {
        const socket = io('http://localhost:5000');

        socket.on('update_data', (newData) => {
            setData(newData);
        });

        socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>MESSAGES</h3>
                    <BsFillArchiveFill className='card_icon'/>
                </div>
                <h1>{data.message}</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>LUMINOSITY</h3>
                    <BsFillGrid3X3GapFill className='card_icon'/>
                </div>
                <h1>{data.light} LUX</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>MOISTURE</h3>
                    <BsPeopleFill className='card_icon'/>
                </div>
                <h1>{data.humidity}%</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>TEMPERATURE</h3>
                    <BsFillBellFill className='card_icon'/>
                </div>
                <h1>{data.temperature}&deg;C</h1>
            </div>
            
            
        </div>
    )
}

export default Air
