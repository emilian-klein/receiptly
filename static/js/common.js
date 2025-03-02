function addEventListenerOnSubmitForm(formID) {
    const form = document.getElementById(formID);
    form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add("was-validated");
    });
}

function addEventListenerOnToastElement(toastID) {
    const toastElement = document.getElementById(toastID);
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
}