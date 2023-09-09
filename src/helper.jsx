//Gets sets and removes the Auth Token Retrieved from Strapi
//Stores in local storage

export const getToken = () => {
  return localStorage.getItem("authToken");
};

export const setToken = (token) => {
  if (token) {
    localStorage.setItem("authToken", token);
  }
};

export const removeToken = () => {
  localStorage.removeItem("authToken");
};
