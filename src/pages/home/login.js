import React, { useState } from 'react';

function Login() {
  const [data, setData] = useState({
    phone: '',
    phoneNumber: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/your-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      // Handle the response as needed
      const responseData = await response.json();
      console.log('Response from server:', responseData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        name="phone"
        value={data.phone}
        onChange={handleChange}
        placeholder="Phone"
      />
      <input
        type="text"
        name="phone number"
        value={data.phoneNumber}
        onChange={handleChange}
        placeholder="Phone Number"
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default Login;