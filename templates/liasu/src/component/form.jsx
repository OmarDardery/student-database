import React, {useState} from 'react';
import validateStudentId from './functions/validate_student_id';

function Form(props) {
    let [message, setMessage] = useState("");
    let [id, setId] = useState("");
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
    async function handleSignUp () {
        if(password !== confirmPassword) {
            alert("Passwords do not match");
        }else{
            let response = await validateStudentId(id);
            setMessage( String(response) );
        }
    }
    function handleSignIn() {
    }
    return (<div>
        {message}
        <div>
            <label htmlFor="ID">University ID:</label>
            <input type="text" onChange={(e)=>{
                setId(e.target.value);
            }} value={id} name="ID" />
        </div>
        <div>
            <label htmlFor="ID">Password:</label>
            <input onChange={(e)=>{
                setPassword(e.target.value);
            }} value={password} type="password" />
        </div>
        {(props.action === "signup") ?
            <div>
                <label htmlFor="ID">Confirm Password:</label>
                <input onChange={(e)=>{
                setConfirmPassword(e.target.value);
            }} value={confirmPassword} type="password" />
            </div>
            : <div></div>}
        <button onClick={()=>{
            if(props.action === "signup") {
                handleSignUp();
            }else {
                handleSignIn();
            }
        }}>Submit</button>
    </div>);
}

export default Form;