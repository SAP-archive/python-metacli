import shutil
import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def clean_project(path):
    shutil.rmtree(path)


def initial_file(template, name, *args, **kwargs):
    project_name = kwargs.get('project_name')
    project_path = kwargs.get('project_path')

    output = template.render(project_name = project_name)
    path = project_path + '/' + name
    return output, path
