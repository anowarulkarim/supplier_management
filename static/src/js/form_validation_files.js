
const fileFields = [
    'trade_license_business_registration', 'certificate_of_incorporation', 'certificate_of_good_standing',
    'establishment_card', 'vat_tax_certificate', 'memorandum_of_association',
    'identification_document_for_authorized_person', 'bank_letter_indicating_bank_account',
    'past_2_years_audited_financial_statements', 'other_certifications'
];

fileFields.forEach(field => {
    document.getElementById(field).addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file && file.size > 1048576) { // 1 MB in bytes
            alert('File size should not exceed 1 MB');
            event.target.value = ''; // Clear the input
        }
    });
});


document.getElementById("image_1920").addEventListener('change', function(event) {
    let file = document.getElementById("image_1920");
    let file_error_msg = document.getElementById("image_1920_error_msg");
    if (!file) {
        file_error_msg.style.display="block";
    }
    else {
        file_error_msg.style.display="none";
    }
});

document.getElementById("company_stamp_and_date").addEventListener('change', function(event) {
    let file = document.getElementById("company_stamp_and_date");
    let file_error_msg = document.getElementById("company_stamp_and_date_error_msg");
    if (!file) {
        file_error_msg.style.display="block";
    }
    else {
        file_error_msg.style.display="none";
    }
});