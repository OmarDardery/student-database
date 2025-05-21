import React, {useState} from 'react';
import validateUser from './functions/validateUser';
import SignUpForm from "./signUpForm";

function Form(props) {
    let [id, setId] = useState("");
    let [password, setPassword] = useState("");
    async function handleSignIn() {
        let response = await validateUser(id, password);
        if(response.authenticated) {
            window.location.href = "/";
        }else{
            props.setMessage(response.message);
            props.notify();
        }
    }
    return (<div className={"form"}>
        {props.action === "login" ?
            (<div style={{"width": "100%"}}>
                <div className={"form-field"}>
                    <label htmlFor="ID">University ID:</label>
                    <input type="text" onChange={(e)=>{
                        setId(e.target.value);
                    }} value={id} name="ID" />
                </div>
                <div className={"form-field"}>
                    <label htmlFor="ID">Password:</label>
                    <input onChange={(e)=>{
                        setPassword(e.target.value);
                    }} value={password} type="password" />
                </div>
                <button onClick={async ()=>{
                    await handleSignIn()
                }} className={"form-submit-button"}>Submit</button>
            </div>) : (
                <SignUpForm setMessage={props.setMessage} notify={props.notify}  />
            )
        }
    </div>);
}

export default Form;