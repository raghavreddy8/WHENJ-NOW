// Replace the RENDER_BACKEND_URL with your actual Render URL after deploying your backend
const RENDER_BACKEND_URL = "https://whenj-now.onrender.com";
const LOCAL_BACKEND_URL = "http://127.0.0.1:8000";

const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const API_URL = isLocalhost 
    ? `${LOCAL_BACKEND_URL}/api/articles/today` 
    : `${RENDER_BACKEND_URL}/api/articles/today`;

export async function fetchArticles(){

    const response = await fetch(API_URL);

    return await response.json();

}