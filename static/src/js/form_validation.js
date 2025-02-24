document.getElementById("tax_identification_number").addEventListener("keyup", function (event) {
    let tinField = document.getElementById("tax_identification_number");
    let errorMsg = document.getElementById("tin_error_msg");

    let tin = tinField.value.trim();
    let numericRegex = /^[0-9]+$/;

    if (tin.length !== 16 || !numericRegex.test(tin)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("company_name").addEventListener("keyup", function (event) {
    let companyNameField = document.getElementById("company_name");
    let errorMsg = document.getElementById("company_name_error_msg");

    let companyName = companyNameField.value.trim();
    console.log("companyName");
    if (companyName.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    }else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});    

document.getElementById("company_registered_address").addEventListener("keyup", function (event) {
    let companyAddressField = document.getElementById("company_registered_address");
    let errorMsg = document.getElementById("company_registered_address_error_msg");

    let companyAddress = companyAddressField.value.trim();
    console.log("companyAddress");
    if (companyAddress.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("trade_license_number").addEventListener("keyup", function (event) {
    let tradeLicenseField = document.getElementById("trade_license_number");
    let errorMsg = document.getElementById("trade_license_error_msg");

    let tradeLicense = tradeLicenseField.value.trim();
    let alphanumericRegex = /^[a-z0-9]+$/i;

    if (tradeLicense.length < 8 || tradeLicense.length > 20 || !alphanumericRegex.test(tradeLicense)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("commencement_date").addEventListener("change", function (event) {
    let commencementDateField = document.getElementById("commencement_date");
    let errorMsg = document.getElementById("commencement_date_error_msg");
    let commencementDate = new Date(commencementDateField.value);
    let today = new Date();
    today.setHours(0, 0, 0, 0); // Set to the start of today

    if (commencementDate >= today) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("expiry_date").addEventListener("change", function (event) {
    let expiryDateField = document.getElementById("expiry_date");
    let errorMsg = document.getElementById("expiry_date_error_msg");

    let expiryDate = new Date(expiryDateField.value);
    let today = new Date();
    today.setHours(0, 0, 0, 0); // Set to the start of today

    if (expiryDate <= today) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("signatory_name").addEventListener("keyup", function (event) {
    let signatoryNameField = document.getElementById("signatory_name");
    let errorMsg = document.getElementById("signatory_name_error_msg");
    console.log("asdfjklaskdfjl")

    let signatoryName = signatoryNameField.value.trim();
    if (signatoryName.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("authorized_signatory").addEventListener("keyup", function (event) {
    let authorizedSignatoryField = document.getElementById("authorized_signatory");
    let errorMsg = document.getElementById("authorized_signatory_error_msg");

    let authorizedSignatory = authorizedSignatoryField.value.trim();
    if (authorizedSignatory.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});


document.getElementById("contact_person_title").addEventListener("keyup", function (event) {
    let contactPersonTitleField = document.getElementById("contact_person_title");
    let errorMsg = document.getElementById("contact_person_title_error_msg");

    let contactPersonTitle = contactPersonTitleField.value.trim();
    if (contactPersonTitle.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("contact_email").addEventListener("keyup", function (event) {
    let contactEmailField = document.getElementById("contact_email");
    let errorMsg = document.getElementById("contact_email_error_msg");

    let contactEmail = contactEmailField.value.trim();
    let emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;

    if (contactEmail.length == 0 || !emailRegex.test(contactEmail)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("contact_phone").addEventListener("keyup", function (event) {
    let contactPhoneField = document.getElementById("contact_phone");
    let errorMsg = document.getElementById("contact_phone_error_msg");

    let contactPhone = contactPhoneField.value.trim();
    let phoneRegex = /^[0-9]+$/;

    if (contactPhone.length == 0 || !phoneRegex.test(contactPhone)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("contact_address").addEventListener("keyup", function (event) {
    let contactAddressField = document.getElementById("contact_address");
    let errorMsg = document.getElementById("contact_address_error_msg");

    let contactAddress = contactAddressField.value.trim();
    if (contactAddress.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("finance_contact_title").addEventListener("keyup", function (event) {
    let financeContactTitleField = document.getElementById("finance_contact_title");
    let errorMsg = document.getElementById("finance_contact_title_error_msg");

    let financeContactTitle = financeContactTitleField.value.trim();
    if (financeContactTitle.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("finance_contact_email").addEventListener("keyup", function (event) {
    let financeContactEmailField = document.getElementById("finance_contact_email");
    let errorMsg = document.getElementById("finance_contact_email_error_msg");

    let financeContactEmail = financeContactEmailField.value.trim();
    let emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;

    if (financeContactEmail.length == 0 || !emailRegex.test(financeContactEmail)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("finance_contact_phone").addEventListener("keyup", function (event) {
    let financeContactPhoneField = document.getElementById("finance_contact_phone");
    let errorMsg = document.getElementById("finance_contact_phone_error_msg");

    let financeContactPhone = financeContactPhoneField.value.trim();
    let phoneRegex = /^[0-9]+$/;

    if (financeContactPhone.length == 0 || !phoneRegex.test(financeContactPhone)) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("finance_contact_address").addEventListener("keyup", function (event) {
    let financeContactAddressField = document.getElementById("finance_contact_address");
    let errorMsg = document.getElementById("finance_contact_address_error_msg");

    let financeContactAddress = financeContactAddressField.value.trim();
    if (financeContactAddress.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("authorized_person_name").addEventListener("keyup", function (event) {
    let authorizedPersonNameField = document.getElementById("authorized_person_name");
    let errorMsg = document.getElementById("authorized_person_name_error_msg");

    let authorizedPersonName = authorizedPersonNameField.value.trim();
    if (authorizedPersonName.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    } else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("authorized_person_email").addEventListener("keyup", function (event) {
    let authorizedPersonEmailField = document.getElementById("authorized_person_email");
    let errorMsg = document.getElementById("authorized_person_email_error_msg");

    let authorizedPersonEmail = authorizedPersonEmailField.value.trim();
    let emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;

    if (authorizedPersonEmail.length == 0 || !emailRegex.test(authorizedPersonEmail)) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("authorized_person_phone").addEventListener("keyup", function (event) {
    let authorizedPersonPhoneField = document.getElementById("authorized_person_phone");
    let errorMsg = document.getElementById("authorized_person_phone_error_msg");

    let authorizedPersonPhone = authorizedPersonPhoneField.value.trim();
    let phoneRegex = /^[0-9]+$/;

    if (authorizedPersonPhone.length == 0 || !phoneRegex.test(authorizedPersonPhone)) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("authorized_person_address").addEventListener("keyup", function (event) {
    let authorizedPersonAddressField = document.getElementById("authorized_person_address");
    let errorMsg = document.getElementById("authorized_person_address_error_msg");

    let authorizedPersonAddress = authorizedPersonAddressField.value.trim();
    if (authorizedPersonAddress.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});


document.getElementById("bank_name").addEventListener("keyup", function (event) {
    let bankNameField = document.getElementById("bank_name");
    let errorMsg = document.getElementById("bank_name_error_msg");

    let bankName = bankNameField.value.trim();
    if (bankName.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("bank_address").addEventListener("keyup", function (event) {
    let bankAddressField = document.getElementById("bank_address");
    let errorMsg = document.getElementById("bank_address_error_msg");

    let bankAddress = bankAddressField.value.trim();
    if (bankAddress.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

document.getElementById("account_number").addEventListener("keyup", function(event){
    let accountNumberField = document.getElementById("account_number");
    let errorMsg = document.getElementById("account_number_error_msg");

    let accountNumber = accountNumberField.value.trim();
    
    if (accountNumber.length == 0) {
        errorMsg.style.display = "block";  // Show the error message
    }
    else {
        errorMsg.style.display = "none";   // Hide the error message
    }
});

















// document.getElementById("file_input").addEventListener("change", function (event) {
//     let fileInput = document.getElementById("file_input");
//     let errorMsg = document.getElementById("file_error_msg");

//     let file = fileInput.files[0];
//     if (file && file.size > 1048576) { // Check if file size is greater than 1MB (1048576 bytes)
//         errorMsg.style.display = "block";  // Show the error message
//     } else {
//         errorMsg.style.display = "none";   // Hide the error message
//     }
// });