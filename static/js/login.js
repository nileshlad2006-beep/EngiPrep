document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.querySelector("input[name=username]").value;
    const password = document.querySelector("input[name=password]").value;

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const result = await response.json();

      alert(result.message);

      if (response.ok) {

        if (result.role === "admin") {
          window.location.href = "/admin";
        } else {
          window.location.href = "/profile";
        }

      }

    } catch (error) {
      alert("Something went wrong. Please try again.");
      console.error(error);
    }
  });