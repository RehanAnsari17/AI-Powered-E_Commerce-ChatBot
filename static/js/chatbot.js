document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');
    const userMessageDiv = document.getElementById('userMessage');
    const responseMessageDiv = document.getElementById('responseMessage');
    const responseContainer = document.getElementById('responseContainer');
    const quickSearchBtns = document.querySelectorAll('.quick-search-btn');

    quickSearchBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            document.getElementById('query').value = query;
            form.dispatchEvent(new Event('submit'));
        });
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const query = document.getElementById('query').value.trim();

        if (!query) return;

        userMessageDiv.textContent = query;
        userMessageDiv.style.display = 'block';
        responseContainer.style.display = 'none';
        resultsDiv.innerHTML = '';
        responseMessageDiv.textContent = '';

        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'chat-message response-message';
        loadingMessage.textContent = 'Searching for the perfect fashion items...';
        loadingMessage.style.display = 'block';
        responseContainer.insertBefore(loadingMessage, resultsDiv);
        responseContainer.style.display = 'block';

        document.getElementById('query').value = '';

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            responseContainer.removeChild(loadingMessage);

            if (response.ok) {
                console.log("🔄 Full Response:", data);

                if (data.message.includes("recommended products")) {
                    responseMessageDiv.textContent = data.message;
                    responseMessageDiv.style.display = 'block';
                    responseContainer.style.display = 'block';

                    const limitedResults = data.results.slice(0, 3);

                    const resultsCards = limitedResults.map(result => {
                        return `
                            <div class="card">
                                <div class="card-img-container">
                                    <img src="${result.image_url}" 
                                         alt="${result.name}" 
                                         class="card-img" 
                                         loading="lazy"
                                         onerror="this.onerror=null;this.src='/static/img/high-quality-placeholder.jpg';this.classList.add('error-image')">
                                    <div class="img-loading">Loading...</div>
                                </div>
                                <div class="card-body">
                                    <h3 class="card-title">${result.name}</h3>
                                    <p class="card-info">Color: ${result.colour} | Category: ${result.Category}</p>
                                </div>
                            </div>
                        `;
                    }).join('');

                    resultsDiv.innerHTML = resultsCards;
                    
                    // Image loading handler
                    document.querySelectorAll('.card-img').forEach(img => {
                        img.onload = function() {
                            this.classList.add('loaded');
                            const loadingDiv = this.nextElementSibling;
                            if (loadingDiv && loadingDiv.classList.contains('img-loading')) {
                                loadingDiv.style.opacity = '0';
                                loadingDiv.style.pointerEvents = 'none';
                            }
                        };
                        if (img.complete) {
                            img.classList.add('loaded');
                            const loadingDiv = img.nextElementSibling;
                            if (loadingDiv && loadingDiv.classList.contains('img-loading')) {
                                loadingDiv.style.opacity = '0';
                                loadingDiv.style.pointerEvents = 'none';
                            }
                        }
                    });

                } else {
                    responseMessageDiv.textContent = data.message;
                    responseMessageDiv.style.display = 'block';
                    responseContainer.style.display = 'block';
                }
            } else {
                responseMessageDiv.textContent = `Error: ${data.error}`;
                responseMessageDiv.style.display = 'block';
                responseContainer.style.display = 'block';
            }

        } catch (error) {
            console.error("❌ Fetch error:", error);
            responseMessageDiv.textContent = `Error: ${error.message}`;
            responseMessageDiv.style.display = 'block';
            responseContainer.style.display = 'block';
        }
    });
});