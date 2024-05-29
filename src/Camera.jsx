import {useRef} from "react";
import Webcam from 'react-webcam'

function App() {

    const webRef = useRef(null);

    return (
        <div className="App">
            <Webcam ref={webRef} />
        </div>

    );
    
}
export default App;