import axios from "axios";

const rawURL = import.meta.env.VITE_API_URL;

function PrepareURL(raw: string | undefined | null, id?: string | null) {
  if (!raw) {
    throw new Error(`Failed to load url ${id}`);
  }
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
