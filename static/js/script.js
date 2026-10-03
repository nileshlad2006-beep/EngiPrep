// const semesters = [
//   { name: "Sem 1", score: 8.23 },
//   { name: "Sem 2", score: 8.80 },
//   { name: "Sem 3", score: 8.50 },
//   { name: "Sem 4", score: 8.20 },
//   { name: "Sem 5", score: 8.00 },
//   { name: "Sem 6", score: 8.50 },
//   { name: "Sem 7", score: 8.00 },
//   { name: "Sem 8", score: 8.00 }
// ];

// const bars = document.getElementById("semesterBars");
// const semesterList = document.getElementById("semesterList");

// semesters.forEach((item) => {
//   const wrap = document.createElement("div");
//   wrap.className = "bar-wrap";

//   const bar = document.createElement("div");
//   bar.className = "bar";
//   bar.style.height = `${item.score * 9.8}%`;
//   bar.dataset.score = item.score.toFixed(2);

//   const label = document.createElement("span");
//   label.className = "semester-label";
//   label.textContent = item.name;

//   wrap.style.position = "relative";
//   wrap.appendChild(bar);
//   wrap.appendChild(label);
//   bars.appendChild(wrap);

//   const chip = document.createElement("div");
//   chip.className = "semester-chip";
//   chip.innerHTML = `<small>${item.name}</small><strong>${item.score.toFixed(2)}</strong>`;
//   semesterList.appendChild(chip);
// });

// // Modal
// const modal = document.getElementById("profileModal");
// const openButtons = [
//   document.getElementById("profileButton"),
//   document.getElementById("editProfileBtn")
// ];
// const closeModal = document.getElementById("closeModal");

// openButtons.forEach(btn => btn.addEventListener("click", () => {
//   modal.classList.add("show");
// }));

// closeModal.addEventListener("click", () => modal.classList.remove("show"));

// modal.addEventListener("click", (e) => {
//   if (e.target === modal) modal.classList.remove("show");
// });

// // Profile save
// document.getElementById("saveProfile").addEventListener("click", () => {
//   const name = document.getElementById("nameInput").value.trim() || "Student";
//   const branch = document.getElementById("branchInput").value.trim() || "CSE - AIML";
//   const college = document.getElementById("collegeInput").value.trim() || "College";

//   document.getElementById("profileName").textContent = name;
//   document.getElementById("topName").textContent = name;
//   document.getElementById("profileBranch").textContent = branch;
//   document.querySelector(".profile-info span:first-child").textContent = `🎓 ${college}`;

//   localStorage.setItem("careerProfile", JSON.stringify({ name, branch, college }));
//   modal.classList.remove("show");
//   showToast("Profile updated successfully ✓");
// });

// // Restore profile
// const savedProfile = localStorage.getItem("careerProfile");
// if (savedProfile) {
//   try {
//     const data = JSON.parse(savedProfile);
//     document.getElementById("profileName").textContent = data.name;
//     document.getElementById("topName").textContent = data.name;
//     document.getElementById("profileBranch").textContent = data.branch;
//     document.querySelector(".profile-info span:first-child").textContent = `🎓 ${data.college}`;
//     document.getElementById("nameInput").value = data.name;
//     document.getElementById("branchInput").value = data.branch;
//     document.getElementById("collegeInput").value = data.college;
//   } catch (e) {
//     console.log("Profile data could not be restored.");
//   }
// }

// // Toast
// let toastTimer;
// function showToast(message) {
//   const toast = document.getElementById("toast");
//   toast.textContent = message;
//   toast.classList.add("show");
//   clearTimeout(toastTimer);
//   toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
// }

// // Highlight current navigation item
// const navLinks = document.querySelectorAll(".nav-link");
// const sections = document.querySelectorAll("main section[id]");

// window.addEventListener("scroll", () => {
//   let current = "dashboard";
//   sections.forEach(section => {
//     if (window.scrollY >= section.offsetTop - 160) {
//       current = section.id;
//     }
//   });

//   navLinks.forEach(link => {
//     link.classList.toggle("active", link.getAttribute("href") === `#${current}`);
//   });
// });
