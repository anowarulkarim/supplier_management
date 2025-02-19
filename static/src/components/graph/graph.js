/** @odoo-module **/
import { Component, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class ChartComponent extends Component {
    setup() {
        this.chartCanvas = useRef("chartCanvas");
        this.chart1 = null;

        // Ensure chart updates when props change
        useEffect(() => {
            if (this.chart1) {
                this.chart1.data.datasets[0].data = [
                    this.props.total_rfq,
                    this.props.approvedRFQs,
                    this.props.totalAmount
                ];
                this.chart1.update();
            }
        }, () => [this.props.total_rfq, this.props.approvedRFQs, this.props.totalAmount]);

        onMounted(this.loadAndRenderChart);
        onWillUnmount(this.cleanupChart);
    }

    async loadAndRenderChart() {
        // Load Chart.js dynamically and wait until it's available
        await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");

        // Wait for Chart.js to be defined
        if (!window.Chart) {
            console.error("Chart.js failed to load");
            return;
        }

        const ctx = this.chartCanvas.el.getContext("2d");

        this.chart1 = new window.Chart(ctx, {  // Use `window.Chart` to avoid undefined issues
            type: "bar",
            data: {
                labels: ["Total RFQ", "Approved RFQs", "Total Amount"],
                datasets: [
                    {
                        label: "Supplier Metrics",
                        data: [this.props.total_rfq, this.props.approvedRFQs, this.props.totalAmount],
                        backgroundColor: ["#3498db", "#2ecc71", "#e74c3c"]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    cleanupChart() {
        if (this.chart1) {
            this.chart1.destroy();
        }
    }
}

ChartComponent.props = {
    total_rfq: { type: Number },
    approvedRFQs: { type: Number },
    totalAmount: { type: Number },
};

ChartComponent.template = "supplier_dashboard.ChartComponent";
