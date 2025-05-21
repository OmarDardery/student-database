import getCookie from "./getCookie";
const validateAndSendCode = async (id) => {
  try {
    const response = await fetch(`/api/send-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('student_database_csrftoken'),
      },
      body:
        JSON.stringify({
          id
        }),
    }).then((response) => {
      if (!response.ok) {
        throw new Error();
      }
    });
    return await response.json();
  } catch (error) {
    console.error('Error during validation request:', error.message);
  }
  return false;
};

export default validateAndSendCode;