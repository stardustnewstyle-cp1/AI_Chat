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

    const tutorial = document.getElementById("tutorial");
    if (tutorial && tutorial.style.display !== "none") {
        tutorial.classList.add("fade-out");
        setTimeout(() => tutorial.style.display = "none", 400);
    }

    const result = document.getElementById("result");
    const loading = document.createElement("div");
    loading.className = "card";
    loading.innerHTML = "<p>考え中...</p>";
    result.appendChild(loading);

    try {
        const response = await fetch("http://localhost:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error("API error");
        }

        const data = await response.json();
        result.removeChild(loading);

        const input = document.getElementById("userInput");
        input.value = "";
        input.style.height = "auto";
        input.focus();

        render(data);
    } catch (error) {
        result.removeChild(loading);

        const errCard = document.createElement("div");
        errCard.className = "card";
        errCard.innerHTML = "<p>通信エラーが発生しました。</p>";
        result.appendChild(errCard);
    }
}

// レンダリング
function render(data) {
    const result = document.getElementById("result");

    if (data.mode === "code") {
        const card = document.createElement("div");
        card.className = "card code-card";

        const title = data.title || "コード例";
        const codeText = (data.sections && data.sections[0] && data.sections[0].code)
            ? data.sections[0].code
            : "コードを生成できませんでした。";

        const h3 = document.createElement("h3");
        h3.textContent = title;
        card.appendChild(h3);

        const pre = document.createElement("pre");
        const code = document.createElement("code");
        code.textContent = codeText;
        pre.appendChild(code);

        card.appendChild(pre);
        result.appendChild(card);

        hljs.highlightAll();
        return;
    }

    // 通常 answer モード
    if (!data.sections || !Array.isArray(data.sections)) {
        const err = document.createElement("div");
        err.className = "card";
        err.innerHTML = "<p>応答データが不正です。</p>";
        result.appendChild(err);
        return;
    }

    data.sections.forEach(sec => {
        const card = document.createElement("div");
        card.className = "card";

        if (sec.header) {
            const h3 = document.createElement("h3");
            h3.textContent = sec.header;
            card.appendChild(h3);
        }

        if (sec.content) {
            const p = document.createElement("p");
            p.textContent = sec.content;
            card.appendChild(p);
        }

        if (sec.list) {
            const ul = document.createElement("ul");
            sec.list.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                ul.appendChild(li);
            });
            card.appendChild(ul);
        }

        if (sec.steps) {
            const ol = document.createElement("ol");
            sec.steps.forEach(step => {
                const li = document.createElement("li");
                li.textContent = step;
                ol.appendChild(li);
            });
            card.appendChild(ol);
        }

        if (sec.code) {
            const pre = document.createElement("pre");
            const code = document.createElement("code");
            code.textContent = sec.code;
            pre.appendChild(code);
            card.appendChild(pre);
        }

        result.appendChild(card);
        hljs.highlightAll();
    });
}