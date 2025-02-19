// import { Component, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

// async function loadChartJS() {
//     if (!window.Chart) {
//         await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");
//     }
// }

// export class ChartComponent extends Component {
//     setup() {
//         this.chartCanvas = useRef("chartCanvas");
//         this.chart = null;

//         // Ensure chart updates when props change
//         useEffect(() => {
//             if (this.chart) {
//                 this.chart.data.datasets[0].data = [
//                     this.props.total_rfq,
//                     this.props.approvedRFQs,
//                     this.props.totalAmount
//                 ];
//                 this.chart.update();
//             }
//         }, () => [this.props.total_rfq, this.props.approvedRFQs, this.props.totalAmount]);

//         onMounted(this.loadAndRenderChart);
//         onWillUnmount(this.cleanupChart);
//     }

//     async loadAndRenderChart() {
//         await loadChartJS();  // Ensure Chart.js is loaded
//         const ctx = this.chartCanvas.el.getContext("2d");

//         this.chart = new Chart(ctx, {
//             type: "bar",
//             data: {
//                 labels: ["Total RFQ", "Approved RFQs", "Total Amount"],
//                 datasets: [
//                     {
//                         label: "Supplier Metrics",
//                         data: [this.props.total_rfq, this.props.approvedRFQs, this.props.totalAmount],
//                         backgroundColor: ["#3498db", "#2ecc71", "#e74c3c"]
//                     }
//                 ]
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     cleanupChart() {
//         if (this.chart) {
//             this.chart.destroy();
//         }
//     }
// }

// ChartComponent.props = {
//     total_rfq: { type: Number },
//     approvedRFQs: { type: Number },
//     totalAmount: { type: Number },
// };

// ChartComponent.template = "supplier_dashboard.ChartComponent";
