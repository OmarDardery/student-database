import React, {useState} from 'react';
import validateStudentId from './functions/validate_student_id';
import validateUser from './functions/validateUser';
import SignUpForm from "./signUpForm";

function Form(props) {
    let [id, setId] = useState("");
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
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
            </div>) : (
                <SignUpForm setPassword={setPassword} setId={setId} setConfirmPassword={setConfirmPassword} handleSignUp={handleSignUp}  />
            )
        }
        <button onClick={async ()=>{
            if(props.action === "signup") {
                await handleSignUp();
            }else {
                await handleSignIn();
            }
        }} className={"form-submit-button"}>Submit</button>
    </div>);
}

export default Form;