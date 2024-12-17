- [1. Exam](#1-exam)
- [2. Question sets](#2-question-sets)
  - [2.1. Short questions](#21-short-questions)
  - [2.2. large questions](#22-large-questions)
- [3. Example](#3-example)

The configuration is done via a `.yaml` file, with the following structure:


```yaml
exam:
  ...

sets:
  ...
```


# 1. Exam

| variable           | type | description                                      |
| ------------------ | ---- | ------------------------------------------------ |
| name               | text | The name of the course                           |
| code               | text | The code of the course                           |
| year               | text | The year of the exam                             |
| session            | text | The session of the exam                          |
| reset_page_counter | bool | Should the page counter reset between each parts |

Example:

```yaml
exam:
  name: Best courses ever
  code: BEAMS666
  year: 1873-2024
  session: 69nd
  reset_page_counter: true
... 
```


# 2. Question sets

Questions sets are structures that contain the questions for a given part of the exam. There is two type of set: short and large.

These are store in the `database` folder and the configuration is done by adding a element to the `config.yaml` `set` list as following:

```yaml
... 
sets:
  - short:
        [...]
  - large:
        [...]
```

## 2.1. Short questions

The short questions set contains small questions that are a few lines at most. Thoses questions can only contain text, no image or code block.

The questions will be displayed as list of enumerated question with some optional blank spaces in between.

The questions have to be store in a single `.txt` or `.md` file, with one question by line.

```
.
└── database/
    └── short_questions.txt
```


Example of such dataset can be seen in [database-example/short_questions.txt](database_example/short_questions.txt)

| variable   | type | description                                 |
| ---------- | ---- | ------------------------------------------- |
| name       | text | The name of the part                        |
| consigne   | text | The text to display above the part          |
| path       | text | The path inside the database                |
| size       | int  | The number of questions to pick             |
| blank_line | int  | The number of blank lines between questions |

Example:

```yaml
... 
sets:
    - short:
        name: Theory
        path: "short_questions.txt"
        size: 1
        consigne: "Chat GPT is allowed. Preparation time: $\\sim$ 10 sec."
        blank_line: 4
```

## 2.2. large questions

The large questions set contains bigger question each store in their own `n_question.md` file, where `n` is the index of the question (start at 1, SHOULD BE CONTINUOUS). All files should be contain in a folder that is used for the `dataset_path` parameter.

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

| variable   | type | description                                 |
| ---------- | ---- | ------------------------------------------- |
| name       | text | The name of the part                        |
| consigne   | text | The text to display above the part          |
| path       | text | The path inside the database                |
| size       | int  | The number of questions to pick             |
| blank_page | int  | The number of blank pages between questions |


Example:

```yaml
... 
set:
    - large:
        name: Project
        path: "large_questions"
        size: 1
        consigne: "Michel Osée is allowed for this part."
        blank_page: 1
```

# 3. Example

[config_example.yaml](config_example.yaml)

```yaml
exam:
  name: Best courses ever
  code: BEAMS666
  year: 1873-2024
  session: 69nd
  reset_page_counter: true

sets:
  - short:
      name: Theory
      path: "short_questions.txt"
      size: 1
      consigne: "Chat GPT is allowed. Preparation time: $\\sim$ 10 sec."
      blank_line: 4
  - large:
      name: Project
      path: "large_questions"
      size: 1
      consigne: "Michel Osée is allowed for this part."
      blank_page: 1
```