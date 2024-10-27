document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("scrapyForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the form from refreshing the page

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        const url = form.getAttribute("action") || "https://api.deeptechafrica.com/scraper";

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data) // Convert the data object to JSON
            });

            if (response.ok) {
                const contentType = response.headers.get("Content-Type") || "";
                const result = contentType.includes("text/html")
                    ? await response.text()
                    : (await response.json()).message || "Success!";

                // Ensure safe insertion of HTML content
                if (contentType.includes("text/html")) {
                    responseMessage.innerHTML = result;
                } else {
                    responseMessage.textContent = result;
                }

                responseMessage.classList.remove("text-danger");
                responseMessage.classList.add("text-success");
            } else {
                const contentType = response.headers.get("Content-Type") || "";
                let error;

                // Try to parse JSON error message if available
                try {
                    error = contentType.includes("application/json")
                        ? (await response.json()).message || "An error occurred."
                        : await response.text();
                } catch (jsonError) {
                    error = "An error occurred.";
                }

                responseMessage.innerHTML = contentType.includes("text/html") ? error : document.createTextNode(error);
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
