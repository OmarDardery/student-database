import React, { useState } from "react";
import validateAndSendCode from "./functions/validate_student_id";

function SignUpForm(props){
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
    let [id, setId] = useState("");
    let [code, setCode] = useState("");
    let [phase, setPhase] = useState(1);
    async function handleSignUp (pass) {
        if(pass.length < 8){
            props.setMessage("Password must have 8 or more characters");
            props.notify();
        }else if(pass !== confirmPassword) {
            props.setMessage("Passwords do not match");
            props.notify();
        }else{
            let response = await validateAndSendCode(id);
            if(response.requestStatus === "True"){
                setPhase(2);
                props.setMessage("Verification code sent!");
            }else{
                props.setMessage(response.message);
                props.notify();
            }
        }
    }
    async function validateCode(userCode){
        
    }

    return (<div style={{"height": "80%", "width": "90%"}}>
        <div style={{"width" : "100%"}}><div style={{"width": "100%", "height": "3%", "display": "flex", "justifyContent": "center", "alignItems": "center"}}>
            <div style={phase === 2 ? {"height": "100%", "width": "50%", "backgroundColor": "darkslategrey"} : {"height": "100%", "width": "50%", "backgroundColor": "whitesmoke"}}></div>
            <div style={phase === 3 ? {"height": "100%", "width": "50%", "backgroundColor": "darkslategrey"} : {"height": "100%", "width": "50%", "backgroundColor": "whitesmoke"}}></div>
        </div>
            {(() => {
                switch(phase) {
                    case 1:
                        return (<div className={"form-field"}>
                                    <div className={"form-field"}>
                                    <label htmlFor="ID">University ID:</label>
                                        <input type="text" onChange={(e)=>{
                                            setId(e.target.value);
                                        }} value={id} name="ID" />
                                    </div>
                                    <div className={"form-field"}>
                                        <label htmlFor="password">Password:</label>
                                        <input onChange={(e)=>{
                                            setPassword(e.target.value);
                                        }} value={password} name={"password"} type="password" />
                                    </div>
                                    <div className={"form-field"}>
                                        <label htmlFor="confirmPoassword">Confirm Password:</label>
                                        <input onChange={(e)=>{
                                            setConfirmPassword(e.target.value);
                                        }} value={confirmPassword} name={"confirmPassword"} type="password" />
                                    </div>
                                    <button onClick={async ()=>{
                                        await handleSignUp(password);
                                    }} className={"form-submit-button"}>Send code</button>
                                </div>);
                    case 2:
                        return (
                            <div>
                                <div className={"form-field"}>
                                    <label htmlFor="code">Verification code:</label>
                                    <input type="text" onChange={(e)=>{
                                        setCode(e.target.value);
                                    }} value={code} name="code" />
                                </div>
                                <button onClick={async ()=>{
                                        await validateCode(code);
                                    }} className={"form-submit-button"}>Confirm code</button>
                            </div>

                        );
                }
            })()}
        </div>
    </div>);
}

export default SignUpForm;