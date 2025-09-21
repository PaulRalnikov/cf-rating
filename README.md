# cf-rating

This application generates rating of participans in given group on [codeforces](https://codeforces.com/).

# Run

```
python3 src/main.py [-h] -g GROUP [-o OUTPUT_DIRECTORY] [-e ESSENTIAL_TASKS_DIR]

options:
-h, --help            show this help message and exit
  -g GROUP, --group GROUP
                        Id of codeforces group
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Output directory (html and css files). Default - value of codeforces group code
  -e ESSENTIAL_TASKS_DIR, --essential_tasks_dir ESSENTIAL_TASKS_DIR
                        Path to directory with essetial tasks tables
```
