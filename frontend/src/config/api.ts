import axios from "axios";

const rawURL = import.meta.env.VITE_API_URL ?? "http://localhost:8010";

function PrepareURL(raw: string) {
  return raw.startsWith("http")
    ? raw.replace(/\/$/, "")
    : `https://${raw.replace(/\/$/, "")}`;
}

export const apiURL = PrepareURL(rawURL);

axios.defaults.withCredentials = true;

const api = axios.create({
  baseURL: apiURL,
});

export default api;
