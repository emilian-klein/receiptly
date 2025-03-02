document.addEventListener("DOMContentLoaded", function () {
    addEventListenerOnCategorySearch();
    addEventListenerOnAddCategoryButtons();
    addEventListenerOnEditCategoryButtons();
    addEventListenerOnSubmitForm("manage-category-form");
    addEventListenerOnToastElement("categories-toast");
});

function addEventListenerOnCategorySearch() {
    const searchInput = document.getElementById("category-search");
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            filterCategories(searchInput.value.toLowerCase());
        });
    }
}

function filterCategories(searchValue) {
    const categories = document.querySelectorAll(".category-item");
    categories.forEach(category => {
        const categoryName = category.textContent.toLowerCase();
        category.classList.toggle("d-none", !categoryName.includes(searchValue));
    });
}

function addEventListenerOnAddCategoryButtons() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".add-category-button");
        if (button) {
            fillManageCategoryModal(button, "add");
        }
    });
}

function addEventListenerOnEditCategoryButtons() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".edit-category-button");
        if (button) {
            fillManageCategoryModal(button, "edit");
        }
    });
}

function fillManageCategoryModal(button, actionType) {
    const modal = document.getElementById("manage-category-modal");
    const form = document.getElementById("manage-category-form");
    form.reset();
    form.classList.remove("was-validated");
    if (actionType === "add") {
        modal.querySelector(".modal-title").textContent = "Add category";
        form.action = "/add-category/";
    } else if (actionType === "edit") {
        modal.querySelector(".modal-title").textContent = "Edit category";
        const categoryID = button.getAttribute("data-category-id");
        form.action = `/edit-category/${categoryID}/`;
        fetch(`/api/categories/${categoryID}`)
            .then(response => response.json())
            .then(data => {
                modal.querySelector("#category-name").value = data.name;
            })
            .catch(error => {
                console.error("Error occurred:", error);
            });
    }
}