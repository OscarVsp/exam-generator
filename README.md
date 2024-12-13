- [1. Usage](#1-usage)
- [2. Questions sets](#2-questions-sets)
  - [2.1. Short questions set](#21-short-questions-set)
  - [2.2. Large questions set](#22-large-questions-set)
- [3. Generator](#3-generator)
- [4. TODOs](#4-todos)

# 1. Usage

Create your dataset of question (see [2. Questions sets](#2-questions-sets))

Edit the `main.py` file to adjust the parameters for the `Generator` (see [3. Generator](#3-generator)) and the `Questions Set` (see [2. Questions sets](#2-questions-sets))

Edit the [students_list.csv](students_list.csv) with the list of students. The matricule is optional (it is used as the seed to randomly pick the questions, but the full name is used instead if missing).

DO NOT EDIT `.tex` and `.sty` files directly! Thoses are being generated automatically and will be override.

Run [example.py](example.py). The generated pdf are available in the [exam_files-example/](/exam_files-example/) folder.

# 2. Questions sets

Questions sets are structures that contain the questions for a given part of the exam. There is two type of Questions sets:

## 2.1. Short questions set

The short questions set contains small questions that are a few lines at most. Thoses questions can only contain text, no image or code block.

The questions will be displayed as list of enumerated question with some optional blank spaces in between.

The questions have to be store in a `.txt` or `.md` file, with one question by line.

Example of such dataset can be seen in [database-example/short_questions.txt](database_example/short_questions.txt)


## 2.2. Large questions set

The large questions set contains bigger question each store in their own `n_question.md` file, where `n` is the index of the question (start at 1, SHOULD BE CONTINUOUS). All files should be contain in a folder that is used for the `dataset_path` parameter.

The question can have the following elements (using markdown syntax):

- custom title: declared on the first line with a header 1 (i.e. `# My favorite question`).
- image: declared using the markdown syntax (i.e. `![alt text](path/to/image.png)`). The folder is used as root directory here.
- code block: with optional language specifier.

Example of such dataset can be seen in [database-example/large_question/](database_example/large_questions/)


# 3. Generator

The `Generator` module handle the overall parameter of the exam, such as:

- `course_name` (str): Name of the course
- `course_code` (str): Code of the course
- `year` (str): academique year
- `session` (str): current session
- `reset_page_counter` (bool) (default=False): should the page counter be reset on each part of the exam.

Once initialized, each QuestionsSet have to be added by using the `.add_set(...)` method.

When `generate_from_csv(...)` is called, it load the [students_list.csv](students_list.csv) (default, can be changed) to get the list of students, then generate the pdf of the exam for each one of them.

The `students_list.csv` can be directly edited or you can convert existing `xlsx` file. 

Here is an example of the usage:
```py
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

```

# 4. TODOs

- Dependencies and install
- Cleaner console output
- Clean latex packages
- Option to cache the tmp file during a generation process (only usefull for big number of student)