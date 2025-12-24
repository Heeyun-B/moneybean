import axios from "./index";

export const getUserProfile = async () => {
  const response = await axios.get("/api/accounts/profile/");
  return response.data;
};

export const updateProfile = async (profileData) => {
  const response = await axios.put("/api/accounts/profile/update/", profileData);
  return response.data;
};