var syncedFavorites;

function toggleFavorite(user, movieId, favorites) {
    if (!syncedFavorites) {
        syncedFavorites = favorites;
    }

    if (user) {
        const isFavorite = syncedFavorites.includes(movieId);
        console.log(movieId);
        console.log(syncedFavorites);
        const action = isFavorite ? "remove" : "add";
        fetch(`/update-user/${movieId}?action=${action}`, {
            method: "POST",
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("User data updated successfully:", data);

                const favoriteIcon = document.querySelector(".favorite");
                favoriteIcon.classList.toggle("active", !isFavorite);

                syncedFavorites = data.Favorites;
            })
            .catch((error) => {
                console.error("Error updating user data:", error);
            });
    } else {
        alert("Please log in to favorite this movie.");
    }
}
