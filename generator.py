from typing import List, Dict
import __main__
import subprocess
import os, sys
import random
import csv
import yaml
import shutil

# TODO Cleaner

from questions_set.base_question_set import BaseQuestionsSet
from questions_set.short_question import ShortQuestionsSet
from questions_set.large_question import LargeQuestionsSet


class Generator:
    """
    The `Generator` class handle the overall parameter of the exam, such as:


    When `generate` is called, it load the `students_list.csv` (can be overide) to get the list of students, then generate the pdf of the exam for each one of them.

    The `students_list.csv` can be directly edited or you can convert existing `xlsx` file.

    """

    def __init__(
        self,
        config_file: str,
        students_list_file: str,
        database_path: str,
        output_path: str,
    ) -> None:

        if not config_file.endswith(".yaml"):
            raise TypeError(
                f'Parameter "config_file" need to be a ".yaml" file. Provided one is {config_file}'
            )

        if not students_list_file.endswith(".csv"):
            raise TypeError(
                f'Parameter "students_list_file" need to be a ".csv" file. Provided one is {students_list_file}'
            )

        if not database_path.endswith("/"):
            database_path += "/"
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        if not output_path.endswith("/"):
            output_path += "/"

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        self.output_dir = output_path
        self.questions_sets: List[BaseQuestionsSet] = []
        self.latex_path: str = os.path.dirname(__main__.__file__) + "/latex"

        if not os.path.exists(self.latex_path + "/tmp"):
            os.makedirs(self.latex_path + "/tmp")
        self._clear_tmp()

        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            exam_config = config["exam"]
            self.course_name: str = exam_config["name"]
            self.course_code: str = exam_config["code"]
            self.year: str = exam_config["year"]
            self.session: str = exam_config["session"]
            self.title_page: bool = bool(exam_config.get("titlepage", False))
            self.draft_pages: int = int(exam_config.get("draft_pages", 0))
            self.reset_page_counter: bool = bool(
                exam_config.get("reset_page_counter", False)
            )

            for set_config_item in config["sets"]:
                set_type = list(set_config_item.keys())[0]  # FIXME not safe
                set_config = set_config_item[set_type]
                if set_type.lower() == "short":
                    new_set = ShortQuestionsSet(
                        set_config["name"],
                        database_path + set_config["path"],
                        self.latex_path,
                        set_config["size"],
                        set_config["consigne"],
                        set_config.get("blank_line", 0),
                    )
                elif set_type.lower() == "large":
                    new_set = LargeQuestionsSet(
                        set_config["name"],
                        database_path + set_config["path"],
                        self.latex_path,
                        set_config["size"],
                        set_config["consigne"],
                        set_config.get("blank_page", 0),
                    )
                else:
                    raise ValueError(
                        f'Error loading the config from file. Set type "{set_type}" is not valid.'
                    )
                self.questions_sets.append(new_set)

        self.students_dict = self._csv_to_dict(students_list_file)

        self._generate_header()
        self._generate_content()

    def _generate_header(self) -> None:
        """
        Generate the `header.sty` file to pass the exam data to latex.

        This is called once at initialisation.
        """
        latex_content = "%This file is automatically generated. DO NOT EDIT!\n\n"
        latex_content += r"\newcommand{\academicyear}{" + self.year + "}\n"
        latex_content += r"\newcommand{\session}{" + self.session + "}\n"
        latex_content += r"\newcommand{\coursename}{" + self.course_name + "}\n"
        latex_content += r"\newcommand{\coursecode}{" + self.course_code + "}"
        with open(
            self.latex_path + "/tmp/header.sty", mode="w", encoding="UTF-8"
        ) as fp:
            fp.write(latex_content)

    def _generate_content(self) -> None:
        """
        Generate the `content.tex` file containing references to the differents part of the exam.

        This is call once at initialisation.
        """
        latex_content = "%This file is automatically generated. DO NOT EDIT!\n\n"

        if self.title_page:
            latex_content += "\input{./title.tex}\n"
        for index, questions_set in enumerate(self.questions_sets):

            latex_content += f"\n\\begin{{center}}\n{{\\Large \\textbf{{Part {index+1} - {questions_set.name}}}}}\n\\end{{center}}\n"
            latex_content += (
                f"\\lfoot{{Part {index+1} - {questions_set.name}}}\n\\smallskip\n"
            )
            latex_content += f"\\input{{\{questions_set.name}}}\n\\newpage\n"
            if self.reset_page_counter:
                latex_content += f"\\setcounter{{page}}{{1}}\n"
        if self.draft_pages:
            latex_content += "\\lfoot{{Draft pages}}" + "\\newpage~" * self.draft_pages
        with open(self.latex_path + "/content.tex", mode="w", encoding="UTF-8") as fp:
            fp.write(latex_content)

    def _generate_sets(self, name: str, matricule: int = None) -> None:
        """
        This fix the random seed from the student matricule or fullname, then call the generation method of each question set.

        Args:
            name (str): name of the student
            matricule (int): Matricule of the student
        """
        if matricule is None:
            matricule = "".join(map(str, map(ord, name)))
        random.seed(matricule)

        for questions_set in self.questions_sets:
            questions_set.generate()

    def _generate_student_header(self, name: str, matricule: int = None) -> None:
        """
        _generate_student_header generate the header containing the student relevant informations including the questions that he got

        This is call for each students.
        """
        with open(
            self.latex_path + "/tmp/student.sty", mode="w", encoding="UTF-8"
        ) as fp:
            fp.write(f"%This file is automatically generated. DO NOT EDIT!\n")
            fp.write(f"\\newcommand{{\\name}}{{{name}}}")
            if matricule is not None:
                fp.write(f"\\newcommand{{\\matricule}}{{{matricule}}}")
            else:
                fp.write(f"\\newcommand{{\\matricule}}{{}}")
            for question_set in self.questions_sets:
                fp.write(
                    f"\\newcommand{{\\{question_set.name}}}{{{question_set.current_file}}}"
                )

    def _generate_pdf(self, name: str) -> None:
        """
        This passes the current student name to latex, them uses the `MakeFile` to build the pdf file.
        The file is finally renamed and moved into the exam folder.

        This is call at the end of each files generation

        Args:
            name (str, optional): name of the student.
        """
        process = subprocess.run(
            ["make", "-C", self.latex_path], stdout=subprocess.DEVNULL, timeout=30
        )
        if process.returncode != 0:
            raise Exception(
                f"Fail to generate pdf. Make return code: {process.returncode}. Check if Latex is installed."
            )
        shutil.move(
            self.latex_path + "/output-files/main.pdf",
            f"{self.output_dir}/{name.replace(' ','_')}_{self.course_code}_EXAM_{self.year}_{self.session}.pdf",
        )

    def _generate_student(
        self, student_name: str, student_matricule: int = None
    ) -> None:
        """
        Internal method to generate exam file for a single student.

        Used by "generate_single", "generate_from_dict" and "generate_from_csv".

        Args:
            student_name (str): full name of the student
            student_matricule (int, optional): matricule of the student
        """
        print(f"Genering pdf for {student_name}:{student_matricule}...")
        self._generate_sets(student_name, student_matricule)
        self._generate_student_header(student_name, student_matricule)
        self._generate_pdf(student_name)

    def generate_single(self, student_name: str, student_matricule: int = None) -> None:
        """
        Generate exam file for a single student.

        For multiple student, please use `generate_from_dict` or `generate_from_csv` instead.

        Args:
            student_name (str): full name of the student
            student_matricule (int, optional): matricule of the student
        """
        self._generate_student(student_name, student_matricule)
        print("Finished")

    def generate(self) -> None:
        """
        Generate exam file for a dict of student with the following structure: `{name:matricule}`.

        Args:
            students_dict (dict): The dict of `{name:matricule}` pairs".
        """

        for name, matricule in self.students_dict.items():
            self._generate_student(name, matricule)
        print("Finished")

    def _clear_tmp(self) -> None:

        subprocess.run(
            ["make", "-C", self.latex_path, "clean"],
            check=False,
            stdout=subprocess.DEVNULL,
        )
        tmp_files = [
            os.path.join(self.latex_path + "/tmp", f)
            for f in os.listdir(self.latex_path + "/tmp")
            if f != "header.sty"
        ]
        for f in tmp_files:
            try:
                os.remove(f)
            except (FileNotFoundError, PermissionError, IsADirectoryError):
                pass

    @staticmethod
    def _csv_to_dict(
        filename: str,
    ) -> Dict[str, int | None]:
        students: Dict[str, int | None] = {}

        with open(filename, mode="r", encoding="UTF-8") as fp:
            students_csv = csv.DictReader(fp)

            for student_row in students_csv:
                students[
                    student_row[students_csv.fieldnames[0]].strip().upper()
                    + " "
                    + student_row[students_csv.fieldnames[1]].strip()
                ] = (
                    int(student_row[students_csv.fieldnames[2]].strip())
                    if student_row[students_csv.fieldnames[2]].strip() != ""
                    else None
                )
        return students


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No config provided was provided. Using example configuration...")
        gen = Generator(
            "/home/oscar/Documents/exam_generator/config_example.yaml",
            "/home/oscar/Documents/exam_generator/students_list_example.csv",
            "/home/oscar/Documents/exam_generator/database_example/",
            "/home/oscar/Documents/exam_generator/exam-files-example/",
        )
    elif len(sys.argv) == 5:
        gen = Generator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise Exception(f"Incorrect parameters.")
    gen.generate()
