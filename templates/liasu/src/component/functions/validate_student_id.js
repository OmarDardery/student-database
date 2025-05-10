const validateStudentId = async (id) => {
  try {
    const response = await fetch(`/api/validate/${id}/`, {
      method: 'GET', // GET request
      headers: {
        'Content-Type': 'application/json', // Let the backend know you're sending JSON data
      },
    });

    if (!response.ok) {
      // If HTTP response is not OK (status is not 2xx)
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json(); // Parse JSON response
    return data.message;
  } catch (error) {
    // Handle network or other errors
    console.error('Error during validation request:', error.message);
  }
  return false; // Return false if validation fails or an error occurs
};

export default validateStudentId;