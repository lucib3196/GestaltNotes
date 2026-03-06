import axios from "axios";

const rawURL = import.meta.env.VITE_API_URL;
const env = import.meta.env.VITE_ENV;

const protocol = env === "dev" ? "http" : "https";

function PrepareURL(raw: string): string {
  if (!raw || raw.trim() === "") {
    throw new Error("VITE_API_URL is not defined or empty");
  }

  let url = raw.trim();

  // remove trailing slash
  url = url.replace(/\/$/, "");

  // remove existing protocol
  url = url.replace(/^https?:\/\//, "");

  // add correct protocol
  url = `${protocol}://${url}`;

  return url;
}

export const apiURL = PrepareURL(rawURL);

axios.defaults.withCredentials = true;

const api = axios.create({
  baseURL: apiURL,
});

export default api;
