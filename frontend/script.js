function autoResize() {
    const input = document.getElementById("userInput");
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
}

document.getElementById("userInput").addEventListener("input", autoResize);

document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send();
    }
});

function appendMessage(role, text) {
    const result = document.getElementById("result");
    const msg = document.createElement("div");
    msg.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    msg.appendChild(bubble);
    result.appendChild(msg);
    result.scrollTop = result.scrollHeight;
}

function flattenSections(data) {
    if (!data || !Array.isArray(data.sections)) return "回答を取得できませんでした。";

    const parts = [];
    data.sections.forEach(sec => {
        if (sec.header) parts.push(sec.header);
        if (sec.content) parts.push(sec.content);
        if (sec.list) parts.push(sec.list.join("\n"));
        if (sec.steps) parts.push(sec.steps.join("\n"));
        if (sec.code) parts.push(sec.code);
    });

    return parts.join("\n\n");
}

async function send() {
    const text = document.getElementById("userInput").value.trim();
    if (!text) return;

    appendMessage("user", text);

    document.getElementById("userInput").value = "";
    autoResize();

    try {
        const response = await fetch("http://localhost:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error("API error");

        const data = await response.json();
        const answer = flattenSections(data);

        appendMessage("assistant", answer);

    } catch (error) {
        appendMessage("assistant", "通信エラーが発生しました。");
    }
}