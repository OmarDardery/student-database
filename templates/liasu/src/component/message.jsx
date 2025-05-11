import React from "react";

function Message(props) {
    return (
        <div className={"message"} style={{"display": `${props.display}`, "position": "fixed", "z-index": "100"}}>
            {props.message}
            <button onClick={() => {
                props.close();
            }}>X</button>
        </div>
    );
}

export default Message;