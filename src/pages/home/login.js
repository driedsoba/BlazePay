import React, { useState } from 'react';

function Login({setIsLoggedIn}) {
  const [data, setData] = useState({
    email: '',
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
      setIsLoggedIn(true)
      console.log('Response from server:', responseData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <div className="sign-up-container">
      <h1 style={{ color: 'black', fontFamily:'Oxygen', }}> Log In!</h1>
          <a style={{ color: '#4760c2' }}>Email Address</a>
          <input style={{
            backgroundColor: '#e5f3f7', 
            color: 'black',
            width:  200,
          }}
            type="text"
            name="email address"
            value={data.email}
            onChange={handleChange}
            placeholder="Raja@gmail.com"
          />
          <a style={{ color: 'grey' }}>Enter Email Address</a>
      </div>
        
      <div>&nbsp;</div>
       
      <div className="sign-up-container">
          <a style={{ color: '#4760c2' }}>Phone Number</a>
          <input style={{
            backgroundColor: '#e5f3f7', 
            color: 'black',
            width:  200,
          }}
            type="text"
            name="phone number"
            value={data.phoneNumber}
            onChange={handleChange}
            placeholder="83728237"
          />
          <a style={{ color: 'grey' }}>Enter Phone Number</a>

          <a>&nbsp;&nbsp;</a>
          <button style={{
                  backgroundColor: '#4760c2',
                  color: 'white',
                  borderColor: 'white',
                  borderTopLeftRadius: 35,
                  borderTopRightRadius: 35,
                  borderBottomLeftRadius: 35,
                  borderBottomRightRadius: 35,
                  width:  150,
                }} 
              onClick={handleSubmit}>Submit
        </button>
        
      </div>

      
    </div>
  );
}

export default Login;