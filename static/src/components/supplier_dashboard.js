// import { Component } from '@odoo/owl';
// import { registry } from '@odoo/owl';

/** @odoo-module **/

import {registry} from "@web/core/registry"
class SupplierDashboard extends Component {
    static template = 'SupplierDashboard';
    setup() {
        
    }
}

SupplierDashboard.template = "owl.SupplierDashboard"

export default SupplierDashboard;
registry.category("actions").add("owl.supplier_dashboard",SupplierDashboard)