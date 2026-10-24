// 例クリックで入力
function fill(text) {
    const input = document.getElementById("userInput");
    input.value = text;
    autoResize();
    input.focus();
}

// textarea 自動リサイズ
function autoResize() {
    const input = document.getElementById("userInput");
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
}

document.getElementById("userInput").addEventListener("input", autoResize);

// Enterで送信（Shift+Enterで改行）
document.getElementById("userInput").addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send();
    }
});

// 送信処理
async function send() {
    const text = document.getElementById("userInput").value.trim();
    if (!text) return;

    // チュートリアルをフェードアウト
    const tutorial = document.getElementById("tutorial");
    if (tutorial.style.display !== "none") {
        tutorial.classList.add("fade-out");
        setTimeout(() => tutorial.style.display = "none", 400);
    }

    // ローディングカード
    const result = document.getElementById("result");
    const loading = document.createElement("div");
    loading.className = "card";
    loading.innerHTML = "<p>考え中...</p>";
    result.appendChild(loading);

    const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();
    result.removeChild(loading);

    render(data);
}

// レンダリング
function render(data) {
    const result = document.getElementById("result");

    // 非技術質問
    if (data.title === "非技術質問") {
        const card = document.createElement("div");
        card.className = "card nontech";
        card.innerHTML = `
            <h3>${data.title}</h3>
            <p>${data.sections[0].content}</p>
        `;
        result.appendChild(card);
        return;
    }

    // セクションごとにカード化
    data.sections.forEach(sec => {
        const card = document.createElement("div");
        card.className = "card";

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
            card.innerHTML += `<pre><code>${sec.code}</code></pre>`;
        }

        result.appendChild(card);
        hljs.highlightAll();
    });
}
