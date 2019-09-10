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
        self.permission = "developer"
        self.debug_parameters_history = {}
        self.shell_available_commands = []
        self.shell_parameters_options = {}

        self.shell_parameters_level = {}
        self.shell_parameters_history = {}
        self.transfer_parameters = {}


class Shell(MainShell):

    def __init__(self, ctx, initialize_param):
        MainShell.__init__(self, ctx)
        self.intro = ":q to quit; --help to list all commands "
        self.call_initialize_ctx_sys_argv = initialize_param
        self.get_available_commands()
        # self.initialize_ctx_sys_argv(ctx)
        self.set_context_obj(ctx)

    # TODO: Saving parameters of different levels
    def initialize_ctx_sys_argv(self, ctx):
        command = ctx.__dict__["command"]

        if self.call_initialize_ctx_sys_argv:

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

            self.update_parameter_values_dict(command, ctx) # use this?

    # TODO: Saving parameters of different levels
    def gather_param_for_base(self, list, param, count=False):
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
                length = pickle.load(f)
                if length > 1:
                    my_dicts = pickle.load(f)
                    self.debug_parameters_history, self.transfer_parameters = my_dicts
                else:
                    self.debug_parameters_history = pickle.load(f)

        except Exception as e:
            self.debug_parameters_history = {}

    def save_parameters_file(self):
        ''' Save the parameters dict in hidden file '''

        file = ".parameters_history"

        with open(file, "wb") as f:
            #pickle.dump(self.debug_parameters_history, f)
            if "Entering" in self.transfer_parameters or "Exiting" in self.transfer_parameters:
                my_dicts = [self.debug_parameters_history, self.transfer_parameters]
                pickle.dump(len(my_dicts), f)
                pickle.dump(my_dicts, f)
            else:
                pickle.dump(1, f)
                pickle.dump(self.debug_parameters_history, f)

    def log_shell_history(self, line):
        ''' log commands run in shell to file '''

        file = "shell_history"

        command_name = line.split()[0]
        args = line.split()[1:]

        subcommand = self.ctx.command.commands.get(command_name)

        if subcommand:
            shell_stmt = "shell: " + self.prompt
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
            shell_stmt = "shell: " + self.prompt
            cmd_stmt = "command: " + line

            with open(file, "a") as f:
                json.dump(shell_stmt, f)
                f.write("\n")
                json.dump(cmd_stmt, f)
                f.write("\n\n")

    def get_available_commands(self):
        ''' Get the commands user able to access based on permission'''

        # clear the list of available commands each time shell called
        if self.shell_available_commands:
            self.shell_available_commands = []

        for key in self.ctx.command.commands:
            command = self.ctx.command.commands.get(key)
            func_level = "developer"

            if "permission" in command.__dict__:
                func_level = command.__dict__["permission"]
            else:
                func_level = "developer"

            if func_level == "admin" and self.permission == "developer":
                pass
            else:
                self.shell_available_commands.append(key)

    def get_saved_parameters(self, command):
        '''
        Get saved parameters from dictionary and decide whether to use those values
        :param command: command just run in shell
        :return: list of parameters
        '''

        # saved_args_list hold the list of parameters return and used when run command
        saved_args_list = []

        # values used to indicate the type of param (saved, default) and its value
        param_type = ""
        param_value = []

        # Get the saved parameters from dictionary
        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                param_opts = param.__dict__["opts"]
                param_count = param.__dict__["count"]
                param_default = param.__dict__["default"]
                param_multiple = param.__dict__["multiple"]
                if param_opts:
                    opt = str(param_opts[0])

                    # get the type of parameter and its value
                    if param_name in self.debug_parameters_history:
                        value = self.debug_parameters_history[param_name][-1]
                        param_type = "saved"
                    elif param_default is not None or param_default is None:
                        value = param_default
                        param_type = "default"
                    else:
                        return "Error", opt, None

                    # format parameters for hint message
                    if isinstance(value, str) and not value:
                        param_value.append(opt + " = ''")
                    else:
                        param_value.append(opt + " = " + str(value))

                    # create args list for parsing command based on option type
                    if param_count:
                        for i in range(0, value):
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

        return param_type, param_value, saved_args_list

    def set_context_obj(self, context):
        ''' Set context object to save parameter value'''

        if context.obj is None:
            context.obj = {}

        if self.shell_parameters_options is None:
            self.shell_parameters_options = {}

        context_parameters = context.__dict__["params"]

        for param, value in context_parameters.items():
            context.obj[param] = value

        if "logger" in context.__dict__["command"].__dict__:
            context.obj["logger"] = context.__dict__["command"].__dict__["logger"]

        self.update_parameter_options_dict(context)

    def check_permission_status(self):
        if os.path.exists(".temp.txt"):
            with open(".temp.txt", "r") as f:
                userlevel, timestamp = f.readline().rstrip().split("$")
                if time.time() - float(timestamp) > 60:
                    warnings.simplefilter("always", Warning)
                    warnings.warn("Login Timeout", Warning)
                    os.remove(".temp.txt")
                    self.permission = "developer"

    # TODO: Saving parameters of different levels
    def update_transfer_parameters(self, enter_value = False, exit_value=False, new_prompt="", new_context=None):

        self.transfer_parameters["Entering"] = enter_value
        self.transfer_parameters["Exited"] = exit_value
        self.transfer_parameters["permission"] = self.permission

        pass_parameter_dict = {}

        if "parameters" in self.transfer_parameters:
            for param, value in self.transfer_parameters["parameters"].items():
                if param != self.prompt and param != new_prompt:
                    pass_parameter_dict[param] = value

        if enter_value:
                new_prompt_param_dict = {}
                if new_context is not None:
                    param_new_command = new_context.__dict__["command"].params
                    for param in param_new_command:
                        param_name = param.__dict__["name"]
                        if param_name in self.shell_parameters_level:

                            new_prompt_param_dict[param_name] = self.shell_parameters_level[param_name]
                            del self.shell_parameters_level[param_name]


                pass_parameter_dict[new_prompt + " > "] = new_prompt_param_dict
                pass_parameter_dict[self.prompt] = self.shell_parameters_level



        self.transfer_parameters["parameters"] = pass_parameter_dict

        self.save_parameters_file()

    def update_parameter_values_dict(self, command, context):
        ''' Update the parameter dictionary object with new values '''

        context_parameters = context.__dict__["params"]
        #print("context param, ", context_parameters)

        # Get the latest param values from context and update dictionary
        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                param_type = param.__dict__["type"]
                if param_name in context_parameters and not isinstance(param_type, click.types.BoolParamType):
                    if param_name not in self.debug_parameters_history: #self.shell_parameters_level :
                        self.debug_parameters_history[param_name] = [context_parameters[param_name], ]
                        #self.shell_parameters_level[param_name] = [context_parameters[param_name], ]
                    else:
                        self.debug_parameters_history[param_name].append(context_parameters[param_name])
                        #self.shell_parameters_level[param_name].append(context_parameters[param_name])

        # Save the parameters to file to always get the latest value
        self.save_parameters_file()

        # Reset the parameters in context for each loop to avoid unexpected key error
        context.__dict__["params"] = {}

    def update_parameter_options_dict(self, context):
        """
        Display saved parameters of the group
        :param context:
        :return:
        """
        ctx_obj = context.obj

        ctx_param = context.__dict__["command"].params

        for param in ctx_param:
            param_name = param.__dict__["name"]
            if param_name in ctx_obj:
                if param_name not in self.shell_parameters_options:
                    self.shell_parameters_options[param_name] = [ctx_obj[param_name], ]
                else:
                    self.shell_parameters_options[param_name].append(ctx_obj[param_name])

    def pass_context_obj(self, parent_shell_ctx, child_shell_ctx):
        """
        Pass context obj information from parent to child
        :param parent_shell_ctx: parent shell is current shell
        :param child_shell_ctx: child shell is nested shell for click group found
        :return:
        """

        # transfer param and value in parent ctx obj to child ctx obj
        for param, value in parent_shell_ctx.obj.items():
            child_shell_ctx.obj[param] = value


    def parse_parameters_and_update_dictionary(self, ctx, args, command):
        """
        Parse parameters of command in context and update param dictionary with new param values
        :param ctx: context of the command
        :param args: parameters passed in to command
        :param command: command run in the shell
        """

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
        self.update_transfer_parameters(enter_value= False, exit_value=True)
        return True

    def do_show(self):
        ''' show all the commands and parameters '''
        print("Available commands for use: ")
        if not self.shell_available_commands:
            print("None")
        else:
            for command in self.shell_available_commands:
                print(command)

        print("\nSaved Parameters: ")
        if not self.shell_parameters_options:
            print("None")
        else:
            for param, value in self.shell_parameters_options.items():
                print("parameter: " + param)
                print("value: " + str(value[-1]))

    def do_history(self):
        print("History of parameters")
        for param, value in self.debug_parameters_history.items():
            print("parameter: " + param)
            print("values: " + str(value))


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
            print("Set parameter " + parameter + " = " + value)

            self.ctx.obj[parameter] = value
            self.update_parameter_options_dict(self.ctx)

            self.debug_parameters_history[parameter].append(value)
            self.shell_parameters_level[parameter].append(value)

            # Save the parameters to file to always get the latest value
            self.save_parameters_file()

    def do_mylogin(self, command):
        self.ctx.invoke(command)

        if os.path.exists(".temp.txt"):
            with open(".temp.txt", "r") as f:
                userlevel, timestamp = f.readline().rstrip().split("$")
                self.permission = userlevel

        self.get_available_commands()
        self.update_transfer_parameters(enter_value=True, exit_value=False)

    def do_mylogout(self, command):
        self.ctx.invoke(command)
        self.permission = "developer"
        self.update_transfer_parameters(enter_value=True, exit_value=False)
        self.get_available_commands()

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

    # TODO: Saving parameters of different levels
    def setup_parameters(self):

        if "Entering" in self.transfer_parameters and self.transfer_parameters["Entering"]:
            if "parameters" in self.transfer_parameters:
                for param, param_list in self.transfer_parameters["parameters"].items():
                    if param == self.prompt:
                        for opts, opt_val in param_list.items():
                            for val in opt_val:
                                if opts not in self.shell_parameters_level:
                                    self.shell_parameters_level[opts] = [val, ]
                                else:
                                    self.shell_parameters_level[opts].append(val)
                    else:
                        for opts, opt_val in param_list.items():
                            for val in opt_val:
                                if opts not in self.shell_parameters_history:
                                    self.shell_parameters_history[opts] = [val, ]
                                else:
                                    self.shell_parameters_history[opts].append(val)


        if "Exited" in self.transfer_parameters and self.transfer_parameters["Exited"]:
            self.permission = self.transfer_parameters["permission"]

    def default(self, line):
        """
        override default method that catches all command
        :param line: command passed in
        """

        # get the command and its parameters
        command_input = line.split()[0]
        args = line.split()[1:]

        # check login status
        self.check_permission_status()

        # check user enter quit command
        if command_input == ":q":
            return self.do_exit()

        if command_input == "--set":
            return self.do_set(args)

        # check user enter help command
        if command_input == "--help":
            return self.do_show()

        # check user enter history command
        if command_input == "--history":
            return self.do_history()

        command = self.ctx.command.commands.get(command_input)

        if command:

            if command.__dict__["name"] == "login":
                return self.do_mylogin(command)

            if command.__dict__["name"] == "logout":
                return self.do_mylogout(command)

            if command.__dict__["name"] not in self.shell_available_commands:
                print("Error: No such command \"" + command.name + "\"")
                return

            # Check if command is a click.Group create a nested shell with cmd to run
            if isinstance(command, click.Group):
                # boolean determine can run nested shell
                create_shell = True
                initialize_args = True

                new_ctx = click.Context(command)
                self.set_context_obj(new_ctx)
                self.pass_context_obj(self.ctx, new_ctx)

                if args:

                    try:
                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(new_ctx, args, command)


                        # check if plugin developed based on click has shell support
                        if command.__dict__["invoke_without_command"] and self.ctx.__dict__["invoked_subcommand"] is None:
                            create_shell = False

                        initialize_args = False

                    except Exception as e:
                        print("Error. Could not use passed parameters: " + str(e))

                else:

                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(command)
                    if arg_type is "Error":
                        print(arg_type + ": required parameter " + arg_values + " need to be set")
                        create_shell = False

                    elif arg_values:
                        try:
                            saved_args_stmt = ", ".join(arg_values)
                            print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                            # parse the parameters in context of command, invoke the command, and update saved values
                            self.parse_parameters_and_update_dictionary(new_ctx, saved_args, command)

                            # check if plugin developed based on click has shell support
                            if command.__dict__["invoke_without_command"] and self.ctx.__dict__["invoked_subcommand"] is None:
                                create_shell = False

                            initialize_args = False

                        except Exception as e:
                            print("Error. Could not use " + arg_type + " parameters : " + str(e))

                # check if can create nested shell
                if create_shell:
                    new_repl = Shell(new_ctx, initialize_args)
                    new_repl.permission = self.permission
                    self.update_transfer_parameters(enter_value = True, exit_value=False, new_prompt=command_input, new_context=new_ctx)
                    new_repl.cmdloop()

            else:

                if args:
                    try:
                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(self.ctx, args, command)

                    except Exception as e:
                        print("Error. Could not use passed parameters: " + str(e))

                else:
                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(command)

                    if arg_type is "Error":
                        print(arg_type + ": required parameters " + arg_values + " need to be set")
                    elif arg_values:
                        try:
                            saved_args_stmt = ", ".join(arg_values)
                            print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                            # parse the parameters in context of command, invoke the command, and update saved values
                            self.parse_parameters_and_update_dictionary(self.ctx, saved_args, command)

                        except Exception as e:
                            print("Error. Could not use " + arg_type + " parameters : " + str(e))

                    else:
                        # invoke the command directly if no args
                        self.ctx.invoke(command)

        else:
            return cmd.Cmd.default(self, line)
