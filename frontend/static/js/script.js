document.addEventListener("DOMContentLoaded", function () {
    let sidebar = document.querySelector(".sidebar");
    let sidebarBtn = document.querySelector(".sidebarBtn");
  
    // Ensure both elements exist
    if (sidebar && sidebarBtn) {
      // Check if the sidebar state is stored in local storage
      const isSidebarActive = localStorage.getItem("isSidebarActive") === "true";
      if (isSidebarActive) {
        sidebar.classList.add("active");
        sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
      }
  
      sidebarBtn.onclick = function () {
        sidebar.classList.toggle("active");
        if (sidebar.classList.contains("active")) {
          sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
          // Save the sidebar state to local storage
          localStorage.setItem("isSidebarActive", "true");
        } else {
          sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
          // Save the sidebar state to local storage
          localStorage.setItem("isSidebarActive", "false");
        }
      };
    } else {
      console.error("Sidebar or Sidebar Button elements not found.");
    }
  });
  
  document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const toggleIcon = this.querySelector('i');

    // Toggle password visibility
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('bx-show');
        toggleIcon.classList.add('bx-hide'); // Change icon to "hide"
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('bx-hide');
        toggleIcon.classList.add('bx-show'); // Change icon to "show"
    }
});
  