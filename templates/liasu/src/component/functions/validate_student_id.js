const validateAndSendCode = async (id) => {
  try {
    console.log("send code");
    
    // Make the fetch request
    const response = await fetch(`/api/send-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementById('root').getAttribute('data-csrf'),
      },
      body: JSON.stringify({ id }),
    });
    
    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    // Parse the JSON
    const data = await response.json();
    console.log("Response data:", data);
    
    // Return the data
    return data;
    
  } catch (error) {
    console.error('Error during validation request:', error);
    // Return a standardized error object
    return {
      requestStatus: "False",
      message: error.message || "An error occurred during validation"
    };
  }
};

export default validateAndSendCode;