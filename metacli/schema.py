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


class ProjectGenerator:

    def __init__(self, project_path, project_name):
        self.project_path = project_path
        self.project_name = project_name

        if os.path.exists(project_path):
            delete = input("Already Existed, would you want to replace? y/n \n")
            if delete == 'y' or delete == 'Y':
                self.clean_project()
            else:
                raise FileExistsError

        os.mkdir(project_path)

    def create_empty_files(self, templates, names, root_name):
        """
        Generate an empty command line project based on templates and names
        :param templates (list): templates to generate files
        :param names (list): file names
        :param root_name:
        :return: outputs (list): generated content for files
                 paths (list): generated files' path
        """
        outputs = []
        paths = []

        assert len(templates) == len(names), "The lengths for templates and files are not equal"

        for (template, file_name) in zip(templates, names):
            content, path = self.create_file(template=template,
                                             name=file_name,
                                             root_name=root_name)

            outputs.append(content)
            paths.append(path)

        return outputs, paths

    def clean_project(self):
        """
        Delete entire project
        :param path: project path
        :return:
        """
        shutil.rmtree(self.project_path)

    def create_file(self, template, name, root_name):

        output = template.render(project_name=self.project_name, root_name=root_name)
        path = self.project_path + '/' + name
        return output, path

    def generate_cli_from_data(self, env, schema, root_name):
        """
        :param env: template engine environment
        :param schema: schema data
        :return: generated cli file
        """
        # generate cli file
        # generate cli body
        cli_template = env.get_template('cli_body.txt')

        cli_body_output = ""
        cli_body_output += self.parse_cli(None, schema, cli_template)

        # add header and end to cli
        cli_start_template = env.get_template("cli_start.txt")
        cli_end_template = env.get_template("cli_end.txt")
        cli_output = cli_start_template.render() + cli_body_output + cli_end_template.render(root=root_name)
        cli_path = self.project_path + '/' + self.project_name + 'cli.py'

        return cli_output, cli_path

    def parse_cli(self, parent, data, template):
        """
        create the cli body based on schema recursively
        :param parent: parent command / group name
        :param data: current command / group dict
        :param template: command / group body template
        :return: generated content for current group / command
        """

        output = ""

        for group in data:

            # parse parameters to template writable string
            group_param_query = ['name', 'help', 'hidden']
            parsed_group_param = {key: group[key] for key in group_param_query}

            convertor = DataTypeConvertor()

            parsed_group_param = convertor.convert_all(parsed_group_param)

            option_params = group['params'] if "params" in group.keys() else []

            # make sure the parameter is option and process the name as special case
            parsed_option_param = []
            for option_param in option_params:
                if option_param['param_type'] != 'option':
                    continue
                del option_param['param_type']

                # process the name field since the code needs to be --<name> instead of name = <name>
                tmp = convertor.convert_all(option_param)
                tmp["argument"] = tmp["name"][1:-1]
                tmp['name'] = "\"" + "--" + tmp['name'][1:]
                parsed_option_param.append(tmp)

            # construct a list for writing template
            group_param = [Data(k, v) for (k, v) in parsed_group_param.items()]

            # process name specifically since name must be at first place in code
            option_param = []
            for option in parsed_option_param:
                tmp = []
                for key in option:
                    if key == "name":
                        tmp.insert(0, Data(key, option[key]))
                    else:
                        tmp.append(Data(key, option[key]))
                option_param.append(tmp)

            # use groups to identify if this is a group or command schema
            click_type = "group" if "groups" in group else "command"
            output += template.render(click_type=click_type,
                                      parent_name=parent if parent else "click",
                                      group_param=group_param,
                                      group_name=group['name'],
                                      options_param=option_param
                                      )
            # dfs to next commands
            if "commands" in group:
                next_output = self.parse_cli(group['name'],
                                             group['commands'],
                                             template)
                output += next_output

            # dfs to next groups
            if "groups" in group:
                next_output = self.parse_cli(group['name'],
                                             group['groups'],
                                             template)
                output += next_output

        return output

    def append_schema_template(self, env, output, path):
        schema_json_output = env.get_template('schema_json.txt').render()
        schema_yaml_output = env.get_template('schema_yaml.txt').render()
        path.append(self.project_path + '/' + 'schema.json')
        path.append(self.project_path + '/' + 'schema.yaml')
        output.append(schema_json_output)
        output.append(schema_yaml_output)

        return output, path

    def write_files(self, output, path):
        try:
            for output, file in zip(output, path):
                with open(file, 'w') as f:
                    f.write(output)
        except Exception as e:
            print(e)
            if os.path.exists(self.project_path):
                self.clean_project()
                print("cleaned project")


class Data:

    def __init__(self, name, val):
        """
        This class is used to load data when writing template
        """
        self.name = name
        self.val = val


class DataTypeConvertor:

    def __init__(self):
        """
        This class is used to parse the data type from JSON to date type we use when writing template
        """
        # Define the mapping between different data type
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

        # Define the data type and the function which can parse data for writing template
        self.func_mapping = {
            "boolean" : self.parse_boolean,
            "str": self.parse_string,
            "None": self.parse_none,
            "int": self.parse_int
        }

    def convert_all(self, data_list):
        """
        :param data_list: the dict as {field_name : field argument}
        :return: the dict as {field_name: field argument which is good for writing template}
        """
        old = data_list
        new = {}

        # If the type is already defined, use the data type instead of default mapping between data type
        if 'type' in old.keys():
            if old['default'] != 'None':
                new['default'] = self.convert(old['default'], old['type'])
                del old['default']
            del old['type']

        # convert all data type into writable type in template
        for key in old.keys():
            if old[key] == 'None':
                new[key] = self.convert(old[key], 'None')
            else:
                new[key] = self.convert(old[key], key)

        return new

    def convert(self, data, data_type):
        """
        :param data: data which needs to be converted
        :param data_type: data type for the data
        :return: data which can be written to template
        """

        if data_type not in self.data_mapping.keys():
            raise KeyError("Unsupported data type in converted: ", data_type)

        return self.func_mapping[self.data_mapping[data_type]](data)

    def parse_boolean(self, data):
        if data == "False":
            return False
        elif data == "True":
            return True
        else:
            raise ValueError("Invalid boolean in converted", data)

    def parse_string(self, data):
        return "\"{}\"".format(data)

    def parse_none(self, data):
        return data

    def parse_int(self, data):
        return data

