import React, { useState, useEffect } from "react";
import { useAuthContext } from "../../context/AuthContext";
import {
  Card,
  CardContent,
  IconButton,
  InputBase,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { Box } from "@mui/system";

const Contacts = () => {
  const { jwt, setJWT, setUser, user } = useAuthContext();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    if (searchQuery.trim() === "") {
      // Handle empty search query
      setSearchResults([]);
      return;
    }

    try {
      // Perform your fetch request here, replace the URL with your API endpoint
      const response = await fetch("http://localhost:8000/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      // Handle the response as needed
      const responseData = await response.json();
      setJWT(responseData["access_token"]);
      setUser(responseData["user_data"]);
      console.log("Response from server:", responseData);
      setSearchResults([]); // Assuming the API returns an array of results
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    // You can add additional logic here when jwt or searchQuery changes
    // For example, you may want to auto-search when the jwt changes
    // or debounce the search query changes to reduce API calls.
  }, [jwt, searchQuery]);

  return (
    <>
      {jwt ? (
        <Box>
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="Search"
            inputProps={{ "aria-label": "search" }}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <IconButton
            type="button"
            sx={{ p: "10px" }}
            aria-label="search"
            onClick={handleSearch}
          >
            <SearchIcon />
          </IconButton>

          <Stack>
            {searchResults.map((result) => (
              <Card key={result.id}>
                <CardContent>
                  <Typography>{result.name}</Typography>
                  {/* Render other result data as needed */}
                </CardContent>
              </Card>
            ))}
          </Stack>
        </Box>
      ) : (
        <></>
      )}
    </>
  );
};

export default Contacts;
