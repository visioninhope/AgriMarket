#!/usr/bin/env python3

"""
AgriMarket Console
"""

from models.user import User # Import User class
from models.product import Product
from models.equipment import Equipment
from models.transaction import Transaction
from models import storage
import cmd
import sys

class AMCommand(cmd.Cmd):
    """ Class AMCommand to implement the command interpreter. """
    prompt = '(agrimarket) '
    __all_117 = 0

    def emptyline(self):
        """ Do nothing on empty input. """
        pass

    def precmd(self, line):
        """ Edit given command to allow a second type of input. """
        if not sys.stdin.isatty():
            print()
        if '.' in line:
            AMCommand.__all_117 = 1
            line = line.replace('.', ' ').replace('(', ' ').replace(')', ' ')
            cmd_argv = line.split()
            cmd_argv[0], cmd_argv[1] = cmd_argv[1], cmd_argv[1]
            line = " ".join(cmd_argv)
        return cmd.Cmd.precmd(self, line)

    def do_quit(self, arg):
        """ Quit command to exit the program. """
        return True

    def do_EOF(self, arg):
        """ EOF command to exit the program. """
        print()
        return True

    def do_create(self, arg):
        """ Create an instance if the Model exists. """
        if not arg:
            print("** class name missing **")
            return None

        try:
            my_model = eval(arg + "()")
            my_model.save()
            print(my_model.id)
        except:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """ Print the string representation of an instance based on ID. """
        cmd_argv = arg.split()

        if not cmd_argv:
            print("** class name missing **")
            return None

        try:
            eval(cmd_argv[0])
        except:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all()

        if len(cmd_argv) < 2:
            print("** instance id missing **")
            return None

        cmd_argv[1] = cmd_argv[1].replace("\"", "")
        key = cmd_argv[0] + '.' + cmd_argv[1]

        if all_objs.get(key, False):
            print(all_objs[key])
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """ Print all instances or all instances of a specific class. """
        cmd_argv = arg.split()

        if not cmd_argv:
            print("** class name missing **")
            return None

        try:
            eval(cmd_argv[0])
        except:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all()
        print_list = []
        len_objs = len(all_objs)

        if len(cmd_argv) > 1:
            class_name = cmd_argv[0]
            print_list = [str(value) for key, value in all_objs.items() if key.startswith(class_name + ".")]
        else:
            print_list = [str(value) for value in all_objs.values()]


        print("[", end="")
        print(", ".join(print_list), end="")
        print("]")

    def do_destroy(self, arg):
        """
        Deletes an instance based on its ID and saves the changes
        Usage: destroy <class name> <id>
        """
        cmd_argv = arg.split()

        if not cmd_argv:
            print("** class name missing **")
            return None

        try:
            eval(cmd_argv[0])
        except:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all()

        if len(cmd_argv) < 2:
            print("** instance id missing **")
            return None
        
        cmd_argv[1] = cmd_argv[1].replace("\"", "")
        key = cmd_argv[0] + '.' + cmd_argv[1]

        if key in all_objs:
            all_objs.pop(key)
            storage.save()
        else:
            print("** no instance found **")


    def do_update(self, arg):
        """ Usage: update <class name> <id> <attribute name> <attribute value> """
        cmd_argv = []
        part2_argv = []
        is_dict = 0
        if "\"" in arg:
            if "," in arg:
                if "{" in arg:
                    is_dict = 1
                    part1_argv = arg.split(",")[0].split()
                    for i in part1_argv:
                        cmd_argv.append(i.replace("\"", ""))
                    part2_argv = arg.replace("}", "").split("{")[1].split(", ")
                    for i in part2_argv:
                        for j in i.split(": "):
                            cmd_argv.append(j.replace("\"", "")
                                            .replace('\'', ""))
                else:
                    arg_key = arg.replace(",", "")
                    part1_argv = arg_key.split()
                    for i in part1_argv[:2]:
                        cmd_argv.append(i.replace("\"", ""))
                    part2_argv = arg.split(", ")[1:]
                    for i in part2_argv:
                        cmd_argv.append(i.replace("\"", ""))
            else:
                part1_argv = arg.split("\"")[0]
                for i in part1_argv.split():
                    cmd_argv.append(i)
                part2_argv = arg.split("\"")[1:]
                for i in part2_argv:
                    if i != " " and i != "":
                        cmd_argv.append(i.replace("\"", ""))
        else:
            part1_argv = arg.split()
            for i in range(len(part1_argv)):
                if i == 4:
                    break
                cmd_argv.append(part1_argv[i])

        if (len(cmd_argv) == 0):
            print("** class name missing **")
            return None

        try:
            eval(cmd_argv[0])
        except:
            print("** class doesn't exist **")
            return None

        if len(cmd_argv) < 2:
            print("** instance id missing **")
            return None

        all_objs = storage.all()

        key = cmd_argv[0] + '.' + cmd_argv[1]
        if all_objs.get(key, False):
            if len(cmd_argv) >= 3:
                if (len(cmd_argv) % 2) == 0:
                    for i in range(2, len(cmd_argv), 2):
                        attr = cmd_argv[i]
                        type_att = getattr(all_objs[key], cmd_argv[i], "")
                        try:
                            cast_val = type(type_att)(cmd_argv[i + 1])
                        except:
                            cast_val = type_att
                        setattr(all_objs[key], cmd_argv[i], cast_val)
                        all_objs[key].save()
                        if is_dict == 0:
                            break

                else:
                    print("** value missing **")
            else:
                print("** attribute name missing **")
        else:
            print("** no instance found **")


    def do_count(self, arg):
        """ Usage: count <class name> or <class name>.count() """
        """ Retrieve the number of instances of a class """
        cmd_argv = arg.split()

        if not cmd_argv:
            print("** class name missing **")
            return


        try:
            eval(cmd_argv[0])
        except:
            print("** class doesn't exist **")
            return

        all_objs = storage.all()
        count = 0

        if len(mcd_argv) > 1:
            class_name = cmd_argv[0]
            count = sum(1 for key in all_objs if key.startswith(class_name + "."))
        else:
            print("** class name missing **")
            return
        print(count)


if __name__ == '__main__':
    AMCommand().cmdloop()
