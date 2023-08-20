from VMACompiler import VMACompiler
import ErrorLog
import sys

if __name__ == "__main__":
    # Check if file path is provided, otherwise exit
    if len(sys.argv) != 2:
        print("Usage: python compile.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Capture the file path from command line arguments

    compiler = VMACompiler(file_path)
    output_path = compiler.compile_to_vmf()

    if not ErrorLog.log:
        print(f"Successfully Compiled {file_path} to {output_path}")
    for error in ErrorLog.log:
        print(f"{error['line']}: {error['message']}")
