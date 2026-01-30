// Fake live counters (replace later with backend data)
let attendance = 0;
let waste = 0;

setInterval(() => {
    attendance = Math.floor(Math.random() * 100);
    waste = Math.floor(Math.random() * 20);

    document.getElementById("attendance-count").innerText = attendance;
    document.getElementById("waste-count").innerText = waste;
}, 3000);

// Chart
const ctx = document.getElementById('statsChart');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
            label: 'Food Waste Cases',
            data: [3, 7, 4, 6, 2],
            borderWidth: 2,
            borderColor: '#38bdf8',
            fill: false,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        },
        scales: {
            x: {
                ticks: { color: 'white' }
            },
            y: {
                ticks: { color: 'white' }
            }
        }
    }
});
