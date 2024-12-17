from typing import List
import random
import os

from .base_question_set import BaseQuestionsSet


class QCMQuestionsSet(BaseQuestionsSet):

    def __init__(
        self,
        name,
        dataset_path: str,
        latex_path: str,
        nb_questions: int = 1,
        consigne: str = None,
        blank_line: int = 4,
    ) -> None:
        self.blank_line = blank_line
        super().__init__(
            name, dataset_path, latex_path, nb_questions, consigne=consigne
        )

    def _load_dataset(self) -> None:

        if os.path.isdir(self.dataset_path):
            if os.path.isfile(f"{self.dataset_path}/questions.txt"):
                self.dataset_path = f"{self.dataset_path}/questions.txt"
            elif os.path.isfile(f"{self.dataset_path}/questions.md"):
                self.dataset_path = f"{self.dataset_path}/questions.md"
            else:
                raise FileNotFoundError(f"Datapath {self.dataset_path} is invalid.")

        with open(file=self.dataset_path, mode="r", encoding="UTF-8") as fp:
            self.dataset: List[Dict[str : List[str]]] = []

            current_question = None
            current_responses = []

            for line in fp.readlines():
                if line.startswith("#"):
                    continue

                if line.startswith("-"):

                    if current_question == None:
                        current_question = (
                            line[1:].strip().replace("&", r"\&").replace("_", r"\_")
                        )

                    else:
                        self.dataset.append(
                            {
                                "question": current_question,
                                "responses": current_responses,
                            }
                        )
                        current_responses = []
                        current_question = line[1:]
                elif line.startswith("  -"):
                    current_responses.append(
                        line.strip()[1:].strip().replace("&", r"\&").replace("_", r"\_")
                    )

    def _generate_latex_content(self, indexes: List[int]) -> None:

        latex_content = self.header

        if len(indexes) > 1:
            latex_content += "\\begin{enumerate}\n"
            for n in indexes:
                latex_content += f"\t\\item {self.dataset[n]['question']}\n"
                latex_content += "\\begin{itemize}\n"
                for response in self.dataset[n]["responses"]:
                    latex_content += f"\t\\item[\$\\openbox\$] {response}\n"
                latex_content += "\\end{itemize}\n"
                if self.blank_line is not None:
                    latex_content += "\n" * self.blank_line
            latex_content += "\\end{enumerate}"
        else:
            latex_content += f"{self.dataset[indexes[0]]['question']}\n"
            latex_content += "\\begin{itemize}\n"
            for response in self.dataset[indexes[0]]["responses"]:
                latex_content += f"\t\\item[\\ding{{111}}] {response}\n"
            latex_content += "\\end{itemize}\n"

        self.latex_content = latex_content
