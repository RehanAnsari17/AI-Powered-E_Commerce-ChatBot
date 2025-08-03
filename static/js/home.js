document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector("[data-modal]");
    const closeButton = document.querySelector("[data-modal-close]");
    const overlay = document.querySelector("[data-modal-overlay]");

    if (!modal || !closeButton || !overlay) {
        console.error("Modal elements not found! Check your HTML structure.");
        return;
    }

    // Function to close the modal
    function closeModal() {
        modal.style.display = "none"; // Hides the modal
    }

    // Click event on close button
    closeButton.addEventListener("click", closeModal);

    // Click event on overlay to close modal
    overlay.addEventListener("click", closeModal);
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        const query = document.getElementById('query').value;

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();

            if (response.ok) {
                if (data.message === "Search results for your query") {
                    // Clear previous results
                    resultsDiv.innerHTML = '';

                    // Limit results to 3
                    const limitedResults = data.results.slice(0, 3);

                    // Create a card for each result
                    const resultsCards = limitedResults.map(result => {
                        return `
                            <div class="card">
                                <img src="${result.img}" alt="${result.name}" class="card-img">
                                <div class="card-body">
                                    <h3 class="card-title">${result.name}</h3>
                                    <p class="card-price">$${result.price}</p>
                                    <p class="card-rating">Rating: ${result.avg_rating} (${result.ratingCount} reviews)</p>
                                </div>
                            </div>
                        `;
                    }).join('');

                    resultsDiv.innerHTML = resultsCards;
                } else {
                    resultsDiv.innerHTML = `<p>${data.message}</p>`;
                }
            } else {
                resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });
});

    let cart = [];

    function addToCart(button) {
        let product = button.closest(".product");
        let name = product.querySelector(".product-name a").innerText;
        let priceText = product.querySelector(".product-price").innerText;
        let price = parseFloat(priceText.replace("$", "").trim());
        let imageSrc = product.querySelector(".product-img img").src;
        let existingItem = cart.find(item => item.name === name);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ name, price, imageSrc, quantity: 1 });
        }

        updateCartUI();
        showAlert(`${name} has been added to the cart!`);  // Show alert
    }

    function updateCartUI() {
        let cartList = document.getElementById("cart-list");
        let cartQty = document.getElementById("cart-qty");
        let cartItemCount = document.getElementById("cart-item-count");
        let cartTotal = document.getElementById("cart-total");

        cartList.innerHTML = "";
        let totalItems = 0;
        let totalPrice = 0;

        cart.forEach((item, index) => {
            totalItems += item.quantity;
            totalPrice += item.price * item.quantity;

            let cartItem = document.createElement("div");
            cartItem.classList.add("product-widget");
            cartItem.innerHTML = `
                <div class="product-img">
                    <img src="${item.imageSrc}" alt="">
                </div>
                <div class="product-body">
                    <h3 class="product-name"><a href="#">${item.name}</a></h3>
                    <h4 class="product-price"><span class="qty">${item.quantity}x</span> $${(item.price * item.quantity).toFixed(2)}</h4>
                </div>
                <button class="delete" onclick="removeFromCart(${index})"><i class="fa fa-close"></i></button>
            `;
            cartList.appendChild(cartItem);
        });

        cartQty.innerText = totalItems;
        cartItemCount.innerText = totalItems;
        cartTotal.innerText = totalPrice.toFixed(2);
    }

    function removeFromCart(index) {
        cart.splice(index, 1);
        updateCartUI();
    }

    function showAlert(message) {
        let alertBox = document.createElement("div");
        alertBox.classList.add("cart-alert");
        alertBox.innerText = message;

        document.body.appendChild(alertBox);

        setTimeout(() => {
            alertBox.remove();
        }, 2000);
    }

    function redirectToPage(select) {
        let page = select.value;
        if (page) {
            window.location.href = page; // Redirect to the selected page
        }
    }