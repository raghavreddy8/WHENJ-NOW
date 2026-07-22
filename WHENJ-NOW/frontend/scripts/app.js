import { fetchArticles } from "./api.js";
import { renderArticles } from "./ui.js";

let currentArticles = [];

async function loadArticles() {

    try {

        const response = await fetchArticles();

        currentArticles = response.articles;

        renderArticles(currentArticles);

        document.getElementById(
            "lastUpdated"
        ).innerText =
            `Last Updated : ${
                new Date(response.last_updated)
                    .toLocaleTimeString()
            }`;

    }

    catch(error){

        console.error(error);

    }

}

function searchArticles(){

    const search =
        document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const filtered =
        currentArticles.filter(article =>

            article.title
                .toLowerCase()
                .includes(search)

            ||

            article.intelligence_summary
                .toLowerCase()
                .includes(search)

            ||

            article.source
                .toLowerCase()
                .includes(search)

        );

    renderArticles(filtered);

}

document
    .getElementById("searchInput")
    .addEventListener(
        "input",
        searchArticles
    );

loadArticles();

setInterval(
    loadArticles,
    60000
);