// static/src/js/form_navigation.js
// JavaScript for handling form step navigation
document.getElementById("next-1").onclick = function() {
    document.getElementById("step-1").style.display = "none";
    document.getElementById("step-2").style.display = "block";
};

document.getElementById("prev-2").onclick = function() {
    document.getElementById("step-2").style.display = "none";
    document.getElementById("step-1").style.display = "block";
};

document.getElementById("next-2").onclick = function() {
    document.getElementById("step-2").style.display = "none";
    document.getElementById("step-3").style.display = "block";
};

document.getElementById("prev-3").onclick = function() {
    document.getElementById("step-3").style.display = "none";
    document.getElementById("step-2").style.display = "block";
};

document.getElementById("next-3").onclick = function() {
    document.getElementById("step-3").style.display = "none";
    document.getElementById("step-4").style.display = "block";
};

document.getElementById("prev-4").onclick = function() {
    document.getElementById("step-4").style.display = "none";
    document.getElementById("step-3").style.display = "block";
};

document.getElementById("next-4").onclick = function() {
    document.getElementById("step-4").style.display = "none";
    document.getElementById("step-5").style.display = "block";
};

document.getElementById("prev-5").onclick = function() {
    document.getElementById("step-5").style.display = "none";
    document.getElementById("step-4").style.display = "block";
};



document.getElementById("tax_identification_number").addEventListener("keyup", function (event) {
    let tinField = document.getElementById("tax_identification_number");
    let errorMsg = document.getElementById("tin_error_msg");

    let tin = tinField.value.trim();
    
    if (tin.length !== 10) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});
