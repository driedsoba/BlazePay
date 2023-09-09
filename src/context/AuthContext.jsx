//Creates a context to store the user login data

import { createContext, useContext } from "react";

export const AuthContext = createContext({
  user: undefined,
  isLoading: false,
  setUser: () => {},
  refreshData: () => {},
});

export const useAuthContext = () => useContext(AuthContext);
