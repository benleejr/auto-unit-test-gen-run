#unit_test_call.py
import os
import time
import ast
import shutil
import coverage
import zipfile
import textwrap
from openai import OpenAI
import time
import unittest
import report_generator
import importlib
from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = 'tests'
app = Flask(__name__)

cors = CORS(app, resources={
    r"/api/healthchecker": {"origins": "https://auto-unit-test-gen-run.vercel.app/"},
    r"/api/run_tests": {"origins": "https://auto-unit-test-gen-run.vercel.app/"},
    r"/api/generate-pdf": {"origins": "https://auto-unit-test-gen-run.vercel.app/"},
    r"/api/download-pdf/*": {"origins": "https://auto-unit-test-gen-run.vercel.app/"},
    r"/api/upload": {"origins": "https://auto-unit-test-gen-run.vercel.app/"}
})

@app.route("/api/healthchecker", methods=["GET"])
def healthchecker():
    return {"status": "success", "message": "Integrate Flask Framework with Next.js"}

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
report_data = []
file_list = []
report_dir = os.path.join(os.getcwd(), "reports")
output_dir = os.path.join(os.getcwd(), "output")
tests_dir = os.path.join(os.getcwd(), "tests")
cov = 0
more_files_added = False

# User file upload endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
  empty_folder('output')
  data = request.get_json()
  file_content = data.get('file_content')
  file_name = data.get('file_name')
  api_key = data.get('api_key')
    
  if file_content and file_name:
    # Save the file_contents to a .py file in the folder uploads
    with open(f"uploads/{file_name}", 'w') as file:
      file.write(file_content)
    generate_tests(file_name, file_content, api_key)  # Pass the file name and its content to generate_tests to generate the unit test file.
  else:
    return 'No file content or file name provided', 400

  return 'Files uploaded successfully'

# Sends PDF to reports folder
@app.route('/reports/<filename>', methods=['GET'])
@cross_origin(origin='https://auto-unit-test-gen-run.vercel.app/', headers=['Content-Type'])
def download_pdf(filename):
    directory = os.path.join(os.getcwd(), "reports")
    return send_from_directory(directory, filename)

# Downloads ZIP results
@app.route('/output/<filename>', methods=['GET'])
@cross_origin(origin='https://auto-unit-test-gen-run.vercel.app/', headers=['Content-Type'])
def download_zip(filename):
    directory = os.path.join(os.getcwd(), "output")
    return send_from_directory(directory, filename)
   
# Loads the test module and runs the tests
def run_tests_and_capture_output(test):
    global cov
    cov = coverage.Coverage()
    cov.start()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    cov.stop()
    cov.report()
    return result

# Parse given file content for functions for import statement
def parse_file_for_funcs(file_content):
    source_code = file_content
        
    parsed_code = ast.parse(source_code)
    function_names = [node.name for node in ast.walk(parsed_code) if isinstance(node, ast.FunctionDef)]
    return function_names

# Load file contents to variable
def load_file_contents(file):
   with open(f"tests/{file}", 'r') as file:
       file_contents = file.read()
       return file_contents

