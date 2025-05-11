import React, {useState} from 'react';
import Form from './component/form';
import "./css/index.css"
import Message from "./component/message";


function App() {
    let [message, setMessage] = useState("");
    let [display, setDisplay] = useState("none");
    let [action, setAction] = useState("login");
    return (
    <div className={"form-container"}>
        <Message message={message} display={display} close={()=>{
            setDisplay("none");
        }}  />
        <div className={"form-button-slider"}>
            <button onClick={() => {
                setAction("login");
            }} className={action === "login" ? "active" : ""}>
            <h1>Login</h1>
            </button>
            <button onClick={() => {
                setAction("signup");
            }} className={action === "login" ? "" : "active"}>
            <h1>Sign Up</h1>
            </button>
        </div>
      <Form notify={()=>{
            setDisplay("block");
        }} setMessage= {setMessage} action = {action} />
    </div>
    );
}

export default App;
