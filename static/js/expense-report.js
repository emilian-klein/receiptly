document.addEventListener("DOMContentLoaded", function () {
    addEventListenerOnStartDateInput();
    addEventListenerOnEndDateInput();
    addEventListenerOnSubmitForm("expense-report-time-range-form");
    addEventListenerOnToastElement("expense-report-toast");
});

function addEventListenerOnStartDateInput() {
    const startDateInput = document.getElementById("expense-report-start-date");
    if (startDateInput) {
        startDateInput.addEventListener("input", function () {
            limitEndDateInput(startDateInput.value);
        });
    }
}

function limitEndDateInput(startDate) {
    const endDateInput = document.getElementById("expense-report-end-date");
    if (endDateInput) {
        endDateInput.min = startDate ? startDate : "";
    }
}

function addEventListenerOnEndDateInput() {
    const endDateInput = document.getElementById("expense-report-end-date");
    if (endDateInput) {
        endDateInput.addEventListener("input", function () {
            limitStartDateInput(endDateInput.value);
        });
    }
}

function limitStartDateInput(endDate) {
    const startDateInput = document.getElementById("expense-report-start-date");
    if (startDateInput) {
        startDateInput.max = endDate ? endDate : "";
    }
}