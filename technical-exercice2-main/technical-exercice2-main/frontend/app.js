const textInput = document.getElementById("textInput");
const summarizeButton = document.getElementById("summarizeButton");
const summaryOutput = document.getElementById("summaryOutput");
const statusBox = document.getElementById("status");

async function summarizeText() {
    const text = textInput.value.trim();

    if (!text) {
        summaryOutput.textContent = "Please enter some text first.";
        return;
    }

    summarizeButton.disabled = true;
    statusBox.textContent = "Generating summary...";
    statusBox.classList.remove("error");

    try {
        // TODO 4:
        // Send the user's text to the backend API.
        const response = await fetch("/api/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        // TODO 5:
        // Process the API response and display the generated summary.
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || `HTTP ${response.status}`);
        }
        summaryOutput.textContent = data.summary;
        statusBox.textContent = "";
    } catch (error) {
        console.error(error);
        statusBox.textContent = "Something went wrong. Please try again.";
        statusBox.classList.add("error");
    } finally {
        summarizeButton.disabled = false;
    }
}

summarizeButton.addEventListener("click", summarizeText);
