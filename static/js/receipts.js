document.addEventListener("DOMContentLoaded", function () {
    addEventListenerOnAddReceiptButton();
    addEventListenerOnEditReceiptButtons();
    addEventListenerOnAddReceiptItemButton();
    addEventListenerOnDeleteReceiptItemButton();
    addEventListenerOnSubmitForm("manage-receipt-form");
    addEventListenerOnToastElement("receipts-toast");
});

function addEventListenerOnAddReceiptButton() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".add-receipt-button");
        if (button) {
            fillManageReceiptModal(button, "add");
        }
    });
}

function addEventListenerOnEditReceiptButtons() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".edit-receipt-button");
        if (button) {
            fillManageReceiptModal(button, "edit");
        }
    });
}

function addEventListenerOnAddReceiptItemButton() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".add-receipt-item-button");
        if (button) {
            addReceiptItem(button);
        }
    });
}

function addEventListenerOnDeleteReceiptItemButton() {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".delete-receipt-item-button");
        if (button) {
            deleteReceiptItem(button);
        }
    });
}

function fillManageReceiptModal(button, actionType) {
    const modal = document.getElementById("manage-receipt-modal");
    const form = document.getElementById("manage-receipt-form");
    modal.querySelector(".receipt-items").innerHTML = "";
    form.reset();
    form.classList.remove("was-validated");
    if (actionType === "add") {
        modal.querySelector(".modal-title").textContent = "Add receipt";
        form.action = "/add-receipt/";
        let item_template = document.getElementById("receipt-item").content.cloneNode(true);
        modal.querySelector(".receipt-items").appendChild(item_template);
    } else if (actionType === "edit") {
        modal.querySelector(".modal-title").textContent = "Edit receipt";
        const receiptID = button.getAttribute("data-receipt-id");
        form.action = `/edit-receipt/${receiptID}/`;
        fetch(`/api/receipts/${receiptID}`)
            .then(response => response.json())
            .then(data => {
                modal.querySelector("#receipt-name").value = data.name;
                modal.querySelector("#receipt-date").value = data.date;
                const items = data.items;
                for (let item of items) {
                    let item_template = document.getElementById("receipt-item").content.cloneNode(true);
                    item_template.querySelector('[name="receipt-items-name[]"]').value = item.name;
                    item_template.querySelector('[name="receipt-items-price[]"]').value = item.price;
                    let categoryField = item_template.querySelector('[name="receipt-items-category[]"]');
                    categoryField.value = item.category ? item.category : "";
                    modal.querySelector(".receipt-items").appendChild(item_template);
                }
            })
            .catch(error => {
                console.error("Error occurred:", error);
            });
    }
}

function addReceiptItem(button) {
    const modalBody = button.closest(".modal-body");
    const receiptItems = modalBody.querySelector(".receipt-items")
    const template = document.getElementById("receipt-item");
    const newItem = template.content.cloneNode(true);
    receiptItems.appendChild(newItem);
}

function deleteReceiptItem(button) {
    button.closest(".row").remove();
}