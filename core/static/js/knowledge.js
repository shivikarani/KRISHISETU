document.addEventListener("DOMContentLoaded", function () {
    loadCategories();
    loadArticles();
});

function loadCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('categoryFilters');
            container.innerHTML = `<button onclick="loadArticles()">All</button>`;
            data.categories.forEach(cat => {
                container.innerHTML += `
                    <button onclick="loadArticles(${cat.id})">${cat.name}</button>
                `;
            });
        });
}

function loadArticles(categoryId = null) {
    let url = '/api/articles/';
    if (categoryId) {
        url += `?category=${categoryId}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('articlesContainer');
            container.innerHTML = "";

            if (data.articles.length === 0) {
                container.innerHTML = "<p>No articles found.</p>";
                return;
            }

            data.articles.forEach(article => {
                container.innerHTML += `
                    <div class="article-card">
                        <h3>${article.title}</h3>
                        <p><strong>${article.category}</strong></p>
                        <p>${article.content}...</p>
                        <small>${article.created_at}</small>
                    </div>
                `;
            });
        });
}