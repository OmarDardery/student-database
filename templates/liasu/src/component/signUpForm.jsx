import React, { useState } from "react";
import validateStudentId from "./functions/validate_student_id";

function SignUpForm(props){
    let [password, setPassword] = useState("");
    let [confirmPassword, setConfirmPassword] = useState("");
    let [id, setId] = useState("");
    let [phase, setPhase] = useState(1);
    return (<div style={{"height": "80%", "width": "90%"}}>
        <div style={{"width": "100%", "height": "3%", "display": "flex", "justifyContent": "center", "alignItems": "center"}}>
            <div style={{"height": "100%", "width": "50%", "backgroundColor": "darkslategrey"}}></div>
            <div style={phase === 2 ? {"height": "100%", "width": "50%", "backgroundColor": "darkslategrey"} : {"height": "100%", "width": "50%", "backgroundColor": "whitesmoke"}}></div>
        </div>

    </div>);
}

export default SignUpForm;