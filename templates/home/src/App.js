import React from 'react';
import getCookie from './components/functions/getCookie';
function App() {
  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Home</h1>
      <button onClick={async ()=>{
          await fetch("/api/logout", {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie("student_database_csrftoken"),
              }
          }).then(response => {
            window.location.href = "/";
          })
      }}>Logout</button>
    </div>
  );
}

export default App;
