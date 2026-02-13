// Color beds red if 0
const beds = document.querySelectorAll(".beds");

beds.forEach(bed => {
  if (bed.innerText.trim() === "0") {
    bed.style.color = "red";
  }
});

// Logout confirmation
function confirmLogout() {
  return confirm("Are you sure you want to logout?");
}
<script src="{{ url_for('static', filename='script.js') }}"></script>
