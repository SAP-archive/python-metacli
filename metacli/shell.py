import click
import cmd
import json
import pickle
import sys
import os


class MainShell(cmd.Cmd):

    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx
        self.prompt = ctx.command.name + " > "
        self.debug_parameters_history = {}
        self.shell_available_commands = []
        self.shell_parameters_options = {}

        ##########
        self.shell_parameters_level = {}
        self.shell_parameters_history = {}
        self.permission = "developer"
        self.time = ""


class Shell(MainShell):

    def __init__(self, ctx):
        MainShell.__init__(self, ctx)
        self.intro = ":q to quit; --help to list all commands "
        self.get_available_commands()
        self.set_context_obj(ctx)

    def load_parameters_file(self):
        ''' load dictionary of saved parameters from file '''

        file = ".parameters_history"

        try:
            with open(file, "rb") as f:
                self.debug_parameters_history = pickle.load(f)
        except Exception as e:
            self.debug_parameters_history = {}

    def save_parameters_file(self):
        ''' Save the parameters dict in hidden file '''

        file = ".parameters_history"

        with open(file, "wb") as f:
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

        print("get available commands")
        print("permsision, ", self.permission)

        # clear the list of available commands each time shell called
        if self.shell_available_commands:
            self.shell_available_commands = []

        for key in self.ctx.command.commands:
            command = self.ctx.command.commands.get(key)
            print("command, ", command.__dict__)
            func_level = "developer"

            if command.__dict__["permission"]:
                func_level = command.__dict__["permission"]

            print("func level, ", func_level)

            if func_level == "admin" and self.permission == "developer":
                command.__dict__["hidden"] = True
            else:
                command.__dict__["hidden"] = False
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



    def update_parameter_values_dict(self, command, context):
        ''' Update the parameter dictionary object with new values '''

        context_parameters = context.__dict__["params"]

        # Get the latest param values from context and update dictionary
        if command.params:
            for param in command.params:

                param_name = param.__dict__["name"]
                param_type = param.__dict__["type"]

                if param_name in context_parameters and not isinstance(param_type, click.types.BoolParamType):
                    if param_name not in self.debug_parameters_history:
                        self.debug_parameters_history[param_name] = [context_parameters[param_name], ]
                    else:
                        self.debug_parameters_history[param_name].append(context_parameters[param_name])

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
        :param child_shell: child shell is nested shell for click group found
        :return:
        """

        # transfer param and value in parent ctx obj to child ctx obj
        for param, value in parent_shell_ctx.obj.items():
            child_shell_ctx.obj[param] = value


    def pass_parameter_values(self, parent_shell_dict, child_shell_dict):

        # transfer values from parent shell to child shell
        for opt, value in parent_shell_dict.items():
            child_shell_dict[opt] = value

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
            print("cannot set the parameter")
        elif len(arg_list) > 2:
            print("can only set parameter at a time")
        else:
            parameter = arg_list[0]
            value = arg_list[1]
            print("set parameter " + parameter + " = " + value)

            print("ctx obj, ", self.ctx.obj)
            print("shell param level, ", self.shell_parameters_level)

            self.ctx.obj[parameter] = value
            self.update_parameter_options_dict(self.ctx)

            # if parameter in self.shell_parameters_level:
            #     self.shell_parameters_level[parameter].append(value)

            self.debug_parameters_history[parameter].append(value)

            # Save the parameters to file to always get the latest value
            self.save_parameters_file()

    def do_mylogin(self, command):
        print("login")
        self.ctx.invoke(command)

        if os.path.exists(".temp.txt"):
            with open(".temp.txt", "r") as f:
                userlevel, timestamp = f.readline().rstrip().split("$")
                self.permission = userlevel
                self.time = timestamp

        self.get_available_commands()

    def do_mylogout(self, command):
        print("logout")
        self.ctx.invoke(command)
        self.permission = "developer"
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

        self.get_available_commands()

        #self.update_parm()

        return line

    def default(self, line):
        """
        override default method that catches all command
        :param line: command passed in
        """

        print("default")
        print("time, ", self.time)
        # get the command and its parameters
        subcommand = line.split()[0]
        args = line.split()[1:]

        # check user enter quit command
        if subcommand == ":q":
            return self.do_exit()

        if subcommand == "--set":
            return self.do_set(args)
        # check user enter help command
        if subcommand == "--help":
            return self.do_show()

        # check user enter history command
        if subcommand == "--history":
            return self.do_history()


        subcommand = self.ctx.command.commands.get(subcommand)

        if subcommand.__dict__["name"] == "login":
            return self.do_mylogin(subcommand)

        if subcommand.__dict__["name"] == "logout":
            return self.do_mylogout(subcommand)

        if subcommand:

            # Check if command is a click.Group create a nested shell with cmd to run
            if isinstance(subcommand, click.Group):
                # boolean determine can run nested shell
                create_shell = True

                new_ctx = click.Context(subcommand)
                self.set_context_obj(new_ctx)

                self.pass_context_obj(self.ctx, new_ctx)

                if args:
                    print("Subcommand Group args")
                    try:
                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(new_ctx, args, subcommand)

                        # check if plugin developed based on click has shell support
                        if subcommand.__dict__["invoke_without_command"] and self.ctx.__dict__["invoked_subcommand"] is None:
                            create_shell = False

                    except Exception as e:
                        print("Error. Could not use passed parameters: " + str(e))

                else:
                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(subcommand)

                    if arg_type is "Error":
                        print(arg_type + ": required parameter " + arg_values + " need to be set")
                        create_shell = False
                    elif arg_values:
                        print("Subcommand Group saved / default args")
                        try:
                            saved_args_stmt = ", ".join(arg_values)
                            print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                            # parse the parameters in context of command, invoke the command, and update saved values
                            self.parse_parameters_and_update_dictionary(new_ctx, saved_args, subcommand)

                            # check if plugin developed based on click has shell support
                            if subcommand.__dict__["invoke_without_command"] and self.ctx.__dict__["invoked_subcommand"] is None:
                                create_shell = False

                        except Exception as e:
                            print("Error. Could not use " + arg_type + " parameters : " + str(e))

                # check if can create nested shell
                if create_shell:
                    # new_repl = Shell(new_ctx)
                    # new_repl.cmdloop()

                    ##################################
                    print("creat shell")
                    new_repl = Shell(new_ctx)
                    new_repl.permission = self.permission
                    #self.pass_parameter_values(self.shell_parameters_options, new_repl.shell_parameters_options)
                    print("param hist, ", self.shell_parameters_history)
                    print("param level, ", self.shell_parameters_level)
                    #self.pass_parameter_values(self.shell_parameters_level, new_repl.shell_parameters_level)
                    #self.pass_parameter_values(self.shell_parameters_level, new_repl.shell_parameters_history)
                    new_repl.cmdloop()

            else:

                if args:
                    print("Subcommand args")
                    try:
                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(self.ctx, args, subcommand)

                    except Exception as e:
                        print("Error. Could not use passed parameters: " + str(e))

                else:
                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(subcommand)

                    if arg_type is "Error":
                        print(arg_type + ": required parameters " + arg_values + " need to be set")
                    elif arg_values:
                        print("Subcommand saved / default args")
                        try:
                            saved_args_stmt = ", ".join(arg_values)
                            print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                            # parse the parameters in context of command, invoke the command, and update saved values
                            self.parse_parameters_and_update_dictionary(self.ctx, saved_args, subcommand)

                        except Exception as e:
                            print("Error. Could not use " + arg_type + " parameters : " + str(e))

                    else:
                        print("Subcommand no args")
                        # invoke the command directly if no args
                        self.ctx.invoke(subcommand)

        else:
            return cmd.Cmd.default(self, line)
