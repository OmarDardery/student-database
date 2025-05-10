import React from 'react';


function Form(props) {
    return (<form>
        <div>
            <label htmlFor="ID">University ID:</label>
            <input type="text" name="ID" />
        </div>
        <div>
            <label htmlFor="ID">Password:</label>
            <input type="password" />
        </div>
        {(props.action === "login") ?
            <div>
                <label htmlFor="ID">Confirm Password:</label>
                <input type="password" />
            </div>
            : <div></div>}
        <button type="submit">Submit</button>
    </form>);
}

export default Form;