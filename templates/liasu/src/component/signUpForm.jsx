import React, { useState } from "react";
import validateStudentId from "./functions/validate_student_id";

function SignUpForm(props){
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
    let [id, setId] = useState("");
    let [phase, setPhase] = useState(1);
    async function handleSignUp () {
        if(password !== confirmPassword) {
            props.setMessage("Passwords do not match");
            props.notify();
        }else{
            let response = await validateStudentId(id);
            props.setMessage( String(response) );
            props.notify();
        }
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
                                        await handleSignUp(setPhase)
                                    }} className={"form-submit-button"}>Send code</button>
                                </div>);
                    case 2:
                        return (
                            <div className={"form-field"}>

                            </div>
                        );
                }
            })()}
        </div>
    </div>);
}

export default SignUpForm;