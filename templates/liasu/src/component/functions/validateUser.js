async function validateUser(id, password) {
  try {
    const response = await fetch(`/api/auth/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Let the backend know you're sending JSON data
      },
      body: JSON.stringify({ id, password }), // Send the ID in the request body
    });

    if (!response.ok) {
      // If HTTP response is not OK (status is not 2xx)
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json(); // Parse JSON response

  } catch (error) {
    // Handle network or other errors
    console.error('Error during validation request:', error.message);
    return { authenticated: false, message: error.message }; // Return an object with authentication status and error message
  }
}

export default validateUser;