import click
import cmd
import json
import pickle
import sys


class MainShell(cmd.Cmd):

    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx
        self.available_commands = []
        self.prompt = ctx.command.name + " > "
        self.parameters = {}


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
                self.parameters = pickle.load(f)
        except Exception as e:
            self.parameters = {}

    def save_parameters_file(self):
        ''' Save the parameters dict in hidden file '''

        file = ".parameters_history"

        with open(file, "wb") as f:
            pickle.dump(self.parameters, f)

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
        if self.available_commands:
            self.available_commands = []

        for key in self.ctx.command.commands:
            command = self.ctx.command.commands.get(key)
            level = command.__dict__['hidden']
            if not level:
                self.available_commands.append(key)

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
                    opt = param_opts[0]
                    # value = ""

                    # get the type of parameter and its value
                    if param_name in self.parameters:
                        value = self.parameters[param_name][-1]
                        param_type = "saved"
                    elif param_default is not None:
                        value = param_default
                        param_type = "default"
                    else:
                        sys.exit("Required parameter " + param_name + " needs to be set.")

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

                else:
                    sys.exit("Required parameter " + param_name + " needs to be set.")

        return param_type, param_value, saved_args_list

    def set_context_obj(self, context):
        ''' Set context object to save parameter value'''

        if context.obj is None:
            context.obj = {}
        context_parameters = context.__dict__["params"]
        for param, value in context_parameters.items():
            context.obj[param] = value

        if "logger" in context.__dict__["command"].__dict__:
            context.obj["logger"] = context.__dict__["command"].__dict__["logger"]

    def update_parameter_dict(self, command, context):
        ''' Update the parameter dictionary object with new values '''

        context_parameters = context.__dict__["params"]

        # Get the latest param values from context and update dictionary
        if command.params:
            for param in command.params:

                param_name = param.__dict__["name"]
                param_type = param.__dict__["type"]

                if param_name in context_parameters and not isinstance(param_type, click.types.BoolParamType):
                    if param_name not in self.parameters:
                        self.parameters[param_name] = [context_parameters[param_name], ]
                    else:
                        self.parameters[param_name].append(context_parameters[param_name])

        # Save the parameters to file to always get the latest value
        self.save_parameters_file()

        # Reset the parameters in context for each loop to avoid unexpected key error
        context.__dict__["params"] = {}

    def pass_context(self, parent_shell_ctx, child_shell):
        """
        Pass context obj information from parent to child
        :param parent_shell_ctx: parent shell is current shell
        :param child_shell: child shell is nested shell for click group found
        :return:
        """

        # transfer param and value in parent ctx obj to child ctx obj
        for param, value in parent_shell_ctx.obj.items():
            child_shell.ctx.obj[param] = value

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
        self.update_parameter_dict(command, ctx)

    def do_exit(self):
        ''' Exit the shell '''
        print("Exiting")
        return True

    def do_show(self):
        ''' show all the commands '''
        print("Available commands for use")
        for command in self.available_commands:
            print(command)

    def do_history(self):
        print("History of parameters")
        for param, value in self.parameters.items():
            print("parameter: " + param)
            print("values: " + str(value))

    def precmd(self, line):
        ''' Overwrite precmd command to load saved parameters and history
        :param line: command run in shell
        :return: command run in shell
        '''

        # log the commands information
        self.log_shell_history(line)

        # each time load saved parameters in case value changes
        self.load_parameters_file()

        return line

    def default(self, line):
        """
        override default method that catches all command
        :param line: command passed in
        """

        # get the command and its parameters
        subcommand = line.split()[0]
        args = line.split()[1:]

        # check user enter quit command
        if subcommand == ":q":
            return self.do_exit()

        # check user enter help command
        if subcommand == "--help":
            return self.do_show()

        # check user enter history command
        if subcommand == "--history":
            return self.do_history()

        subcommand = self.ctx.command.commands.get(subcommand)

        if subcommand:

            # Check if command is a click.Group create a nested shell with cmd to run
            if isinstance(subcommand, click.Group):

                new_ctx = click.Context(subcommand)

                if args:
                    # parse the parameters in context of command, invoke the command, and update saved values
                    self.parse_parameters_and_update_dictionary(new_ctx, args, subcommand)
                else:
                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(subcommand)

                    if arg_values:
                        saved_args_stmt = ", ".join(arg_values)
                        print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(new_ctx, saved_args, subcommand)

                new_repl = Shell(new_ctx)

                self.pass_context(self.ctx, new_repl)
                new_repl.cmdloop()

            else:

                if args:
                    # parse the parameters in context of command, invoke the command, and update saved values
                    self.parse_parameters_and_update_dictionary(self.ctx, args, subcommand)
                else:
                    # get saved or default parameters if user has not passed any args and provide as hint
                    arg_type, arg_values, saved_args = self.get_saved_parameters(subcommand)

                    if arg_values:
                        saved_args_stmt = ", ".join(arg_values)
                        print("used " + arg_type + " parameters { " + saved_args_stmt + " }")

                        # parse the parameters in context of command, invoke the command, and update saved values
                        self.parse_parameters_and_update_dictionary(self.ctx, saved_args, subcommand)

                    else:
                        # invoke the command directly if no args
                        self.ctx.invoke(subcommand)

        else:
            return cmd.Cmd.default(self, line)
