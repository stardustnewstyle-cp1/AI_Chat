# utils/self_improvement_cycle.py

from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.pipelines.pipeline import Pipeline


def self_improvement_cycle(intent_result, raw_output):
    """
    TeacherLayer の自己改善ロジックに合わせた改善ループ
    """

    teacher = TeacherLayer()

    # 1. Teacher が期待される出力を生成
    expected_output = teacher.generate_expected_output(intent_result, raw_output)

    # 2. Pipeline が実際の出力を生成
    pipeline_output = Pipeline.run(raw_output)

    # 3. 差分を検出
    missing_items = teacher.compare(expected_output, pipeline_output)

    # 4. 改善を適用
    improved_output = teacher.apply_improvement(pipeline_output, missing_items)

    # 5. Teacher の統合処理（improve）
    final_output = teacher.improve(intent_result, raw_output)

    return {
        "expected_output": expected_output,
        "pipeline_output": pipeline_output,
        "missing_items": missing_items,
        "improved_output": improved_output,
        "final_output": final_output
    }
