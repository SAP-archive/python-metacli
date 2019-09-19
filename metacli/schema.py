import shutil
import os
import jinja2


def list_files(startpath):
    """
    Show files structure based on startpath in console
    :param startpath: path
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def clean_project(path):
    """
    Delete entire project
    :param path: project path
    :return:
    """
    shutil.rmtree(path)


def create_file(template, name, *args, **kwargs):
    project_name = kwargs.get('project_name')
    project_path = kwargs.get('project_path')
    root_name = kwargs.get('root_name')

    output = template.render(project_name = project_name, root_name = root_name)
    path = project_path + '/' + name
    return output, path


def parse_cli(parent, data, template):
    """
    create the cli body content recursively
    :param parent: parent command / group name
    :param data: current command / group dict
    :param template: command / group body template
    :return: generated content for current group / command
    """

    output = ""

    for group in data:

        group_param_query = ['name', 'help', 'hidden']
        parsed_group_param = {key : group[key] for key in group_param_query}

        convertor = DataTypeConvertor()

        parsed_group_param = convertor.convert_all(parsed_group_param)

        option_params = group['params'] if "params" in group.keys() else []

        parsed_option_param = []
        for option_param in option_params:
            if option_param['param_type'] != 'option':
                continue
            del option_param['param_type']

            tmp = convertor.convert_all(option_param)
            tmp["argument"] = tmp["name"][1:-1]
            tmp['name'] = "\"" + "--" + tmp['name'][1:]
            parsed_option_param.append(tmp)

        group_param = [Data(k, v) for (k, v) in parsed_group_param.items()]

        option_param = []
        for option in parsed_option_param:
            tmp = []
            for key in option:
                if key == "name":
                    tmp.insert(0, Data(key, option[key]))
                else:
                    tmp.append(Data(key, option[key]))
            option_param.append(tmp)

        click_type = "group" if "groups" in group else "command"
        output += template.render(click_type=click_type,
                                        parent_name=parent if parent else "click",
                                        group_param=group_param,
                                        group_name=group['name'],
                                        options_param= option_param
                                        )
        if "commands" in group:
            next_output = parse_cli(group['name'],
                                          group['commands'],
                                          template)
            output += next_output

        if "groups" in group:
            next_output = parse_cli(group['name'],
                                          group['groups'],
                                          template)
            output += next_output

    return output


def create_empty_files(templates, names, project_name, project_path, root_name):
    """
    Generate an empty command line project based on templates and names
    :param templates (list): templates to generate files
    :param names (list): file names
    :param project_name (str):
    :param prject_path (str):
    :param root_name:
    :return: outputs (list): generated content for files
             paths (list): generated files' path
    """
    outputs = []
    paths = []

    assert len(templates) == len(names), "The lengths for templates and files are not equal"

    for (template, file_name) in zip(templates, names):
        content, path = create_file(template=template,
                                    name=file_name,
                                    project_name=project_name,
                                    project_path=project_path,
                                    root_name = root_name)

        outputs.append(content)
        paths.append(path)

    return outputs, paths





class Data:

    def __init__(self, name, val):
        self.name = name
        self.val = val


class DataTypeConvertor:

    def __init__(self):
        self.data_mapping = {
            'INT':'int',
            'STRING':'str',
            'str':'str',
            'None': 'None',
            'boolean': 'boolean',
            'BOOL': "boolean",
            'name': 'str',
            'help': 'str',
            'prompt':'str',
            'required':"boolean",
            'hidden': "boolean"
        }

        self.func_mapping = {
            "boolean" : self.parse_boolean,
            "str": self.parse_string,
            "None": self.parse_none,
            "int": self.parse_int
        }

    def convert_all(self, data_list):
        old = data_list
        new = {}

        if 'type' in old.keys():
            if old['default'] != 'None':
                new['default'] = self.convert(old['default'], old['type'])
                del old['default']
            del old['type']


        for key in old.keys():
            if old[key] == 'None':
                new[key] = self.convert(old[key], 'None')
            else:
                new[key] = self.convert(old[key], key)

        return new

    def convert(self, data, data_type):
        if data_type not in self.data_mapping.keys():
            raise KeyError("Unsopport Data Type: ", data_type)

        return self.func_mapping[self.data_mapping[data_type]](data)

    def parse_boolean(self, data):
        if data == "False":
            return False
        elif data == "True":
            return True
        else:
            raise ValueError("Invalid Boolean", data)

    def parse_string(self, data):
        return "\"{}\"".format(data)

    def parse_none(self, data):
        return data

    def parse_int(self, data):
        return data

