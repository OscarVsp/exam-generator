- [1. Question sets](#1-question-sets)
  - [1.1. Short questions](#11-short-questions)
  - [1.2. Large questions](#12-large-questions)


# 1. Question sets

Questions sets are structures that contain the questions for a given part of the exam. There is two type of set: short and large.

They are store in the `database` folder and their configuration is done in the `config.yaml` file (see [configuration](configuration.md))


## 1.1. Short questions

The short questions set contains small questions that are a few lines at most. Theses questions can only contains text, no image or code block.

The questions will be displayed as list of enumerated question with some optional blank spaces in between.

The questions have to be store in a single `.txt` or `.md` file, with one question by line.

```
.
└── database/
    └── short_questions.txt
```


Example of such dataset can be seen in [database-example/short_questions.txt](database_example/short_questions.txt)

## 1.2. Large questions

The large questions set contains bigger question with optional image or code block.

Each questions is stored in it own `n_question.md` file, where `n` is the index of the question (start at 1, SHOULD BE CONTINUOUS). These files should be contain in a folder that is used for the `dataset_path` parameter.

```
.
└── database/
    └── large_questions/
        ├── 1_question.md
        ├── 2_question.md
        ├── image.png
        └── ...
```

The question can have the following elements (using markdown syntax):

- custom title: declared on the first line with a header 1 (i.e. `# My favorite question`).
- image: declared using the markdown syntax (i.e. `![alt text](path/to/image.png)`). The folder is used as root directory here.
- code block: with optional language specifier.

Example of such dataset can be seen in [database-example/large_question/](database_example/large_questions/)
