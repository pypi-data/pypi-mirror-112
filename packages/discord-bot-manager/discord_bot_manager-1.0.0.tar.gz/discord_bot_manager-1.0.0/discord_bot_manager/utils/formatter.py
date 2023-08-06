def get_help_text_from_list(commands, activator=None, main_command_help_text=None):
    if not commands:
        return ""

    max_command_length = max(
        [*[len(str(command)) for command in commands], len('COMMANDS')]
    ) + len("[syntax]") + 2
    max_command_help_text_length = max(
        (max([len(command.get_help_text()), len(command.get_command_syntax())]) for command in commands)
    )

    out = "`"
    if main_command_help_text:
        out += main_command_help_text + '\n'

    if activator:
        help_text = f"Commands For '{activator}'"
    else:
        help_text = "All Commands"

    out += (
            f"{help_text:^{max_command_length + max_command_help_text_length + 2}}\n" +
            " " * (max_command_help_text_length + max_command_length + 2) +
            "\n"
    )
    out += (
            f"{'commands':<{max_command_length}}| help" +
            " " * (max_command_help_text_length - 4) +
            "\n"
    )
    out += (
            "-" * (max_command_help_text_length + max_command_length + 2) +
            "\n"
    )

    for command in commands:
        out += (
                f"{str(command):<{max_command_length}}| {command.get_help_text()}" +
                " " * (max_command_help_text_length - len(command.get_help_text())) +
                "\n"
        )
        out += (
                f"{str(command) + '[syntax]':<{max_command_length}}| {command.get_command_syntax()}" +
                " " * (max_command_help_text_length - len(command.get_command_syntax())) +
                "\n"
        )
    out += " " * (max_command_help_text_length + max_command_length + 2) + "\n"
    out += "`"
    return out
