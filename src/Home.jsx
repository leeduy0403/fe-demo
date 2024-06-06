import {useState, useEffect} from "react";
//import Webcam from 'react-webcam'
// import React from 'react'
// import Camera from './Camera'
import Slider from './Slider';
import Button_Cam from './Button_Cam';
import Light from './Light';
import Air from './Air';

 import 
 { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } 
 from 'recharts';
// import Slider from './Slider';

function getDate() {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = today.getFullYear();
  const date = today.getDate();
  return `${date}/${month}/${year}`;
}

function Home() {

    // // Should have an API to fetch data
    // const data = [
    //     {
    //       name: 'Page A',
    //       uv: 4000,
    //       pv: 2400
    //     },
    //     {
    //       name: 'Page B',
    //       uv: 3000,
    //       pv: 1398
    //     },
    //     {
    //       name: 'Page C',
    //       uv: 2000,
    //       pv: 9800
    //     },
    //     {
    //       name: 'Page D',
    //       uv: 2780,
    //       pv: 3908
    //     },
    //     {
    //       name: 'Page E',
    //       uv: 1890,
    //       pv: 4800
    //     },
    //     {
    //       name: 'Page F',
    //       uv: 2390,
    //       pv: 3800
    //     },
    //     {
    //       name: 'Page G',
    //       uv: 3490,
    //       pv: 4300
    //     },
    //   ];

    const [data, setData] = useState({temperature: '', humidity: '', light: ''});

    const [airData, setAirData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/api/env')
                const result = await response.json()
                const newData = {
                  temperature: result.temperature,
                  humidity: result.humidity,
                  light: result.light,
                  timestamp: new Date().toLocaleTimeString()
                };
                setData(newData)
                setAirData(prevData => [...prevData, newData]);
            }
            catch (error) {
                console.log('Error fetching air data:', error)
            }
        }

        fetchData();

        const interval = setInterval(fetchData, 10000)

        return () => {
            clearInterval(interval)
        }
    }, []);

    // get current data
    const [currentDate, setCurrentDate] = useState(getDate());
     

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3>DASHBOARD</h3>
        </div>

        <div><Air /></div>

        <div><Slider /></div>

        <div><Light /></div>

        <h2>The date today is: {currentDate}</h2>

        <div className='charts'>
            <ResponsiveContainer width="100%" height="100%">
            <BarChart
            width={500}
            height={300}
            data={airData}
            margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
            }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis domain={['auto', 'auto']}/>
                <Tooltip />
                <Legend />
                {/* <Bar dataKey="temperature" fill="#8884d8" /> */}
                <Bar dataKey="humidity" fill="#82ca9d" />
                </BarChart>
            </ResponsiveContainer>

            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                width={500}
                height={300}
                data={airData}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis domain={['auto', 'auto']}/>
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="temperature" stroke="#8884d8" activeDot={{ r: 8 }} />
                {/* <Line type="monotone" dataKey="humidity" stroke="#82ca9d" /> */}
                </LineChart>
            </ResponsiveContainer>

        </div>
    
        <div className='camera' ><Button_Cam /></div>
        
    </main>
  )
}

export default Home