#Function will generate unit tests using an API call with GPT
def generate_tests(file, file_content, key):
    file_name = os.path.splitext(file)[0]
    file_content = f"{file_content}"
           
    client = OpenAI(api_key=key)
    response = client.ChatCompletion.create(
    model="gpt-3.5-turbo-16k-0613",
    messages=[
        {
        "role": "system",
        "content": "You will be receiving programming files in Python that may be part of a larger project.\nYour goal is to write unit tests for the files given to you."+
        "Write numerous tests including various test cases.\nPut each test in its own individual class.\nDo not include from and any import statements."+
        "\nONLY give unit test code as a response that can be run.\nDO NOT give any other prompts or descriptions.\nAdd comments to the code as you see necessary.\n"+
        "Do not include anything that cannot be run by a Python compiler.\nDo not include from and any import statements at all.\nRemember to add: if __name__ == ""__main__"": unittest.main() at the end of the file."
        },
        {
        "role": "user",
        "content": file_content
        }
    ],
    temperature=1,
    max_tokens=16000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    #Get generated text only response['choices'][0]['message']['content']
    #print(f"API Response: {response}")
    
    list_of_funcs = parse_file_for_funcs(file_content)
    list_of_funcs = ', '.join(list_of_funcs)
    generated_code = f"from uploads.{file_name} import {list_of_funcs}\n"
    generated_code += "import unittest\n\n"
    generated_code += response['choices'][0]['message']['content']
    # Remove unwanted lines
    generated_code = generated_code.replace("```python", "").replace("```", "")

    #Test Line
    print(f"Generated Code: {generated_code}")

    # Write output to a new test file in the tests folder
    with open(f'tests/test_{file_name}.py', 'w') as test_file:
        test_file.write(generated_code)
        
    # Write output to a new file in the output folder so it can be zipped for the output for user.
    with open(f'output/test_{file_name}.py', 'w') as test_file:
        test_file.write(generated_code)

    return 'Test files generated successfully'

#Run Each Generated Test in the 'tests' folder.
@app.route('/api/run_tests', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://auto-unit-test-gen-run.vercel.app/', methods=['POST'], allow_headers=['Content-Type'], headers=['Access-Control-Allow-Origin'])
def run_tests():
    global report_data
    global cov
    report_data.clear()
    report_dir = os.path.join(os.getcwd(), "reports")
    
    for file in os.listdir('tests'):
        if file.startswith('test_') and file.endswith('.py'):    
            module_name = file[:-3]  # remove .py extension
            test_module = importlib.import_module(f"tests.{module_name}")
            
            # Record start time
            start_time = time.time()
            
            # Runs the tests and captures their output for creating the report.
            results = run_tests_and_capture_output(test_module)
            
            # Record end time
            end_time = time.time()
            
            total_tests = results.testsRun
            num_passed_tests = results.testsRun - (len(results.errors) + len(results.failures))
            num_errs = len(results.errors) + len(results.failures)
            file_name = file[5:]  # remove 'test_' prefix
            total_time = end_time - start_time
            formatted_time = "{:.2f}".format(total_time)
            pass_fail_ratio = ((results.testsRun - (len(results.errors) + len(results.failures))) / results.testsRun) * 100
            coverage_percentage = cov.report(file=None)
            
            # Report data is list of lists. File_name var at beginning is the title of the table.
            # The first list is the heading row for the table.
            # Second list is the results of the test
            # Third list is the error and failure output that is put below the other results in one big merged cell.
            report_data.append([
                file_name, ['Total Tests Run', 'Tests Passed', 'Total Errors', 'Runtime', 'Pass/Fail Ratio', 'Coverage'], [str(total_tests), str(num_passed_tests), str(num_errs),
                                                                                                                    f"{formatted_time} seconds", f"{pass_fail_ratio:.2f}%", f"{coverage_percentage:.2f}%",],
                [f"{format_errors_and_failures(results.errors + results.failures)}"]
            ])
        
            # Test print to console
            print("\nTest Results: ")
            print("Passed: ", num_passed_tests)
            print("Errors:", num_errs)
            print("Number of tests run:", total_tests)
    #End for Loop
                
    #Save file in /reports with a timestamp
    unique_report_filename = f"report_{int(time.time())}.pdf"
    report_file_path = os.path.join(report_dir, unique_report_filename)
    report_generator.create_pdf_report(report_data, report_file_path)
    report_generator.create_pdf_report(report_data, os.path.join(output_dir, unique_report_filename))
    unique_zip_filename = f"output_{int(time.time())}.zip"
    create_zip(unique_zip_filename)
    
    empty_folder('tests', '__init__.py')
    empty_folder('uploads')
    
    return jsonify({
        "path": unique_report_filename,
        "zip": unique_zip_filename
    })
    
# Formats errors
def format_errors_and_failures(errors_and_failures, max_line_width=140):
    formatted_errors = []
    for test, error in errors_and_failures:
        test_name = test.id()
        error_type = type(error)

        error_info = str(error)
        error_info = error_info.split('"')
        error_path = error_info[1]
        error_path = os.path.basename(error_path)
        error_info[1] = error_path
        error_info = ''.join(error_info)
        error_info = '\n'.join([textwrap.fill(line, width=max_line_width) for line in error_info.splitlines()])
        error_info.replace('\t', '')
        
        formatted_error = f"Test: {test_name}\nError Type: {error_type}\nError Info: {error_info}\n"
        formatted_errors.append(formatted_error)

    if len(formatted_errors) == 0:
        return "No errors encountered."
    else:
        return '\n'.join(formatted_errors)
    
 
# Clear out tests folder except the __init__.py file as that is necessary for imports to function.
def empty_folder(folder_path, file_to_keep=None):
    try:
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            
            if file == file_to_keep:
                continue
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        print(f"An error occured: {e}")
        
# Creates a zip file for the report and test code generated for user
def create_zip(zip_filename):
    files_to_add = list_files_in_folder(output_dir)
    with zipfile.ZipFile(os.path.join("output", zip_filename), 'w') as myzip:
        for file_to_add in files_to_add:
            myzip.write(os.path.join(os.getcwd(), "output", file_to_add), os.path.basename(file_to_add))
        
# Adds all files in the output dir to a list to be zipped
def list_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return files

if __name__ == '__main__':
    app.run(use_reloader=False)