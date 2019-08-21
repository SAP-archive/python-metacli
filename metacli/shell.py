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

    def load_parameters_file(self):
        ''' load dictionary of saved parameters from file '''

        file = ".parameters_history"

        try:
            with open(file, "rb") as f:
                print("open file in load parameter file")
                self.parameters = pickle.load(f)

        except Exception as e:
            self.parameters = {}

        print("param dict, ", self.parameters)

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

            with open(file, "a") as f:
                json.dump(shell_stmt, f)
                f.write("\n")
                json.dump(line, f)
                f.write("\n\n")

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

    def update_parameter_dict(self, command, context):
        ''' Update the parameter dictionary object with new values '''

        context_parameters = context.__dict__["params"]

        if command.params:
            for param in command.params:

                param_name = param.__dict__["name"]
                param_type = param.__dict__["type"]

                if param_name in context_parameters and not isinstance(param_type, click.types.BoolParamType):
                    if param_name not in self.parameters:
                        self.parameters[param_name] = [context_parameters[param_name], ]
                    else:
                        self.parameters[param_name].append(context_parameters[param_name])

        print("param dict, ", self.parameters)

        # save the parameters to always get the latest value
        self.save_parameters_file()

        # resetting the parameters for each loop to avoid unexpected key error

        context.__dict__["params"] = {}

    def save_parameters_file(self):
        ''' Save the parameters dict in hidden file '''

        file = ".parameters_history"

        with open(file, "wb") as f:
            print("open file in save parameters file")
            pickle.dump(self.parameters, f)

    def do_exit(self):
        ''' Exit the shell '''
        print("Exiting")
        return True

    def do_list(self):
        ''' list all the commands '''
        print("Available commands for use")
        for command in self.available_commands:
            print(command)

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

        saved_args_list = None

        # new_args_list hold the list of parameters return and used when run command
        new_args_list = []

        # Get the saved parameters from dictionary
        if command.params:
            for param in command.params:
                param_name = param.__dict__["name"]
                if param_name in self.parameters:
                    saved_args_list = self.parameters[param_name]
                else:
                    sys.exit("Required parameter" + param_name + " to be set.")



        # Used the saved parameters value if found
        # Else used the current parameters passed now
        # TODO determine when should return saved or current parameters
        # TODO how user specify want to use saved parameters
        if saved_args_list is not None:
            if isinstance(saved_args_list, tuple):
                for arg in saved_args_list:
                    new_args_list.append(arg)
            else:
                new_args_list.append(saved_args_list)

            print("found saved parameters")
            print("saved: ", new_args_list)

        return new_args_list


    def set_context_obj(self, context):
        ''' Set context object to save parameter value'''

        context.obj = {}
        context_parameters = context.__dict__["params"]
        for param, value in context_parameters.items():
            context.obj[param] = value



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
            return self.do_list()

        subcommand = self.ctx.command.commands.get(subcommand)

        if subcommand:

            # Check if command is a click.Group create a nested shell with cmd to run
            if isinstance(subcommand, click.Group):

                new_ctx = click.Context(subcommand)

                # TODO: determine whether to use the saved parameters or not
                # if not args:
                #     # get saved parameters if user not passed any
                #     args = self.get_saved_parameters(subcommand)

                if args:

                    # TODO: determine whether to use the saved parameters or not
                    # automatically use whatever parameters currently passed, not saved
                    #args = self.get_saved_parameters(subcommand, args)



                    # parse parameters passed in
                    subcommand.parse_args(new_ctx, args)

                    self.set_context_obj(new_ctx)
                    # automatically adds new parameter value to dictionary
                    self.update_parameter_dict(subcommand, new_ctx)

                new_repl = Shell(new_ctx)
                new_repl.cmdloop()

            else:

                if args:

                    ## TODO: determine whether to use the saved parameters or not
                    # automatically use whatever parameters currently passed, not saved
                    #args = self.get_saved_parameters(subcommand, args)

                    # parse parameters passed in and then invoke the command
                    subcommand.parse_args(self.ctx, args)
                    self.ctx.forward(subcommand)

                    # automatically adds new parameter value to dictionary
                    self.update_parameter_dict(subcommand, self.ctx)

                else:

                    # invoke the command
                    self.ctx.invoke(subcommand)

        else:
            return cmd.Cmd.default(self, line)
