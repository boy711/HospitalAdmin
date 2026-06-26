const body = document.querySelector("body");
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const modeToggle = document.getElementById("modeToggle");
const darkBtn = document.getElementById("darkBtn");
const darkIcon = document.getElementById("darkIcon");
const notifBtn = document.getElementById("notifBtn");
const notifDot = document.getElementById("notifDot");
const searchInput = document.getElementById("searchInput");

// ===== Restore saved state on load =====
const getMode = localStorage.getItem("mode");
if (getMode === "dark") {
    body.classList.add("dark");
    darkIcon.className = "uil uil-sun";
}

const getStatus = localStorage.getItem("status");
if (getStatus === "close") {
    sidebar.classList.add("close");
}

// ===== Dark Mode — single source of truth, saved to localStorage =====
function toggleDark() {
    body.classList.toggle("dark");
    const isDark = body.classList.contains("dark");
    darkIcon.className = isDark ? "uil uil-sun" : "uil uil-moon";
    localStorage.setItem("mode", isDark ? "dark" : "light");
}
darkBtn.addEventListener("click", toggleDark);
modeToggle.addEventListener("click", toggleDark);

// ===== Sidebar Toggle — saved to localStorage =====
sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    localStorage.setItem("status", sidebar.classList.contains("close") ? "close" : "open");
});

// ===== Notifications — click to clear/restore dot =====
notifBtn.addEventListener("click", () => {
    notifDot.style.display = notifDot.style.display === "none" ? "block" : "none";
});

// ===== User Dropdown =====
const userSection = document.getElementById("userSection");
const userDropdown = document.getElementById("userDropdown");
const userChevron = document.getElementById("userChevron");

userSection.addEventListener("click", function(e) {
    userDropdown.classList.toggle("open");
    userChevron.style.transform = userDropdown.classList.contains("open") ? "rotate(180deg)" : "rotate(0deg)";
    e.stopPropagation();
});

// Close dropdown when clicking outside
document.addEventListener("click", function() {
    userDropdown.classList.remove("open");
    userChevron.style.transform = "rotate(0deg)";
});

// Logout confirm
document.getElementById("logoutForm").addEventListener("submit", function(e) {
    if (!confirm("Are you sure you want to logout?")) {
        e.preventDefault();
    }
});

// ===== Live Search — highlights matching rows =====
searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();
    document.querySelectorAll(".data-list").forEach(item => {
        item.classList.remove("highlight");
        if (query && item.textContent.toLowerCase().includes(query)) {
            item.classList.add("highlight");
        }
    });
});