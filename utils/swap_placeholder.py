import argparse
import sys
import os

def swap_placeholder(target_file, placeholder, source_file, output_file=None):
    """
    Replaces a placeholder in the target_file with the content of source_file.
    """
    try:
        # Check if files exist
        if not os.path.exists(target_file):
            print(f"Error: Target file '{target_file}' not found.")
            sys.exit(1)
        if not os.path.exists(source_file):
            print(f"Error: Source file '{source_file}' not found.")
            sys.exit(1)

        # Read target file
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Read source file
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()

        # Check if placeholder exists
        if placeholder not in content:
            print(f"Warning: Placeholder '{placeholder}' not found in '{target_file}'. No changes made.")
            return

        # Perform replacement
        new_content = content.replace(placeholder, source_content)

        # Determine output file
        out_path = output_file if output_file else target_file

        # Write result
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Successfully replaced '{placeholder}' with content from '{source_file}' in '{out_path}'.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Swap a placeholder in a file with content from another file.')
    parser.add_argument('target_file', help='The file containing the placeholder')
    parser.add_argument('placeholder', help='The placeholder string to replace (e.g., {{DATA_01}})')
    parser.add_argument('source_file', help='The file containing the content to inject')
    parser.add_argument('--output', '-o', help='Optional output file path (default: overwrites target_file)')

    args = parser.parse_args()

    swap_placeholder(args.target_file, args.placeholder, args.source_file, args.output)
