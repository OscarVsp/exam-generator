- [1. Dependencies](#1-dependencies)
- [2. Configuration](#2-configuration)
- [3. Usage](#3-usage)
- [4. Questions sets](#4-questions-sets)
  - [4.1. Short questions set](#41-short-questions-set)
  - [4.2. Large questions set](#42-large-questions-set)
- [5. TODOs](#5-todos)

# 1. Dependencies


`make install`

# 2. Configuration

The configuration is done via the `[config.yaml](config.yaml)` file.

TODO better doc

# 3. Usage 

`make CONFIG=config.yaml`


# 4. Questions sets

Questions sets are structures that contain the questions for a given part of the exam. There is two type of Questions sets:

## 4.1. Short questions set

The short questions set contains small questions that are a few lines at most. Thoses questions can only contain text, no image or code block.

The questions will be displayed as list of enumerated question with some optional blank spaces in between.

The questions have to be store in a `.txt` or `.md` file, with one question by line.

Example of such dataset can be seen in [database-example/short_questions.txt](database_example/short_questions.txt)


## 4.2. Large questions set

The large questions set contains bigger question each store in their own `n_question.md` file, where `n` is the index of the question (start at 1, SHOULD BE CONTINUOUS). All files should be contain in a folder that is used for the `dataset_path` parameter.

The question can have the following elements (using markdown syntax):

- custom title: declared on the first line with a header 1 (i.e. `# My favorite question`).
- image: declared using the markdown syntax (i.e. `![alt text](path/to/image.png)`). The folder is used as root directory here.
- code block: with optional language specifier.

Example of such dataset can be seen in [database-example/large_question/](database_example/large_questions/)


# 5. TODOs

- Debug, logs and exception handler
- Clean latex packages
- Better docs
- Make a docker image ?