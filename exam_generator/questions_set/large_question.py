from typing import List, Tuple
import random
from pathlib import Path
import os
import re
import __main__

from .base_question_set import BaseQuestionsSet


class MarkdownToLatex:

    DATASET_PATH = None

    @staticmethod
    def _replace_code_block(match) -> str:
        language = match.group(1)
        code = match.group(2).strip()
        replacement = "\\vspace{0.5cm}\n\\begin{lstlisting}"
        if language is not None:
            replacement += f"[language={language}]"
        replacement += f"\n{code}\n"
        replacement += "\\end{lstlisting}\n\\vspace{0.5cm}\n"
        return replacement

    @staticmethod
    def _md_code_to_tex(markdown_content: str) -> str:
        pattern = r"```(\w+)?\n([\s\S]*?)```"
        latex_content = re.sub(
            pattern,
            MarkdownToLatex._replace_code_block,
            markdown_content,
            flags=re.DOTALL,
        )
        return latex_content

    @staticmethod
    def _replace_img(match) -> str:
        image_path = match.group(1)
        replacement = f"\\vspace{{0.5cm}}\n\\begin{{figure}}[H]\n\t\\centering\n\t\\includegraphics[width=0.9\\linewidth]{{{MarkdownToLatex.DATASET_PATH}/{image_path}}}\n\\end{{figure}}\n"
        return replacement

    @staticmethod
    def _md_img_to_tex(markdown_content: str) -> str:
        pattern = r"!\[.*?\]\((.*?)\)"
        latex_content = re.sub(pattern, MarkdownToLatex._replace_img, markdown_content)
        return latex_content

    @staticmethod
    def _md_title_to_text(markdown_content: str) -> str:
        lines = markdown_content.splitlines()
        if lines and re.match(r"^#(.+)", lines[0]):
            title = re.match(r"^#\s*(.+)", lines[0]).group(1)
            lines[0] = f"\\section*{{Question {MarkdownToLatex.INDEX} - {title}}}"
        else:
            lines.insert(0, f"\\section*{{Question {MarkdownToLatex.INDEX}}}")
        latex_content = "\n".join(lines)
        return latex_content

    @staticmethod
    def convert(markdown_content: str, index: int, dataset_path: str) -> str:
        MarkdownToLatex.DATASET_PATH = dataset_path
        MarkdownToLatex.INDEX = index
        title_content = MarkdownToLatex._md_title_to_text(markdown_content)
        code_block_content = MarkdownToLatex._md_code_to_tex(title_content)
        img_content = MarkdownToLatex._md_img_to_tex(code_block_content)
        return img_content


class LargeQuestionsSet(BaseQuestionsSet):

    def __init__(
        self,
        name,
        dataset_path: str,
        nb_questions: int = 1,
        consigne: str = None,
        blank_page: int = 1,
    ) -> None:
        self.blank_page = blank_page
        super().__init__(name, dataset_path, nb_questions, consigne=consigne)

    def _load_dataset(self) -> None:
        self.dataset: List[str] = []
        if os.path.isdir(self.dataset_path):
            index = 1
            while os.path.exists(f"{self.dataset_path}/{index}_question.md"):
                with open(
                    file=f"{self.dataset_path}/{index}_question.md",
                    mode="r",
                    encoding="UTF-8",
                ) as fp:
                    markdown_content = fp.read()
                latex_content = MarkdownToLatex.convert(
                    markdown_content, index, self.dataset_path
                )
                latex_content += "\n\\newpage"
                if self.blank_page is not None:
                    latex_content += "\n\\null\n\\newpage" * self.blank_page
                self.dataset.append(latex_content)
                index += 1

    def _generate_latex_content(self) -> None:

        latex_content = self.header

        indexes = self._pick_indexes()

        latex_content = "\n".join([self.dataset[index] for index in indexes])

        self.latex_content = latex_content
