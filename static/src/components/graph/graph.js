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
                this.chart1.data.labels = this.props.graph_label;
                this.chart1.data.datasets[0].data = this.props.graph_data;
                this.chart1.data.datasets[0].backgroundColor = this.generateColors(this.props.graph_data.length);
                this.chart1.update();
            }
        }, () => [this.props.graph_data, this.props.graph_label]);

        onMounted(this.loadAndRenderChart);
        onWillUnmount(this.cleanupChart);
    }

    async loadAndRenderChart() {
        // Load Chart.js dynamically
        await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");

        if (!window.Chart) {
            
            return;
        }

        const ctx = this.chartCanvas.el.getContext("2d");

        this.chart1 = new window.Chart(ctx, {
            type: "bar",
            data: {
                labels: this.props.graph_label,
                datasets: [
                    {
                        label: "Total Amount per RFP",
                        data: this.props.graph_data,
                        backgroundColor: this.generateColors(this.props.graph_data.length),
                        borderColor: "#ffffff",
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top",
                    }
                }
            }
        });
    }

    generateColors(count) {
        // Generate a random color array for each slice
        return Array.from({ length: count }, () => `hsl(${Math.floor(Math.random() * 360)}, 70%, 60%)`);
    }

    cleanupChart() {
        if (this.chart1) {
            this.chart1.destroy();
        }
    }
}

ChartComponent.props = {
    graph_data: { type: Array },
    graph_label: { type: Array },
};

ChartComponent.template = "supplier_dashboard.ChartComponent";
