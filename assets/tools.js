
  // Utility to get CSRF token from cookies
  function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Main reusable function to call API securely
  async function callApiSecurely(apiUrl, data = {}) {
    const csrftoken = getCSRFToken();

    try {
      const response = await fetch(apiUrl, {
        method: 'POST', // use POST, can be adjusted if needed
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const jsonData = await response.json();
      return jsonData;  // Return the parsed JSON data

    } catch (error) {
      console.error('Error in API call:', error);
      return null; // or you can throw error or return an error object
    }
  }


  function test(){
  return 'true'
  }
