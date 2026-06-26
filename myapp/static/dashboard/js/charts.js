// ===== Sample Data =====
const weeklyData = {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
    appointments: [22, 28, 20, 35, 31],
    patients: [45, 52, 38, 61, 55]
};

const departmentData = {
    labels: ["Cardiology", "Orthopedics", "Neurology", "General"],
    values: [320, 280, 210, 190],
    colors: ["#6366f1", "#06b6d4", "#22c55e", "#f97316"]
};

// ===== Theme-aware text/grid color for charts =====
function getChartColors() {
    const isDark = document.body.classList.contains("dark");
    return {
        text: isDark ? "#CCC" : "#444",
        grid: isDark ? "#3a3b3c" : "#eee"
    };
}

let weeklyChart, departmentChart;

function renderCharts() {
    const colors = getChartColors();

    // Destroy old instances before re-rendering (needed for dark mode redraw)
    if (weeklyChart) weeklyChart.destroy();
    if (departmentChart) departmentChart.destroy();

    // ===== Weekly Activity — Bar Chart =====
    const weeklyCtx = document.getElementById("weeklyActivityChart");
    if (weeklyCtx) {
        weeklyChart = new Chart(weeklyCtx, {
            type: "bar",
            data: {
                labels: weeklyData.labels,
                datasets: [
                    {
                        label: "appointments",
                        data: weeklyData.appointments,
                        backgroundColor: "#6366f1",
                        borderRadius: 4
                    },
                    {
                        label: "patients",
                        data: weeklyData.patients,
                        backgroundColor: "#06b6d4",
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: colors.text }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: colors.text },
                        grid: { display: false }
                    },
                    y: {
                        ticks: { color: colors.text },
                        grid: { color: colors.grid }
                    }
                }
            }
        });
    }

    // ===== Department Distribution — Pie Chart =====
    const deptCtx = document.getElementById("departmentChart");
    if (deptCtx) {
        departmentChart = new Chart(deptCtx, {
            type: "pie",
            data: {
                labels: departmentData.labels,
                datasets: [{
                    data: departmentData.values,
                    backgroundColor: departmentData.colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // ===== Build custom legend with patient counts =====
    const legendEl = document.getElementById("departmentLegend");
    if (legendEl) {
        legendEl.innerHTML = "";
        departmentData.labels.forEach((label, i) => {
            const li = document.createElement("li");
            li.innerHTML = `<span class="dot" style="background:${departmentData.colors[i]}"></span> ${label}: ${departmentData.values[i]} patients`;
            legendEl.appendChild(li);
        });
    }
}

// Initial render
document.addEventListener("DOMContentLoaded", renderCharts);

// Re-render charts whenever dark mode toggles, so colors update live
const originalToggleDark = toggleDark;
toggleDark = function () {
    originalToggleDark();
    renderCharts();
};
darkBtn.removeEventListener("click", originalToggleDark);
modeToggle.removeEventListener("click", originalToggleDark);
darkBtn.addEventListener("click", toggleDark);
modeToggle.addEventListener("click", toggleDark);
