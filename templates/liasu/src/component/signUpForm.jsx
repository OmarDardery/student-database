import React, { useState } from "react";
import validateAndSendCode from "./functions/validate_student_id";

function SignUpForm(props){
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
    let [id, setId] = useState("");
    let [code, setCode] = useState("");
    let [phase, setPhase] = useState(1);
    async function handleSignUp (pass) {
        try {
            if (pass.length < 8) {
                props.setMessage("Password must have 8 or more characters");
                props.notify();
                return { requestStatus: "False", message: "Password too short" };
            } else if (pass !== confirmPassword) {
                props.setMessage("Passwords do not match");
                props.notify();
                return { requestStatus: "False", message: "Passwords don't match" };
            } else {
                console.log("Calling validateAndSendCode with ID:", id);
                const result = await validateAndSendCode(id);
                console.log("Result from validateAndSendCode:", result);
                return result;
            }
        } catch (error) {
            console.error("Error in handleSignUp:", error);
            return { requestStatus: "False", message: "An unexpected error occurred" };
        }
    }
async function validateCode(userCode) {
    if (userCode.length !== 6) {
        props.setMessage("Code must be 6 characters long.");
        props.notify();
        return { authenticated: false };
    } else {
        try {
            const response = await fetch(`/api/validate-code`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('root').getAttribute('data-csrf'),
                },
                // Change 'userCode' to 'code' to match the backend expectation
                body: JSON.stringify({ code: userCode }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log(data);
            // Convert the backend response format to what your frontend expects
            return {
                authenticated: data.requestStatus === "True",
                message: data.message || "Code validation complete"
            };
        } catch (error) {
            console.error("Error validating code:", error);
            props.setMessage("Error validating code");
            props.notify();
            return { authenticated: false };
        }
    }
}
    async function signUpUser(userId, userPassword) {
    try {
        const response = await fetch(`/api/sign-up`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('root').getAttribute('data-csrf'),
            },
            body: JSON.stringify({ userId, userPassword }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error signing up user:", error);
        return { completed: false, message: "Error signing up user" };
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
                                return (<div style={{"width": "100%"}}>
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
                                            <button 
  onClick={async () => {
    try {
      console.log("Button clicked, calling handleSignUp with password:", password);
      const result = await handleSignUp(password);
      console.log("Result from handleSignUp:", result);
      
      if (result && result.requestStatus === "True") {
        setPhase(2);
        props.setMessage("Verification code sent!");
        props.notify();
      } else {
        props.setMessage(result?.message || "Unknown error occurred");
        props.notify();
      }
    } catch (error) {
      console.error("Error in button click handler:", error);
      props.setMessage("An unexpected error occurred");
      props.notify();
    }
  }} 
  className={"form-submit-button"}
>
  Send code
</button>
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
                                                const result = await validateCode(code);
                                                if(result.authenticated){
                                                    setPhase(3);
                                                }else{
                                                    props.setMessage("Verification code incorrect");
                                                    props.notify();
                                                }
                                            }} className={"form-submit-button"}>Confirm code</button>
                                    </div>

                                );
                            case 3:
                                return (
                                    <div>
                                        <h1>
                                            Confirm Credentials:
                                        </h1>
                                        <div className={"form-field"}>
                                            <label htmlFor="ID">University ID:</label>
                                            <input type="text" contentEditable={"false"} value={id} name="ID" />
                                        </div>
                                        <div className={"form-field"}>
                                            <label htmlFor="password">Password:</label>
                                            <input contentEditable={"false"} value={password} name={"password"} type="text" />
                                        </div>
                                        <h4>By signing up you accept our <a href={"/terms/"} target={"_blank"}>Terms Of Service</a></h4>
                                        <button onClick={async ()=>{
                                                const result = await signUpUser(id, password);
                                                if(result.completed){
                                                    window.location.reload();
                                                }else{
                                                    props.setMessage("Something unexpected happened");
                                                    props.notify();
                                                }
                                            }} className={"form-submit-button"}>Complete sign up</button>
                                    </div>
                                );
                        }
                    })()}
                </div>
    </div>);
}

export default SignUpForm;