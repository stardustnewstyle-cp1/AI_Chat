let isSending = false;

/* -----------------------------
 * 入力補助
 * ----------------------------- */
function fill(text) {
    const input = document.getElementById("userInput");
    input.value = text;
    autoResize();
    input.focus();
}

function autoResize() {
    const input = document.getElementById("userInput");
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
}

function hideTutorial() {
    const tutorial = document.getElementById("tutorial");
    if (tutorial) tutorial.style.display = "none";
}

/* -----------------------------
 * メッセージ描画（ユーザー）
 * ----------------------------- */
function appendMessage(role, text) {
    hideTutorial();

    const result = document.getElementById("result");
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(bubble);
    result.appendChild(message);
    result.scrollTop = result.scrollHeight;
}

/* -----------------------------
 * Follow-up ボタン描画
 * ----------------------------- */
function appendFollowUp(text, actions) {
    const result = document.getElementById("result");
    const message = document.createElement("div");
    message.className = "message assistant";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    const followup = document.createElement("div");
    followup.className = "followup";

    actions.forEach((action) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "followup-btn";
        btn.textContent = action.label;
        btn.addEventListener("click", () => {
            if (typeof action.onClick === "function") {
                action.onClick();
            }
        });
        followup.appendChild(btn);
    });

    message.appendChild(bubble);
    message.appendChild(followup);
    result.appendChild(message);
    result.scrollTop = result.scrollHeight;
}

/* -----------------------------
 * バッジ生成
 * ----------------------------- */
function createBadge(label, tone = "purple") {
    const badge = document.createElement("span");
    badge.className = `meta-badge ${tone}`;
    badge.textContent = label;
    return badge;
}

/* -----------------------------
 * セクション描画
 * ----------------------------- */
function renderSection(section) {
    if (!section || typeof section !== "object") return null;

    const block = document.createElement("div");
    block.className = "section-block";

    if (section.header) {
        const header = document.createElement("h3");
        header.className = "section-header";
        header.textContent = section.header;
        block.appendChild(header);
    }

    if (section.content) {
        const content = document.createElement("p");
        content.className = "section-content";
        content.textContent = section.content;
        block.appendChild(content);
    }

    if (Array.isArray(section.list) && section.list.length > 0) {
        const ul = document.createElement("ul");
        ul.className = "section-list";
        section.list.forEach((item) => {
            const li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        });
        block.appendChild(ul);
    }

    if (Array.isArray(section.steps) && section.steps.length > 0) {
        const ol = document.createElement("ol");
        ol.className = "section-steps";
        section.steps.forEach((step) => {
            const li = document.createElement("li");
            li.textContent = step;
            ol.appendChild(li);
        });
        block.appendChild(ol);
    }

    if (section.code) {
        const pre = document.createElement("pre");
        pre.className = "section-code";
        const code = document.createElement("code");
        code.textContent = section.code;
        pre.appendChild(code);
        block.appendChild(pre);
    }

    return block;
}

/* -----------------------------
 * ★ カード描画（TeacherLayer のみ）
 * ----------------------------- */
function renderAnswerCard(data) {
    const result = document.getElementById("result");
    hideTutorial();

    const message = document.createElement("div");
    message.className = "message assistant";

    const card = document.createElement("div");
    card.className = "answer-card";

    /* --- Title --- */
    const title = document.createElement("div");
    title.className = "answer-title";
    title.textContent = data.title || "回答";
    card.appendChild(title);

    /* --- Meta badges --- */
    const meta = document.createElement("div");
    meta.className = "answer-meta";

    if (data.intent) meta.appendChild(createBadge(data.intent, "blue"));
    if (data.reasoning) meta.appendChild(createBadge(data.reasoning, "purple"));
    if (data.level) meta.appendChild(createBadge(data.level, "green"));

    card.appendChild(meta);

    /* --- Sections --- */
    const sections = Array.isArray(data.sections) ? data.sections : [];
    sections.forEach((section) => {
        const rendered = renderSection(section);
        if (rendered) card.appendChild(rendered);
    });

    /* --- Append card --- */
    message.appendChild(card);
    result.appendChild(message);
    result.scrollTop = result.scrollHeight;
}

/* -----------------------------
 * Follow-up デフォルト
 * ----------------------------- */
function defaultFollowUps() {
    return [
        {
            label: "修正案を出す",
            onClick: () => {
                appendMessage("assistant", "この部分は、責務を分離して、例外ハンドリングとログ出力を追加した方が安全です。");
            }
        },
        {
            label: "原因を詳しく",
            onClick: () => {
                appendMessage("assistant", "原因は、入力の前処理と実際の処理フローがずれている場合が多いです。まずは入力値の検証と呼び出し順序を確認してください。");
            }
        },
        {
            label: "別の観点で見る",
            onClick: () => {
                appendMessage("assistant", "設計の観点では、関数の責務が増えすぎている可能性があります。役割を分けると、テストしやすくなります。");
            }
        },
        {
            label: "別質問にする",
            onClick: () => {
                appendMessage("assistant", "質問をもう少し具体的にしてください。例えば「このコードの」「このAPIの」「エラー原因の」などです。");
            }
        }
    ];
}

/* -----------------------------
 * 入力イベント
 * ----------------------------- */
document.getElementById("userInput").addEventListener("input", autoResize);

document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send();
    }
});

document.getElementById("sendButton").addEventListener("click", () => {
    send();
});

/* -----------------------------
 * API 送信
 * ----------------------------- */
async function send() {
    if (isSending) return;

    const input = document.getElementById("userInput");
    const button = document.getElementById("sendButton");
    const text = input.value.trim();

    if (!text) return;

    isSending = true;
    button.disabled = true;

    appendMessage("user", text);

    input.value = "";
    autoResize();

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

        if (data.mode === "external") {
            appendFollowUp(
                "外部情報が必要です。内部検索で補助します。",
                [
                    {
                        label: "続ける",
                        onClick: () => {
                            appendMessage("assistant", "検索結果を補助情報として使い、質問に対して最適な回答を整理します。");
                        }
                    },
                    {
                        label: "ローカル回答に切替",
                        onClick: () => {
                            appendMessage("assistant", "ローカル回答で続けます。対象がこのリポジトリのコードや設計なら、より正確に答えられます。");
                        }
                    },
                    {
                        label: "別質問にする",
                        onClick: () => {
                            appendMessage("assistant", "質問の対象を絞ってください。例えば「このファイルの」「この関数の」「このエラーの」などです。");
                        }
                    }
                ]
            );
            return;
        }

        /* ★ 修正：appendMessage を削除して TeacherLayer のカードのみ描画 */
        renderAnswerCard(data);

        appendFollowUp("必要なら次のどれかを選んでください。", defaultFollowUps());

    } catch (error) {
        appendMessage("assistant", "通信エラーが発生しました。");
        appendFollowUp(
            "次のどれかを選んでください。",
            [
                {
                    label: "再試行",
                    onClick: () => send()
                },
                {
                    label: "別質問にする",
                    onClick: () => appendMessage("assistant", "質問をもう少し具体的にしてください。")
                }
            ]
        );
    } finally {
        isSending = false;
        button.disabled = false;
    }
}
