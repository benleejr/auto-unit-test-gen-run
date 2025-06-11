import os
import argparse
import shutil
import ast
import time
import importlib
import unittest
import coverage
import zipfile
import textwrap
from openai import OpenAI
import report_generator

# Directories used for processing
UPLOADS_DIR = 'uploads'
TESTS_DIR = 'tests'
OUTPUT_DIR = 'output'
REPORTS_DIR = 'reports'


def ensure_dirs():
    for d in [UPLOADS_DIR, TESTS_DIR, OUTPUT_DIR, REPORTS_DIR]:
        os.makedirs(d, exist_ok=True)


def parse_file_for_funcs(source_code: str):
    parsed_code = ast.parse(source_code)
    return [n.name for n in ast.walk(parsed_code) if isinstance(n, ast.FunctionDef)]


def generate_tests(file_path: str, api_key: str):
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    with open(file_path, 'r') as fh:
        file_content = fh.read()

    shutil.copy(file_path, os.path.join(UPLOADS_DIR, file_name))

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be receiving programming files in Python that may be part of a larger project."
                    "Your goal is to write unit tests for the files given to you."
                    "Write numerous tests including various test cases."
                    "Put each test in its own individual class."
                    "Do not include from and any import statements."
                    "ONLY give unit test code as a response that can be run."
                    "DO NOT give any other prompts or descriptions."
                    "Add comments to the code as you see necessary."
                    "Do not include anything that cannot be run by a Python compiler."
                    "Do not include from and any import statements at all."
                    "Remember to add: if __name__ == '__main__': unittest.main() at the end of the file."
                ),
            },
            {"role": "user", "content": file_content},
        ],
        temperature=1,
        max_tokens=16000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    list_of_funcs = ', '.join(parse_file_for_funcs(file_content))
    generated_code = f"from {UPLOADS_DIR}.{base_name} import {list_of_funcs}\n"
    generated_code += "import unittest\n\n"
    generated_code += response.choices[0].message.content
    generated_code = generated_code.replace("```python", "").replace("```", "")

    with open(os.path.join(TESTS_DIR, f"test_{base_name}.py"), 'w') as fh:
        fh.write(generated_code)
    with open(os.path.join(OUTPUT_DIR, f"test_{base_name}.py"), 'w') as fh:
        fh.write(generated_code)


def run_tests_and_capture_output(test_module):
    cov = coverage.Coverage()
    cov.start()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    cov.stop()
    cov.report()
    return result, cov


def format_errors_and_failures(errors_and_failures, max_line_width=140):
    formatted = []
    for test, error in errors_and_failures:
        test_name = test.id()
        error_type = type(error)
        error_info = str(error)
        error_info = '\n'.join([
            textwrap.fill(line, width=max_line_width) for line in error_info.splitlines()
        ])
        formatted.append(
            f"Test: {test_name}\nError Type: {error_type}\nError Info: {error_info}\n"
        )
    if not formatted:
        return "No errors encountered."
    return '\n'.join(formatted)


def run_all_tests():
    report_data = []
    for file in os.listdir(TESTS_DIR):
        if file.startswith('test_') and file.endswith('.py'):
            module_name = file[5:-3]
            test_module = importlib.import_module(f"{TESTS_DIR}.{module_name}")
            start = time.time()
            results, cov = run_tests_and_capture_output(test_module)
            end = time.time()

            total_tests = results.testsRun
            passed = total_tests - (len(results.errors) + len(results.failures))
            num_errs = len(results.errors) + len(results.failures)
            runtime = f"{end - start:.2f} seconds"
            ratio = ((passed) / total_tests) * 100 if total_tests else 0
            coverage_percent = cov.report(file=None)
            report_data.append([
                file,
                ['Total Tests Run', 'Tests Passed', 'Total Errors', 'Runtime', 'Pass/Fail Ratio', 'Coverage'],
                [str(total_tests), str(passed), str(num_errs), runtime, f"{ratio:.2f}%", f"{coverage_percent:.2f}%"],
                [format_errors_and_failures(results.errors + results.failures)],
            ])

    report_file = os.path.join(REPORTS_DIR, f"report_{int(time.time())}.pdf")
    report_generator.create_pdf_report(report_data, report_file)

    zip_name = os.path.join(OUTPUT_DIR, f"output_{int(time.time())}.zip")
    with zipfile.ZipFile(zip_name, 'w') as myzip:
        for fname in os.listdir(OUTPUT_DIR):
            myzip.write(os.path.join(OUTPUT_DIR, fname), fname)
        for fname in os.listdir(REPORTS_DIR):
            myzip.write(os.path.join(REPORTS_DIR, fname), fname)

    return report_file, zip_name


def main():
    parser = argparse.ArgumentParser(description="Generate unit tests and run them without a web server")
    parser.add_argument('files', nargs='+', help='Python files to process')
    parser.add_argument('--api-key', required=True, help='OpenAI API key')
    args = parser.parse_args()

    ensure_dirs()
    for path in args.files:
        generate_tests(path, args.api_key)
    pdf, zip_path = run_all_tests()
    print(f"Report saved to {pdf}")
    print(f"Results archived in {zip_path}")


if __name__ == '__main__':
    main()
