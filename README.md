# Supplier Management System

## Overview
The **Supplier Management System** is an Odoo 17-based module designed to streamline supplier registration, Request for Purchase (RFP) handling, and quotation management. It ensures efficient supplier onboarding, RFP publishing, and evaluation processes while providing insightful reporting and an interactive dashboard for better decision-making.

## Features

### 1. Email Verification & Two-Step Verification
- Email sign-up with OTP validation.
- Blacklist verification before registration.
- Two-step verification for supplier account creation.

### 2. Supplier Registration
- A structured **supplier registration form** with five sections:
  1. Company Information (Name, Address, Contact Details, TIN, etc.)
  2. Financial Information (Bank Name, Account Details, SWIFT Code, IBAN, etc.)
  3. Previous Client References (Up to 5 clients)
  4. Certification Details (Name, Number, Certifying Body, Validity, etc.)
  5. Document Submission (Trade License, Tax Certificate, etc.)
- Validation checks for required fields and file size limits.
- Authorized signatory declaration before submission.
- Automatic system validation before submission.
- Email notifications for reviewers upon new submissions.

### 3. RFP (Request for Purchase) Management
- RFP creation, submission, and approval process.
- Reviewer-based access control:
  - **Reviewer**: Can create, submit, and recommend RFPs.
  - **Approver**: Can approve, reject, or close RFPs.
- Linked RFQ (Request for Quotation) lines to track supplier quotations.
- Notification system for approvals and supplier updates.

### 4. Quotation Management
- Quotation submission against RFPs by suppliers.
- Scoring system for evaluating quotations based on delivery, pricing, and terms.
- Recommendation process for selecting the best supplier.
- Automatic RFQ-to-RFP linkage.

### 5. Reporting System
- Generate **RFP Reports** with filtering options based on suppliers and date range.
- Generate reports in **QWeb HTML preview** and **Excel format**.
- Multi-section report structure including:
  - Company and Supplier Details
  - RFP Summary
  - Product-wise Breakdown
  - Financial Summary
- Automatic validation and exception handling for missing data.

### 6. Data Visualization & Dashboard
- **Dynamic OWL-based Dashboard** with interactive charts and graphs.
- Key metrics displayed:
  - **Approved RFQs**
  - **Total Spend Amount**
  - **Product-wise Breakdown**
- Graphical representations:
  - **Line Charts & Bar Graphs** for RFP data.
  - **Pivot Tables** for supplier-wise and status-wise analysis.
- Real-time updates and date filtering options.

## User Roles & Access Control
- **Supplier**
  - Register, view profile, submit quotations.
- **Reviewer**
  - Create and review RFPs, review supplier registration, and score quotations.
- **Approver**
  - Approve/reject supplier registrations and RFPs.

## Technologies Used
- **Odoo 17** (Backend & Frontend)
- **Python** (Business Logic & ORM)
- **PostgreSQL** (Database)
- **OWL (Odoo Web Library)** (Frontend UI Components)
- **JavaScript & XML** (Templates & Views)
- **QWeb** (Report Generation)

## How to Use
1. **Register as a Supplier** through the portal.
2. **Submit RFPs** with relevant details and document attachments.
3. **Review & Approve Supplier Applications** based on verification.
4. **Manage Quotations** by evaluating supplier proposals.
5. **Analyze Supplier & RFP Data** through the dashboard and reports.

## Guidelines
- Follow Odoo’s official [coding guidelines](https://www.odoo.com/documentation/17.0/contributing/development/coding_guidelines.html).

---
This module provides a structured supplier management workflow to optimize procurement and supplier evaluation processes within Odoo.


## Installation
1. Clone the repository:
2. Move the module to your Odoo addons directory.
3. Restart the Odoo server:
   ```sh
   odoo-bin -c /etc/odoo.conf -u supplier_management
   ```
4. Activate the module from the Odoo Apps menu.

## Usage
1. Navigate to **Supplier Management** in the Odoo backend.
2. Register new suppliers and approve/reject applications.
3. Create and manage RFPs and link them to RFQs.
4. Track supplier performance and quotation details.

## Contributing
If you'd like to contribute, please fork the repository and submit a pull request.
