import React, {useState} from 'react';
import Form from './component/form';
function App() {
    let [action, setAction] = useState("login");
    return (
    <div style={{ textAlign: 'center' }}>
      <Form action = {action} />
    </div>
    );
}

export default App;
