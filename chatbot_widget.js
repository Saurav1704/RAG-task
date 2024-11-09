document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("rag-chatbot-container");

    if (container) {
        container.innerHTML = `
            <div class="rag-chatbot">
                <input type="text" id="user-query" placeholder="Ask me anything..." />
                <button id="send-query">Send</button>
                <div id="chatbot-response"></div>
            </div>
        `;

        document.getElementById("send-query").addEventListener("click", async () => {
            const query = document.getElementById("user-query").value;
            const responseContainer = document.getElementById("chatbot-response");

            try {
                const response = await fetch("http://localhost:5000/chatbot", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query }),
                });

                const data = await response.json();
                if (data.error) {
                    responseContainer.textContent = `Error: ${data.error}`;
                } else {
                    responseContainer.textContent = data.answer;
                }
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }
});
