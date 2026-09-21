#app_aitechnicalinfochat.py
import streamlit as st

# ============================
# ダミーレイヤー（後で本物に差し替える）
# ============================

class IntentLayer:
    def classify(self, user_input):
        # 本番では意味軸分類モデルを入れる
        return "design"  # 仮の返り値


class ReasoningLayer:
    def generate(self, intent, mode, user_profile, memory):
        # 本番ではテンプレート生成を入れる
        return f"[Reasoning Layer 未実装] intent={intent}, mode={mode}"


class TeacherLayer:
    def __init__(self):
        self.log = []

    def improve(self, raw_answer, intent, mode):
        # 本番では改善ロジックを入れる
        improved = raw_answer + "  ← TeacherLayer:改善なし(ダミー)"
        self.log.append({"intent": intent, "mode": mode, "raw": raw_answer})
        return improved


class MemoryLayer:
    def __init__(self):
        self.state = {}

    def update(self, user_input, teacher_output):
        # 本番では文脈保存を入れる
        self.state["last_input"] = user_input
        self.state["last_output"] = teacher_output


class GlobalLayer:
    def update(self, intent, teacher_output):
        # 本番では全体学習を入れる
        pass


class DummyLLM:
    def generate(self, text):
        # 本番では LLM を接続する
        return text + "  ← LLM(ダミー)"


# ============================
# Router（本番の心臓部）
# ============================

class Router:
    def __init__(self, intent_layer, reasoning_layer, teacher_layer,
                 memory_layer, global_layer, llm):
        self.intent_layer = intent_layer
        self.reasoning_layer = reasoning_layer
        self.teacher_layer = teacher_layer
        self.memory_layer = memory_layer
        self.global_layer = global_layer
        self.llm = llm

    def run(self, user_input, mode, user_profile):
        # 1. Intent Layer
        intent = self.intent_layer.classify(user_input)

        # 2. Reasoning Layer
        reasoning_output = self.reasoning_layer.generate(
            intent=intent,
            mode=mode,
            user_profile=user_profile,
            memory=self.memory_layer.state
        )

        # 3. Teacher Layer
        teacher_output = self.teacher_layer.improve(
            raw_answer=reasoning_output,
            intent=intent,
            mode=mode
        )

        # 4. Memory Layer
        self.memory_layer.update(user_input, teacher_output)

        # 5. Global Layer
        self.global_layer.update(intent, teacher_output)

        # 6. LLM
        final_answer = self.llm.generate(teacher_output)

        # 7. UI に返す
        return {
            "final_answer": final_answer,
            "intent": intent,
            "teacher_log": self.teacher_layer.log,
            "memory_state": self.memory_layer.state,
            "raw_reasoning": reasoning_output
        }


# ============================
# Streamlit UI（提出用）
# ============================

st.title("hide AI - 本番プロトタイプ")

mode = st.selectbox("Mode", ["kids", "beginner", "standard", "advanced", "pro"])
user_input = st.text_input("質問を入力してください")

# Router 初期化
router = Router(
    IntentLayer(),
    ReasoningLayer(),
    TeacherLayer(),
    MemoryLayer(),
    GlobalLayer(),
    DummyLLM()
)

if st.button("送信"):
    result = router.run(user_input, mode, user_profile={})
    st.write("### 🧠 最終回答")
    st.write(result["final_answer"])

    with st.expander("Teacher Log"):
        st.write(result["teacher_log"])

    with st.expander("Memory State"):
        st.write(result["memory_state"])

    with st.expander("Raw Reasoning Output"):
        st.write(result["raw_reasoning"])
