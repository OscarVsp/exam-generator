- [1. Sets of questions](#1-sets-of-questions)
- [2. Configuration](#2-configuration)
- [3. Student list](#3-student-list)
- [4. Usage](#4-usage)
  - [4.1. Docker](#41-docker)
  - [4.2. Source](#42-source)
    - [4.2.1. Installation](#421-installation)
    - [4.3. Usage](#43-usage)


# 1. Sets of questions

see [database](database.md)

# 2. Configuration

see [configuration](configuration.md)

# 3. Student list

The list of the students is stored in a `.csv` file with the following structure:

| lastname           | firstname           | ID          |
| ------------------ | ------------------- | ----------- |
| student1 last name | student1 first name | student1 id |
| student2 last name | student2 first name | student2 id |
| ...                | ...                 | ...         |

The first line contains the column title. see [students_list.csv](../students_list_example.csv) for an example.

# 4. Usage

## 4.1. Docker

To used the generator via docker, you can create a `docker-compose.yaml` file using this template:

```yaml
services:
  app:
    image: oscarvsp/exam-generator:latest
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./students_list.csv:/app/students_list.csv
      - ./database:/app/database
      - ./output:/app/output
```

Given that your folder structure look like this:

```
.
├── database/
│   └── ...
├── output/
├── config.yaml
├── docker-compose.yaml
└── students_list.csv
```

Then run the following command to generate the pdf:

`docker composer up --build`


## 4.2. Source

### 4.2.1. Installation

```sh
git clone https://github.com/OscarVsp/exam_generator.git 
cd exam_generator
make install
```

This will clone the repo and install the requirements (`texlive`, `latexmk`, `texlive-xetex` and `python3-yaml`).

### 4.3. Usage

The parent folder containing the `exam_generator` should look like this:

```
.
├── database/
│   └── ...
├── exam_generator/
│   └── ...
├── output/
├── config.yaml
└── students_list.csv
```

From this folder, you can run the following command to generate the pdf:

```sh
make -C exam_generator CONF=config.yaml STUDENTS=students_list.csv DS_PATH=database/ OUTPUT_PATH=output
```

