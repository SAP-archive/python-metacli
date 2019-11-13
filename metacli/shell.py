import click
import cmd
import json
import pickle
import os
import time
import warnings
import sys

class MainShell(cmd.Cmd):

    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx
        self.prompt = ctx.command.name + " > "
        self.group = ctx.command.name + " > "
        self.debug_parameters_history = {}
        self.shell_available_commands = []
        self.shell_parameters_current_session = {}
        self.shell_parameters_previous_session= {}
        self.transfer_parameters_shells = {}
        self.shell_group_saved_parameters = {}


class Shell(MainShell):

    def __init__(self, ctx, root_shell = False):
        MainShell.__init__(self, ctx)
        self.intro = ":q / :quit to quit; :h / :help to list all commands and parameters; :shell_history / " \
                     ":sh to show saved parameters value; :set / :s set parameter value"
        self.root_shell = root_shell
        if root_shell:
            self.set_root_context_obj_and_param_dict_sys_argv(ctx)
        else:
            self.set_context_obj(ctx)
        self.get_available_commands()

    def set_root_context_obj_and_param_dict_sys_argv(self, ctx):
        ''' To gather parameters for root plugin group from system args '''
        command = ctx.__dict__["command"]
        param_values = sys.argv[1:len(sys.argv) - 1]

        ctx_param_dict = {}

        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                param_opts = param.__dict__["opts"]
                param_count = param.__dict__["count"]
                param_default = param.__dict__["default"]

                p = str(param_opts[0])
                if param_count:
                    value_list = self.gather_param_for_base(param_values, p, count=True)
                    ctx_param_dict[param_name] = len(value_list[0])
                elif p not in param_values:
                    ctx_param_dict[param_name] = param_default
                else:
                    value_list = self.gather_param_for_base(param_values, p)
                    if len(value_list) < 2:
                        ctx_param_dict[param_name] = value_list[0]
                    else:
                        ctx_param_dict[param_name] = tuple(value_list)

        ctx.__dict__["params"] = ctx_param_dict

        self.set_context_obj(ctx)

        self.update_parameter_values_dict(command, ctx)

    def gather_param_for_base(self, list, param, count=False):
        ''' Helper function to get values for specific parameter '''
        gather = False

        param_values = []

        for p in list:
            if count and param in p:
                param_values.append(p)
            elif p == param:
                gather = True
            elif "--" in p or "-" in p:
                gather = False
            elif gather:
                param_values.append(p)

        return param_values

    def load_parameters_file(self):
        ''' load dictionary of saved parameters from file '''

        file = ".parameters_history"

        try:
            with open(file, "rb") as f:
                my_dicts = pickle.load(f)
                self.debug_parameters_history, self.transfer_parameters_shells = my_dicts

        except Exception as e:
            self.debug_parameters_history = {}

    def save_parameters_file(self):
        ''' Save the parameters dict in hidden file '''

        file = ".parameters_history"

        with open(file, "wb") as f:
            my_dicts = [self.debug_parameters_history, self.transfer_parameters_shells]
            pickle.dump(my_dicts, f)

    def log_shell_history(self, line):
        ''' log commands run in shell to file '''

        file = "shell_history"

        command_name = line.split()[0]
        args = line.split()[1:]

        subcommand = self.ctx.command.commands.get(command_name)

        if subcommand:
            shell_stmt = "shell: " + self.group #self.prompt
            cmd_stmt = "command: " + command_name
            arg_stmt = "arguments: " + str(args)

            with open(file, "a") as f:
                json.dump(shell_stmt, f)
                f.write("\n")
                json.dump(cmd_stmt, f)
                f.write("\n")
                json.dump(arg_stmt, f)
                f.write("\n\n")
        else:
            shell_stmt = "shell: " + self.group # self.prompt
            cmd_stmt = "command: " + line

            with open(file, "a") as f:
                json.dump(shell_stmt, f)
                f.write("\n")
                json.dump(cmd_stmt, f)
                f.write("\n\n")

    def get_available_commands(self):
        ''' Get the commands user able to access'''

        # clear the list of available commands each time shell called
        if self.shell_available_commands:
            self.shell_available_commands = []

        for cmd in self.ctx.command.commands:
            self.shell_available_commands.append(cmd)

    def get_saved_parameters(self, group_name, is_group, command):
        '''
        Get saved parameters from dictionary and decide whether to use those values
        :param command: command just run in shell
        :return: list of parameters
        '''
        # saved_args_list hold the list of parameters return and used when run command
        saved_args_list = []

        # values used to indicate the type of param (saved, default), its value, value_type
        param_type = ""
        param_value = []
        value_bool = False

        group_param_level_dict = {}
        if group_name in self.shell_parameters_current_session:
            group_param_level_dict = self.shell_parameters_current_session[group_name]

        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                param_opts = param.__dict__["opts"]
                param_count = param.__dict__["count"]
                param_default = param.__dict__["default"]
                param_multiple = param.__dict__["multiple"]
                param_type = param.__dict__["type"]
                if param_opts:
                    opt = str(param_opts[0])
                    # get the type of parameter and its value)
                    if group_param_level_dict and param_name in group_param_level_dict:
                        value = group_param_level_dict[param_name][-1]
                        param_type = "saved"
                    else:
                        found_saved_param, saved_value = self.search_value_in_history(param_name)
                        if found_saved_param and not is_group:
                            value = saved_value
                            param_type = "saved"
                        elif param_default is not None or param_default is None:
                            if isinstance(param_type, click.types.BoolParamType):
                                value_bool = True
                            value = param_default
                            param_type = "default"
                        else:
                            return "Error", opt, None, None

                    # format parameters for hint message
                    if isinstance(value, str) and not value:
                        param_value.append(opt + " = ''")
                    else:
                        param_value.append(opt + " = " + str(value))

                    # create args list for parsing command based on option type
                    if param_count:
                        for i in range(0, int(value)):
                            saved_args_list.append(opt)
                    elif param_multiple:
                        for arg in value:
                            saved_args_list.append(opt)
                            saved_args_list.append(arg)
                    elif isinstance(value, tuple):
                        saved_args_list.append(opt)
                        for arg in value:
                            saved_args_list.append(arg)
                    else:
                        saved_args_list.append(opt)
                        saved_args_list.append(value)

        return param_type, param_value, saved_args_list, value_bool

    def search_value_in_history(self, param_name):
        ''' Helper function to search for param values '''
        found_param = False
        value = ""
        for group, param_list in self.shell_parameters_previous_session.items():
            # Get saved param value if value is not a saved value for group parameter options
            group_options = self.transfer_parameters_shells["group_options"][group]
            if param_name in param_list and param_name not in group_options:
                found_param = True
                value = param_list[param_name][-1]

        return found_param, value

    def set_context_obj(self, context):

        ''' Set context object to save parameter value'''

        if context.obj is None:
            context.obj = {}

        if self.shell_group_saved_parameters is None:
            self.shell_group_saved_parameters = {}

        context_parameters = context.__dict__["params"]

        for param, value in context_parameters.items():
            context.obj[param] = value

        if "logger" in context.__dict__["command"].__dict__:
            context.obj["logger"] = context.__dict__["command"].__dict__["logger"]

        self.update_parameter_options_dict(context)


    def update_transfer_parameters_shells(self, enter_value = False, exit_value=False, new_prompt="", new_context=None):
        ''' Save parameters values for group (based on prompt ) for nested levels'''
        self.transfer_parameters_shells["Entering"] = enter_value
        self.transfer_parameters_shells["Exited"] = exit_value

        pass_parameter_dict = {}
        pass_group_option = {}

        if "parameters" in self.transfer_parameters_shells:
            for param, value in self.transfer_parameters_shells["parameters"].items():
                if param != self.group and param != new_prompt:
                    pass_parameter_dict[param] = value

        if "group_options" in self.transfer_parameters_shells:
            for param, value in self.transfer_parameters_shells["group_options"].items():
                if param != self.group and param != new_prompt:
                    pass_group_option[param] = value

        cur_group_level_param_dict = {}
        if self.group in self.shell_parameters_current_session:
            cur_group_level_param_dict = self.shell_parameters_current_session[self.group]

        if enter_value:
                new_prompt_param_dict = {}
                if new_context is not None:
                    param_new_command = new_context.__dict__["command"].params
                    for param in param_new_command:
                        param_name = param.__dict__["name"]
                        if cur_group_level_param_dict and param_name in cur_group_level_param_dict:
                            param_val = cur_group_level_param_dict[param_name]
                            if len(param_val) > 1:
                                cur_group_level_param_dict[param_name] = param_val[:-1]
                                new_prompt_param_dict[param_name] = [param_val[-1], ]
                            else:
                                new_prompt_param_dict[param_name] = cur_group_level_param_dict[param_name]
                                del cur_group_level_param_dict[param_name]
                        if self.shell_group_saved_parameters and param_name in self.shell_group_saved_parameters:
                            param_val = self.shell_group_saved_parameters[param_name]
                            if len(param_val) > 1:
                                self.shell_group_saved_parameters[param_name] = param_val[:-1]
                            else:
                                del self.shell_group_saved_parameters[param_name]

                pass_parameter_dict[new_prompt + " > "] = new_prompt_param_dict
                pass_parameter_dict[self.group] = cur_group_level_param_dict
                pass_group_option[self.group] = self.shell_group_saved_parameters

        self.transfer_parameters_shells["parameters"] = pass_parameter_dict
        self.transfer_parameters_shells["group_options"] = pass_group_option

        self.save_parameters_file()

    def update_parameter_values_dict(self,command, context):
        ''' Update the parameter dictionary object with new values '''

        context_parameters = context.__dict__["params"]

        group_param_dict = {}

        if self.group in self.shell_parameters_current_session:
            group_param_dict = self.shell_parameters_current_session[self.group]

        # Get the latest param values from context and update dictionary
        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                param_type = param.__dict__["type"]
                if param_name in context_parameters and not isinstance(param_type, click.types.BoolParamType):
                    if param_name not in group_param_dict:
                        group_param_dict[param_name] = [context_parameters[param_name],]
                    else:
                        group_param_dict[param_name].append(context_parameters[param_name])
                self.shell_parameters_current_session[self.group] = group_param_dict
                self.debug_parameters_history[self.group] = group_param_dict

        # Save the parameters to file to always get the latest value
        self.save_parameters_file()

        # Reset the parameters in context for each loop to avoid unexpected key error
        context.__dict__["params"] = {}

    def update_parameter_options_dict(self, context, param=""):
        """
        Update saved parameters of the group
        :param context:
        :return:
        """

        ctx_obj = context.obj
        ctx_param = context.__dict__["command"].params

        if param and param in self.shell_group_saved_parameters:
            self.shell_group_saved_parameters[param].append(ctx_obj[param])
        else:
            for param in ctx_param:
                param_name = param.__dict__["name"]
                if param_name in ctx_obj:
                    if param_name not in self.shell_group_saved_parameters:
                        self.shell_group_saved_parameters[param_name] = [ctx_obj[param_name], ]
                    else:
                        self.shell_group_saved_parameters[param_name].append(ctx_obj[param_name])

    def set_and_pass_context_obj(self, nested_shell_context):
        # set the context of nested shell for click group found
        self.set_context_obj(nested_shell_context)

        # transfer the param and value in context obj of current shell to the nested shell
        for param, value in self.ctx.obj.items():
            nested_shell_context.obj[param] = value

    def parse_parameters_and_update_dictionary(self, ctx, args, command, bool_type):
        """
        Parse parameters of command in context and update param dictionary with new param values
        :param ctx: context of the command
        :param args: parameters passed in to command
        :param command: command run in the shell
        """

        if not bool_type:
            # parse the parameters passed in context
            command.parse_args(ctx, args)

        # For commands that are Groups, before invoking those commands, need to save the parameters
        # to the context object to allow commands under that Group to use those parameters
        if isinstance(command, click.Group):
            self.set_context_obj(ctx)

        # invoke the command
        ctx.forward(command)

        # updates parameter value to dictionary
        self.update_parameter_values_dict(command, ctx)

    def do_exit(self):
        ''' Exit the shell '''
        print("Exiting")
        self.update_transfer_parameters_shells(enter_value= False, exit_value=True)
        if self.root_shell:
            if os.path.exists(".parameters_history"):
                os.remove(".parameters_history")
        return True

    def do_myhelp(self):
        ''' show all the commands and parameters '''
        print("Available commands for use: ")
        if not self.shell_available_commands:
            print("None")
        else:
            for command in self.shell_available_commands:
                print(command)

        print("\nSaved Parameters: ")
        if not self.shell_group_saved_parameters:
            print("None")
        else:
            for param, value in self.shell_group_saved_parameters.items():
                print("parameter: " + param)
                val = value[-1]
                if isinstance(val, str) and not val:
                    print("''")
                else:
                    print(str(val))

    def do_history(self, arg):
        ''' Print parameter history'''
        if arg and arg[0] == "--debug":
            print("History of parameters of all sessions")
            self.print_dictionaries(self.debug_parameters_history)
        else:
            print("History of parameters in previous shell session")
            self.print_dictionaries(self.shell_parameters_previous_session)

            print("\nHistory of parameters in current shell session")
            self.print_dictionaries(self.shell_parameters_current_session)

    def print_dictionaries(self, shell_attribute_dictionary):
        ''' Helper function to print parameter dictionaries '''
        for group, param_list in shell_attribute_dictionary.items():
            if param_list:
                print("group: " + group)
                for param, param_values in param_list.items():
                    print("parameter: " + param)
                    print("values: " + str(param_values))
                    print()

    def do_set(self, args):
        ''' set the parameter to have value '''
        arg_list = args[0].split("=")
        if len(arg_list) < 2:
            print("Cannot set the parameter")
        elif len(arg_list) > 2:
            print("Can only set one parameter at a time")
        else:
            parameter = arg_list[0]
            value = arg_list[1]

            group_param_level_dict = self.shell_parameters_current_session[self.group] #self.prompt]
            if parameter not in self.shell_group_saved_parameters and parameter not in group_param_level_dict:
                print("Cannot set the nonexistent parameter")
            else:
                print("Set parameter " + parameter + " = " + value)
                if parameter in self.ctx.obj:
                    self.ctx.obj[parameter] = value
                    self.update_parameter_options_dict(self.ctx, param=parameter)


                if parameter in group_param_level_dict:
                    group_param_level_dict[parameter].append(value)
                    self.shell_parameters_current_session[self.group] = group_param_level_dict
                    self.debug_parameters_history[self.group] = group_param_level_dict

            # Save the parameters to file to always get the latest value
            self.save_parameters_file()

    def precmd(self, line):
        ''' Overwrite precmd command to load saved parameters and history
        :param line: command run in shell
        :return: command run in shell
        '''
        # log the commands information
        self.log_shell_history(line)

        # each time load saved parameters in case value changes
        self.load_parameters_file()

        self.setup_parameters()

        self.get_available_commands()

        return line

    def setup_parameters(self):
        ''' Set up parameter dictionaries for shell session'''
        if "Entering" in self.transfer_parameters_shells and self.transfer_parameters_shells["Entering"]:
            if "parameters" in self.transfer_parameters_shells:
                for group, param_list in self.transfer_parameters_shells["parameters"].items():
                    if group == self.group :
                        self.shell_parameters_current_session[group] = param_list
                    else:
                        self.shell_parameters_previous_session[group] = param_list


    def default(self, line):
        """
        override default method that catches all command
        :param line: command passed in
        """

        # get the command and its parameters
        command_input = line.split()[0]
        args = line.split()[1:]


        # check user enter quit command
        if command_input == ":quit" or command_input == ":q":
            return self.do_exit()

        if command_input == ":set" or command_input == ":s":
            return self.do_set(args)

        # check user enter help command
        if command_input == ":help" or command_input == ":h":
            return self.do_myhelp()

        # check user enter history command
        if command_input == ":shell_history" or command_input == ":sh":
            return self.do_history(args)

        command = self.ctx.command.commands.get(command_input)

        if command:

            create_shell = False
            arg_type = ""
            args_stmt = ""
            com_args = []
            ctx_used = None
            is_group = False
            group = ""
            bool_type = False

            if isinstance(command, click.Group):
                create_shell = True
                is_group = True
                group = command_input
                ctx_used = click.Context(command)
                self.set_and_pass_context_obj(ctx_used)

                # check if plugin developed based on click has shell support
                if command.__dict__["invoke_without_command"] and ctx_used.__dict__["invoked_subcommand"] is None:
                    create_shell = False
            else:
                ctx_used = self.ctx
                is_group = False
                group = self.group #self.prompt
                create_shell = False


            if command.__dict__["name"] not in self.shell_available_commands:
                print("Error: No such command \"" + command.name + "\"")
                return

            if args:
                arg_type = "passed"
                com_args = args
                args_stmt = " = ".join(args)
            else:
                # get saved or default parameters if user has not passed any args and provide as hint
                #arg_type, arg_values, saved_args = self.get_saved_parameters(group_name=command_input, is_group=True, command=command)
                arg_type, arg_values, com_args, bool_type = self.get_saved_parameters(group_name=group,
                                                                             is_group=is_group, command=command)
                args_stmt = ", ".join(arg_values)

            if arg_type is "Error":
                print(arg_type + ": required parameters " + args_stmt + " need to be set")
            elif com_args:
                try:
                    print("used " + arg_type + " parameters { " + args_stmt + " }")

                    # parse the parameters in context of command, invoke the command, and update saved values
                    self.parse_parameters_and_update_dictionary(ctx_used, com_args, command, bool_type)

                except Exception as e:
                    #print("Error. Could not use " + arg_type + " parameters.")
                    create_shell = False
            else :
                # invoke the command directly if no args
                ctx_used.invoke(command)

            # check if can create nested shell
            if create_shell:
                self.update_transfer_parameters_shells(enter_value=True, exit_value=False, new_prompt=group, new_context=ctx_used)
                new_repl = Shell(ctx_used, root_shell = False)
                new_repl.group = new_repl.prompt
                new_repl.prompt = self.prompt + " : " + new_repl.prompt
                new_repl.cmdloop()

        else:
            return cmd.Cmd.default(self, line)
