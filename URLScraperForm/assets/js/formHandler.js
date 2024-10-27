document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("scrapyForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the form from refreshing the page

        const formData = new FormData(form);
        const url = form.getAttribute("action") || "https://api.deeptechafrica.com/scraper";

        try {
            const response = await fetch(url, {
                method: "POST",
                body: new URLSearchParams(formData), // Converts FormData to URL-encoded format
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded" // Needed for form submissions
                }
            });

            if (response.ok) {
                // Check if the response is HTML by attempting to parse it as text
                const contentType = response.headers.get("Content-Type") || "";
                const result = contentType.includes("text/html")
                    ? await response.text()
                    : (await response.json()).message || "Success!";

                responseMessage.innerHTML = result;
                responseMessage.classList.remove("text-danger");
                responseMessage.classList.add("text-success");
            } else {
                const contentType = response.headers.get("Content-Type") || "";
                const error = contentType.includes("text/html")
                    ? await response.text()
                    : (await response.json()).message || "An error occurred.";

                responseMessage.innerHTML = error;
                responseMessage.classList.remove("text-success");
                responseMessage.classList.add("text-danger");
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            responseMessage.textContent = "Failed to submit form.";
            responseMessage.classList.remove("text-success");
            responseMessage.classList.add("text-danger");
        }
    });
});
