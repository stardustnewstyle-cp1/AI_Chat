function self_improvement_cycle(input):

    teacher = TeacherLayer.generate_expected_output(input)

    pipeline = Pipeline.run(input)

    evaluation = EvaluateLayer.compare(teacher, pipeline)

    improvements = ImproveLayer.apply(evaluation)

    TeacherLayer.update(improvements)

    return {
        "teacher": teacher,
        "pipeline": pipeline,
        "evaluation": evaluation,
        "improvements": improvements
    }
