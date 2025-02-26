/** @odoo-module **/
import { ChartComponent } from "./graph/graph";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component } from '@odoo/owl';
import { registry } from "@web/core/registry";
import { Card } from './card/card';
import { Product } from "./product/product";

const { onWillStart, useRef, onMounted, useState } = owl;

class SupplierDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        this.state = useState({
            all_rfqs: [],
            suppliers: [],
            selectedSupplier: null,
            dateRange: "this_week",
            total_rfq: 0,
            approvedRFQs: 0,
            totalAmount: 0,
            productBreakdown: [],
            grap_type: "bar",
            graph_lebel: [],
            graph_data: [],
            searchQuery: "", // New state for search query
        });

        onWillStart(async () => {
            this.state.suppliers = await this.fetchSuppliers();
            await this.fetchMetrics();
        });
    }

    async fetchSuppliers() {
        try {
            const suppliers = await this.orm.searchRead(
                "res.partner",
                [["supplier_rank", ">", 0]], // ✅ Only fetch suppliers
                ["id", "name"]
            );
            return suppliers;
        } catch (error) {
            
            return [];
        }
    }

    async fetchMetrics() {
        if (!this.state.selectedSupplier) return;

        const dateFilter = this.getDateFilter();
        const supplierId = this.state.selectedSupplier;

        try {
            const poDomain = [
                ["partner_id", "=", supplierId], // Supplier
                ["state", "=", "purchase"], // Approved RFQs only
                ["date_order", ">=", dateFilter[0]], // Start Date
                ["date_order", "<=", dateFilter[1]]  // End Date
            ];
            const rfqDomain = [
                ["partner_id", "=", supplierId], // Supplier
                ["date_order", ">=", dateFilter[0]], // Start Date
                ["date_order", "<=", dateFilter[1]]  // End Date
            ];

            let t = [];
            let d = [];
            const rfqs = await this.orm.searchRead("purchase.order", poDomain, ["id", "amount_total", "order_line", "rfp_id"]);
            const total_rfqs = await this.orm.searchRead("purchase.order", rfqDomain, ["id", "amount_total"]);
            this.state.all_rfqs = rfqs;

            rfqs.forEach(element => {
                if (element.rfp_id) {
                    t.push(element.rfp_id[1]);
                } else {
                    t.push("Unknown");
                }
                d.push(element.amount_total || 0);
            });

            this.state.graph_data = d;
            this.state.graph_lebel = t;

            const orderLineIds = rfqs.flatMap(rfq => rfq.order_line);
            const orderLines = await this.orm.searchRead("purchase.order.line", [["id", "in", orderLineIds]], ["id", "product_id", "product_qty", "price_unit","delivery_charge"]);
            const productFrequency = {};

            const productIds = orderLines.map(line => line.product_id[0]);
            const products = await this.orm.searchRead("product.product", [["id", "in", productIds]], ["id", "image_1920"]);

            const productImageMap = {};
            products.forEach(product => {
                productImageMap[product.id] = product.image_1920;
            });

            let amount = 0;
            orderLines.forEach(line => {
                const productId = line.product_id[0];

                if (!productFrequency[productId]) {
                    productFrequency[productId] = {
                        product_id: line.product_id,
                        product_qty: 0,
                        total_amount: 0,
                        image: productImageMap[productId] || null
                    };
                }
                productFrequency[productId].product_qty += line.product_qty;
                productFrequency[productId].total_amount += line.product_qty * line.price_unit;
                amount += productFrequency[productId].total_amount;
                // amount += line.delivery_charge;
            });

            this.state.productBreakdown = Object.values(productFrequency);

            this.state.total_rfq = total_rfqs.length;
            this.state.approvedRFQs = rfqs.length;
            this.state.totalAmount = amount;
        } catch (error) {
            var a=10;
        }
    }

    getDateFilter() {
        const today = new Date();
        let startDate, endDate = new Date(today);

        switch (this.state.dateRange) {
            case "this_week":
                startDate = new Date(today);
                startDate.setDate(today.getDate() - today.getDay() + (today.getDay() === 0 ? -6 : 1)); 
                break;
            case "last_week":
                startDate = new Date(today);
                startDate.setDate(today.getDate() - today.getDay() - 6);
                endDate.setDate(endDate.getDate() - today.getDay() - (today.getDay() === 0 ? 0 : 1)); 
                break;
            case "last_month":
                startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                endDate = new Date(today.getFullYear(), today.getMonth(), 0);
                break;
            case "last_year":
                startDate = new Date(today.getFullYear() - 1, 0, 1);
                endDate = new Date(today.getFullYear() - 1, 11, 31);
                break;
            case "this_month":
                startDate = new Date(today.getFullYear(), today.getMonth(), 1);
                endDate = new Date(today);
                break;
            default:
                startDate = new Date(today);
                endDate = new Date(today);
        }

        return [
            startDate.toISOString().split("T")[0], 
            endDate.toISOString().split("T")[0]
        ];
    }

    onSupplierChange(event) {
        this.state.selectedSupplier = parseInt(event.target.value);
        this.fetchMetrics();
    }

    onDateRangeChange(event) {
        this.state.dateRange = String(event.target.value);
        this.fetchMetrics();
    }

    // Search handler
    onSearchQueryChange(event) {
        this.state.searchQuery = event.target.value;
        
    }

    get filteredProducts() {
        
        if (!this.state.searchQuery) {
            return this.state.productBreakdown;
        }
        const filtered = this.state.productBreakdown.filter(product =>
            product.product_id[1].toLowerCase().includes(this.state.searchQuery.toLowerCase())
        );
        
        return filtered;
    }
}

SupplierDashboard.template = "owl.SupplierDashboard";
SupplierDashboard.components = { Card, Product, ChartComponent };

registry.category("actions").add("owl.supplier_dashboard", SupplierDashboard);

export default SupplierDashboard;