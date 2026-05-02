from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

for case in test_cases:
    print(f"testing: {case}")
    print(get_files_info(*case))
