let selectedRating = 0;

const reviewSection = document.querySelector(".review-section");
const pageId = reviewSection.dataset.pageId;

// chave única no LocalStorage
const STORAGE_KEY = `reviews_${pageId}`;
// ⭐⭐⭐ Sistema de estrelas (hover + clique)
document.querySelectorAll("#starContainer span").forEach(star => {

    star.addEventListener("mouseover", function () {
        highlightStars(this.dataset.value);
    });

    star.addEventListener("mouseout", function () {
        highlightStars(selectedRating);
    });

    star.addEventListener("click", function () {
        selectedRating = this.dataset.value;
        highlightStars(selectedRating);
    });
});

function highlightStars(rating) {
    document.querySelectorAll("#starContainer span").forEach(star => {
        star.classList.remove("selected");
        if (parseInt(star.dataset.value) <= rating) {
            star.classList.add("selected");
        }
    });
}

// ⭐⭐⭐ Enviar avaliação
document.getElementById("submitReview").addEventListener("click", function () {

    const text = document.getElementById("reviewText").value.trim();

    if (selectedRating == 0) {
        alert("Por favor, escolha uma nota.");
        return;
    }

    if (text.length < 3) {
        alert("O comentário é muito curto.");
        return;
    }

    const newReview = {
        rating: parseInt(selectedRating),
        text: text,
        date: new Date().toLocaleString("pt-BR")
    };

    let reviews = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    reviews.push(newReview);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews));

    document.getElementById("reviewText").value = "";
    selectedRating = 0;
    highlightStars(0);

    loadReviews();
});


// ⭐⭐⭐ Carregar avaliações
function loadReviews() {
    let reviews = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

    const list = document.getElementById("reviewsList");
    list.innerHTML = "";

    if (reviews.length === 0) {
        list.innerHTML = "<p>Sem avaliações ainda.</p>";
        return;
    }

    let total = 0;

    reviews.forEach(review => {
        total += review.rating;

        const div = document.createElement("div");
        div.classList.add("review");

        div.innerHTML = `
            <strong>${"★".repeat(review.rating)}</strong> – ${review.date}
            <p>${review.text}</p>
        `;

        list.appendChild(div);
    });

    const avg = (total / reviews.length).toFixed(1);

    document.getElementById("avgRating").innerText = avg;
    document.getElementById("totalReviews").innerText = reviews.length;

    if (document.getElementById("topAvgRating"))
        document.getElementById("topAvgRating").innerText = avg;

    if (document.getElementById("topTotalReviews"))
        document.getElementById("topTotalReviews").innerText = reviews.length;
}

/* === Carrinho de compras === */

function addToCart() {
    // dados do produto
    const product = {
        id: 1,  // coloque um ID diferente em cada página
        name: "Violão Elétrico Takamine FT340 BS",
        price: 13290.50,
        image: "https://i.postimg.cc/zBqSgMhr/imgtk.webp",
        qty: 1
    };

    // verificar carrinho no localStorage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // verificar se já existe no carrinho
    let existing = cart.find(item => item.id === product.id);

    if (existing) {
        existing.qty += 1; // aumenta quantidade
    } else {
        cart.push(product);
    }

    // salva novamente
    localStorage.setItem("cart", JSON.stringify(cart));

    alert("Produto adicionado ao carrinho!");
}
// Carrega tudo ao iniciar
loadReviews();
