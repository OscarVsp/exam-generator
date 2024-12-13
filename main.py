from generator.generator import (
    Generator,
    ShortQuestionsSet,
    LargeQuestionsSet,
)

if __name__ == "__main__":

    generator = Generator(
        course_name=r"Digital architectures \& design",
        course_code="ELECH409",
        year="2023-2024",
        session="1st",
        reset_page_counter=True,
        output_dir="exam-files",
    )

    generator.add_set(
        ShortQuestionsSet(
            name="Theory",
            dataset_path="database/theory_questions.txt",
            nb_questions=2,
            consigne=r"No extra resource are allow for this part. Preparation time: $\sim$ 4 min",
            blank_line=4,
        )
    )

    generator.add_set(
        LargeQuestionsSet(
            name="Exercises",
            dataset_path="database/exercises",
            nb_questions=1,
            consigne=r"Personal handwritten notes are allowed for this part. Preparation time: $\sim$ 7 min",
            blank_page=1,
        )
    )

    generator.add_set(
        ShortQuestionsSet(
            name="Project",
            dataset_path="database/project_questions.txt",
            nb_questions=1,
            consigne=r"The printed report of the project is allowed for this part",
            blank_line=4,
        )
    )

    generator.generate_from_csv()
