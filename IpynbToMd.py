import os
import nbformat
import shutil
import pandas as pd
import pathlib


def convert_ipynb_to_markdown(ipynb_file):
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    markdown_content = []

    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            markdown_content.append(cell.source)
        elif cell.cell_type == 'code':
            markdown_content.append(f"```python\n{cell.source}\n```")

    return "\n\n".join(markdown_content)


def convert_csv_to_markdown(csv_file):
    df = pd.read_csv(csv_file)
    markdown_table = df.to_markdown(index=False)
    return markdown_table


def convert_folder_to_markdown(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            input_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, folder_path)
            output_dir = os.path.join(output_folder, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            if filename.endswith('.ipynb'):
                markdown_content = convert_ipynb_to_markdown(input_file_path)
                md_filename = filename.replace('.ipynb', '.md')
                md_file_path = os.path.join(output_dir, md_filename)

                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)

                print(f"Converted {input_file_path} to {md_file_path}")

            elif filename.endswith('.csv'):
                markdown_table = convert_csv_to_markdown(input_file_path)
                md_filename = filename.replace('.csv', '.md')
                md_file_path = os.path.join(output_dir, md_filename)

                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_table)

                print(f"Converted {input_file_path} to {md_file_path}")
            else:
                output_file_path = os.path.join(output_dir, filename)
                shutil.copy(input_file_path, output_file_path)

                print(f"Copied {input_file_path} to {output_file_path}")


if __name__ == '__main__':
    print("Enter the path for input folder: ")
    temp = input()
    top_folder_path = pathlib.Path(temp)
    print("Enter the path for output folder: ")
    temp = input()
    output_folder_path = pathlib.Path(temp)
    convert_folder_to_markdown(top_folder_path, output_folder_path)
