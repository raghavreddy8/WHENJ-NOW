const API_URL =
    "http://127.0.0.1:8000/api/articles/today";

export async function fetchArticles(){

    const response = await fetch(API_URL);

    return await response.json();

}