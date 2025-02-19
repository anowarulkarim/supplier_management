/** @odoo-module **/
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
const { onWillStart, useRef, onMounted, useState } = owl
import { Component } from '@odoo/owl';
import {registry} from "@web/core/registry"
import { Card } from './card/card'


class SupplierDashboard extends Component {
    setup() {
        this.orm = useService("orm")

        this.state = useState({
            all_rfqs:[],
            suppliers: [],
            selectedSupplier: null,
            dateRange: "this_week",
            total_rfq: 0,
            approvedRFQs: 0,
            totalAmount: 0,
            productBreakdown: [],
        });
        onWillStart(async () => {
            this.state.suppliers = await this.fetchSuppliers();
            await this.fetchMetrics();
            console.log("State Updated:", this.state.suppliers); // ✅ Debugging output
        });

        console.log(this.state.suppliers)
    }
    async fetchSuppliers() {
        try {
            const suppliers = await this.orm.searchRead(
                "res.partner",
                [["supplier_rank", ">", -1]], // ✅ Only fetch suppliers
                ["id", "name"]
            );
            // console.log("Fetched Suppliers:", suppliers); // ✅ Debugging output
            // suppliers.forEach(supplier => {
            //     console.log("Supplier:", supplier);
            // });
            return suppliers;
        } catch (error) {
            console.error("Error fetching suppliers:", error);
            return [];
        }
    }
    
    async fetchMetrics() {
        console.log("sdfkjlk")
        if (!this.state.selectedSupplier) return;


        const dateFilter = this.getDateFilter();
        const supplierId = this.state.selectedSupplier;
        
        console.log(dateFilter,supplierId)

        try {

            const poDomain = [
                ["partner_id", "=", supplierId], // Supplier
                ["state", "=", "purchase"], // Approved RFQs only
                ["date_order", ">=", dateFilter[0]], // Start Date
                ["date_order", "<=", dateFilter[1]]  // End Date
            ];
            console.log(dateFilter[0],dateFilter[1])
            const rfqDomain = [
                ["partner_id", "=", supplierId], // Supplier
                ["date_order", ">=", dateFilter[0]], // Start Date
                ["date_order", "<=", dateFilter[1]]  // End Date
            ];
            console.log("kjjjhasdf")

            

            const rfqs = await this.orm.searchRead("purchase.order", poDomain, ["id", "amount_total","order_line"]);
            const total_rfqs = await this.orm.searchRead("purchase.order", rfqDomain, ["id", "amount_total"]);
            console.log("rfps     as",rfqs)
            this.state.all_rfqs=rfqs
            
            rfqs.forEach(element => {
                console.log(element.order_line)
                element.order_line.forEach(a=>{
                    console.log(typeof(element.order_line))
                });
            });

            const orderLineIds = rfqs.flatMap(rfq => rfq.order_line);
            const orderLines = await this.orm.searchRead("purchase.order.line", [["id", "in", orderLineIds]], ["id", "product_id", "product_qty", "price_unit"]);
            console.log("Order Lines:", orderLines);
            const productFrequency = {};

            orderLines.forEach(line => {
                const productId = line.product_id[0];
                console.log()
                if (!productFrequency[productId]) {
                    productFrequency[productId] = {
                        product_id: line.product_id,
                        product_qty: 0,
                        total_amount: 0
                    };
                }
                productFrequency[productId].product_qty += line.product_qty;
                productFrequency[productId].total_amount += line.product_qty * line.price_unit;
            });

            this.state.productBreakdown = Object.values(productFrequency);
            console.log("Product Break Down",this.state.productBreakdown)


            this.state.total_rfq=total_rfqs.length;
            this.state.approvedRFQs = rfqs.length;
            // this.state.totalAmount = data.totalAmount;
            // this.state.productBreakdown = data.productBreakdown;
            
            
        } catch (error) {
            console.error("Error fetching metrics:", error);
        }
    }
    get_product_lines(){

    }

    getDateFilter() {
        const today = new Date();
        let startDate, endDate = new Date(today);
    
        switch (this.state.dateRange) {
            case "this_week":
                // Start from the beginning of this week (Monday)
                startDate = new Date(today);
                startDate.setDate(today.getDate() - today.getDay() + (today.getDay() === 0 ? -6 : 1)); // Monday is 1 in getDay()
                break;
            case "last_week":
                // Start from the beginning of last week (Monday)
                startDate = new Date(today);
                startDate.setDate(today.getDate() - today.getDay() - 6);
                // End at the end of last week (Sunday)
                endDate.setDate(endDate.getDate() - today.getDay() - (today.getDay() === 0 ? 0 : 1)); // Sunday is 0 in getDay()
                break;
            case "last_month":
                // Start from the first day of last month
                startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                // End date should be the last day of last month
                endDate = new Date(today.getFullYear(), today.getMonth(), 0);
                break;
            case "last_year":
                // Start from the first day of last year
                startDate = new Date(today.getFullYear() - 1, 0, 1);
                // End date should be the last day of last year
                endDate = new Date(today.getFullYear() - 1, 11, 31);
                break;

            case "this_month":
                    // Start from the first day of this month
                startDate = new Date(today.getFullYear(), today.getMonth(), 1);
                    // End date is today
                endDate = new Date(today);
                break;
            
            default:
                // Default case, using today as both start and end
                startDate = new Date(today);
                endDate = new Date(today);
        }
    
        // Return the dates formatted as YYYY-MM-DD strings
        return [
            startDate.toISOString().split("T")[0], 
            endDate.toISOString().split("T")[0]
        ];
    }
    onSupplierChange(event) {
        this.state.selectedSupplier = parseInt(event.target.value);
        this.fetchMetrics();
        console.log("here it is", this.state.selectedSupplier)
    }

    onDateRangeChange(event) {
        this.state.dateRange = String(event.target.value);
        this.fetchMetrics();
        console.log("here it is for date", this.state.dateRange)
    }
}

SupplierDashboard.template = "owl.SupplierDashboard"
SupplierDashboard.components = { Card }

registry.category("actions").add("owl.supplier_dashboard",SupplierDashboard)

export default SupplierDashboard;

