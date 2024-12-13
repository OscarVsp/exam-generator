import exam_generator as EG

if __name__ == "__main__":

    generator = EG.Generator(
        course_name=r"Best courses ever",
        course_code="BEAMS666",
        year="1873-2024",
        session="69nd",
        reset_page_counter=True,
        output_dir="exam-files-example",
    )

    generator.add_set(
        EG.ShortQuestionsSet(
            name="Theory",
            dataset_path="database_example/short_questions.txt",
            nb_questions=1,
            consigne=r"Chat GPT is allowed. Preparation time: $\sim$ 10 sec.",
            blank_line=4,
        )
    )

    generator.add_set(
        EG.LargeQuestionsSet(
            name="Project",
            dataset_path="database_example/large_questions",
            nb_questions=1,
            consigne="Michel Osée is allowed for this part.",
            blank_page=1,
        )
    )

    generator.generate_from_csv(filename="students_list.csv")
