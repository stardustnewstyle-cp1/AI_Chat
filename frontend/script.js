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

function appendMessage(role, text) {
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

function flattenSections(data) {
    if (!data || !data.sections || !Array.isArray(data.sections)) {
        return "回答を取得できませんでした。";
    }

    const parts = [];
    data.sections.forEach((sec) => {
        if (sec.header) parts.push(sec.header);
        if (sec.content) parts.push(sec.content);
        if (sec.list) parts.push(sec.list.join("\n"));
        if (sec.steps) parts.push(sec.steps.join("\n"));
        if (sec.code) parts.push(sec.code);
    });

    return parts.join("\n\n");
}

function defaultFollowUps() {
    return [
        {
            label: "修正案を出す",
            onClick: () => {
                appendMessage("assistant", "この部分は、責務を分離し、例外ハンドリングとログ出力を追加するのが安全です。");
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
                appendMessage("assistant", "質問をもう少し具体的にしていただければ、より正確に答えられます。");
            }
        }
    ];
}

document.getElementById("userInput").addEventListener("input", autoResize);

document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send();
    }
});

async function send() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);

    input.value = "";
    autoResize();

    try {
        const response = await fetch("http://localhost:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error("API error");

        const data = await response.json();

        if (data.mode === "external") {
            appendFollowUp(
                "外部情報が必要です。内部検索で補足します。",
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

        const answer = flattenSections(data);
        appendMessage("assistant", answer);

        appendFollowUp(
            "必要なら次のどれかを選んでください。",
            defaultFollowUps()
        );

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
    }
}