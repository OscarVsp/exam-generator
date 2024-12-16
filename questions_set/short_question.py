from typing import List
import random
import os

from .base_question_set import BaseQuestionsSet


class ShortQuestionsSet(BaseQuestionsSet):

    def __init__(
        self,
        name,
        dataset_path: str,
        nb_questions: int = 1,
        consigne: str = None,
        blank_line: int = 4,
    ) -> None:
        self.blank_line = blank_line
        super().__init__(name, dataset_path, nb_questions, consigne=consigne)

    def _load_dataset(self) -> None:

        if os.path.isdir(self.dataset_path):
            if os.path.isfile(f"{self.dataset_path}/questions.txt"):
                self.dataset_path = f"{self.dataset_path}/questions.txt"
            elif os.path.isfile(f"{self.dataset_path}/questions.md"):
                self.dataset_path = f"{self.dataset_path}/questions.md"
            else:
                raise FileNotFoundError(f"Datapath {self.dataset_path} is invalid.")

        with open(file=self.dataset_path, mode="r", encoding="UTF-8") as fp:
            self.dataset: List[str] = [
                q.replace("&", r"\&").replace("_", r"\_").strip("\n").strip()
                for q in fp.readlines()
            ]

    def _generate_latex_content(self) -> None:

        latex_content = self.header

        indexes = self._pick_indexes()

        if len(indexes) > 1:
            latex_content += "\\begin{enumerate}\n"
            for n in indexes:
                latex_content += f"\t\\item {self.dataset[n]}\n"
                if self.blank_line is not None:
                    latex_content += "\n" * self.blank_line
            latex_content += "\\end{enumerate}"
        else:
            latex_content += f"{self.dataset[indexes[0]]}"

        self.latex_content = latex_content
