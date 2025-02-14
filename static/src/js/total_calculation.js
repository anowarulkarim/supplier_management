document.addEventListener("DOMContentLoaded", function () {
    // Function to calculate the total
    function calculateTotal(row) {
        let quantity = parseFloat(row.querySelector("input[name^='quantity_']").value) || 0;
        let unitPrice = parseFloat(row.querySelector("input[name^='unit_price_']").value) || 0;
        let deliveryCharges = parseFloat(row.querySelector("input[name^='delivery_charges_']").value) || 0;

        let total = (quantity * unitPrice) + deliveryCharges;
        row.querySelector("input[name^='total_']").value = total.toFixed(2);
    }

    // Attach event listeners to quantity, unit price, and delivery charges inputs
    document.querySelectorAll("tbody tr").forEach(row => {
        row.querySelectorAll("input[name^='quantity_'], input[name^='unit_price_'], input[name^='delivery_charges_']").forEach(input => {
            input.addEventListener("input", function () {
                calculateTotal(row);
            });
        });
    });
});