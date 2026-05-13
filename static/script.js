const container = document.getElementById("catalogueContainer");

const searchInput = document.getElementById("searchInput");

const bookForm = document.getElementById("bookForm");

let books = [];


/* LOAD BOOKS */

async function loadBooks() {

    try {

        const response = await fetch("/catalogue");

        if (!response.ok) {
            throw new Error("Failed to load books");
        }

        books = await response.json();

        displayBooks(books);

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="error-message">
                Failed to load catalogue.
            </div>
        `;
    }
}


/* DISPLAY BOOKS */

function displayBooks(bookList) {

    container.innerHTML = "";

    if (bookList.length === 0) {

        container.innerHTML = `
            <div class="empty-message">
                No books found.
            </div>
        `;

        return;
    }

    bookList.forEach(book => {

        const card = document.createElement("div");

        card.className = "book-card";

        card.innerHTML = `

            <div class="book-top">

                <div class="book-tag">
                    ${book.releaseYear || "Unknown Year"}
                </div>

                <div class="book-id">
                    ID: ${book.id}
                </div>

            </div>

            <div class="book-title">
                ${book.title}
            </div>

            <div class="book-author">
                ${book.author}
            </div>

            ${
                book.publisher
                ? `
                    <div class="book-info">
                        <strong>Publisher:</strong>
                        ${book.publisher}
                    </div>
                `
                : ""
            }

            ${
                book.description
                ? `
                    <div class="book-description">
                        ${book.description}
                    </div>
                `
                : ""
            }

            <button
                class="delete-btn"
                onclick="deleteBook(${book.id})"
            >
                Delete
            </button>
        `;

        container.appendChild(card);
    });
}


/* SEARCH */

searchInput.addEventListener("input", (e) => {

    const searchText =
        e.target.value.toLowerCase().trim();

    const filteredBooks = books.filter(book => {

        const titleMatch =
            book.title &&
            book.title.toLowerCase().includes(searchText);

        const authorMatch =
            book.author &&
            book.author.toLowerCase().includes(searchText);

        const publisherMatch =
            book.publisher &&
            book.publisher.toLowerCase().includes(searchText);

        const idMatch =
            String(book.id).includes(searchText);

        return (
            titleMatch ||
            authorMatch ||
            publisherMatch ||
            idMatch
        );
    });

    displayBooks(filteredBooks);
});


/* ADD BOOK */

bookForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const newBook = {

        title:
            document.getElementById("title").value,

        author:
            document.getElementById("author").value,

        publisher:
            document.getElementById("publisher").value,

        releaseYear:
            parseInt(
                document.getElementById("releaseYear").value
            ) || null,

        description:
            document.getElementById("description").value
    };

    try {

        const response = await fetch("/catalogue", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(newBook)
        });

        if (!response.ok) {
            throw new Error("Failed to add book");
        }

        bookForm.reset();

        loadBooks();

    } catch (error) {

        console.error(error);

        alert("Failed to add book");
    }
});


/* DELETE BOOK */

async function deleteBook(bookId) {

    const confirmed = confirm(
        `Delete book ID ${bookId}?`
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `/catalogue/${bookId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete book");
        }

        loadBooks();

    } catch (error) {

        console.error(error);

        alert("Failed to delete book");
    }
}


/* INITIAL LOAD */

loadBooks();