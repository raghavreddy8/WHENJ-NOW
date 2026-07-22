export function createArticleCard(article) {

    const card = document.createElement("div");

    card.className = "article-card fade-in";

    const published = article.published
        ? new Date(article.published).toLocaleString()
        : "Unknown";

    const importance = "★".repeat(article.importance ?? 0);

    card.innerHTML = `

        <h2 class="article-title">
            ${article.title}
        </h2>

        <p class="article-summary">
            ${article.intelligence_summary}
        </p>

        <div class="article-footer">

            <div>

                <div class="badge">
                    ${article.source}
                </div>

                <p class="mt-3 text-slate-400">
                    Published : ${published}
                </p>

                <p class="mt-1 text-yellow-300">
                    ${importance}
                </p>

            </div>

            <a
                class="read-btn"
                href="${article.link}"
                target="_blank">

                Read Original →

            </a>

        </div>

    `;

    return card;

}

export function renderArticles(articles) {

    const container =
        document.getElementById("articlesContainer");

    container.innerHTML = "";

    articles.forEach(article => {

        container.appendChild(
            createArticleCard(article)
        );

    });

}