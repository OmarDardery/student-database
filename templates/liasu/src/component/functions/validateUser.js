
async function validateUser(id, password) {
  try {
    console.log("Validating user");
    const response = await fetch(`/api/auth`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementById('root').getAttribute('data-csrf'),
      },
      body: JSON.stringify({ id, password }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Properly await the JSON parsing
    const data = await response.json();
    console.log(data);

    // Check authentication status - note the comparison
    if (data.authenticated === "True" || data.authenticated === true) {
      return { authenticated: true };
    } else {
      return { authenticated: false, message: data.message || "Authentication failed" };
    }
  } catch (error) {
    console.error('Error during validation request:', error.message);
    return { authenticated: false, message: error.message };
  }
}

export default validateUser;