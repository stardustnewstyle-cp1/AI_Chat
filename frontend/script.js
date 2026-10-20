async function send() {
    const text = document.getElementById("userInput").value;
    if (!text) return;

    // チュートリアルを非表示
    document.getElementById("tutorial").style.display = "none";

    const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();
    render(data);
}

function render(data) {
    const result = document.getElementById("result");
    result.innerHTML = "";

    // 非技術質問カード
    if (data.title === "非技術質問") {
        const card = document.createElement("div");
        card.className = "card nontech-card";
        card.innerHTML = `
            <h2>${data.title}</h2>
            <p>${data.sections[0].content}</p>
        `;
        result.appendChild(card);
        return;
    }

    // Copilot 型：セクションごとにカード分割
    data.sections.forEach(sec => {
        const card = document.createElement("div");
        card.className = "card section-card";

        card.innerHTML += `<h3>${sec.header}</h3>`;

        if (sec.content) {
            card.innerHTML += `<p>${sec.content}</p>`;
        }

        if (sec.list) {
            card.innerHTML += "<ul>";
            sec.list.forEach(item => {
                card.innerHTML += `<li>${item}</li>`;
            });
            card.innerHTML += "</ul>";
        }

        if (sec.steps) {
            card.innerHTML += "<ol>";
            sec.steps.forEach(step => {
                card.innerHTML += `<li>${step}</li>`;
            });
            card.innerHTML += "</ol>";
        }

        if (sec.code) {
            card.innerHTML += `<pre>${sec.code}</pre>`;
        }

        result.appendChild(card);
    });
}
