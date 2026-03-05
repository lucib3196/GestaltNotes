import axios from "axios";

const rawURL = import.meta.env.VITE_API_URL;

function PrepareURL(raw: string): string {
  if (!raw || raw.trim() === "") {
    throw new Error("VITE_API_URL is not defined or empty");
  }

  let url = raw.trim().replace(/\/$/, "");

  if (!url.startsWith("https://")) {
    url = url.replace(/^http:\/\//, "");
    url = `https://${url}`;
  }

  return url;
}

export const apiURL = PrepareURL(rawURL);

axios.defaults.withCredentials = true;

const api = axios.create({
  baseURL: apiURL,
});

export default api;