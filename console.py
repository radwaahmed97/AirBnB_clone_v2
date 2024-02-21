#!/usr/bin/python3
"""entry point to command line interpreter"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json
import shlex


class HBNBCommand(cmd.Cmd):
    """HBNB command line interpreter"""

    prompt = "(hbnb) "
    my_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """closes the program, saves safely data when ctrl+D is pressed"""
        print()
        return True

    def emptyline(self):
        """overrides the default emptyline function"""
        pass

    def do_nothing(self, arg):
        """does nothing :D"""
        pass

    def do_create(self, line):
        """Usage: create <class> """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")


    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        Structure: show [class name] [id]
        """
        datasplit = shlex.split(arg)
        if len(datasplit) == 0:
            print("** class name missing **")
            return
        if datasplit[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(datasplit) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        stored_dict = storage.all()
        key = datasplit[0] + "." + datasplit[1]
        if key in stored_dict:
            obj_instance = str(stored_dict[key])
            print(obj_instance)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (saves the changes into the JSON file)
        Structure: destroy [class name] [id]
        """
        datasplit = shlex.split(arg)
        if len(datasplit) == 0:
            print("** class name missing **")
            return
        if datasplit[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(datasplit) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        stored_dict = storage.all()
        key = datasplit[0] + "." + datasplit[1]
        if key in stored_dict:
            del stored_dict[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        Structure: all [class name] or all
        """

        storage.reload()
        tojsonlist = []
        stored_dict = storage.all()
        if not arg:
            for key in stored_dict:
                tojsonlist.append(str(stored_dict[key]))
            print(json.dumps(tojsonlist))
            return
        token = shlex.split(arg)
        if token[0] in HBNBCommand.my_dict.keys():
            for key in stored_dict:
                if token[0] in key:
                    tojsonlist.append(str(stored_dict[key]))
            print(json.dumps(tojsonlist))
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file).
        Structure: update [class name] [id] [arg_name] [arg_value]
        """
        if not arg:
            print("** class name missing **")
            return
        datasplit = shlex.split(arg)
        storage.reload()
        stored_dict = storage.all()
        if datasplit[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(datasplit) == 1:
            print("** instance id missing **")
            return
        try:
            key = datasplit[0] + "." + datasplit[1]
            stored_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        if len(datasplit) == 2:
            print("** attribute name missing **")
            return
        if len(datasplit) == 3:
            print("** value missing **")
            return
        my_instance = stored_dict[key]
        if hasattr(my_instance, datasplit[2]):
            data_type = type(getattr(my_instance, datasplit[2]))
            setattr(my_instance, datasplit[2], data_type(datasplit[3]))
        else:
            setattr(my_instance, datasplit[2], datasplit[3])
        storage.save()

    def do_update2(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file).
        Structure: update [class name] [id] [dictionary]
        """
        if not arg:
            print("** class name missing **")
            return
        my_dictionary = "{" + arg.split("{")[1]
        my_data = shlex.split(arg)
        storage.reload()
        objs_dict = storage.all()
        if my_data[0] not in HBNBCommand.my_dict.keys():
            print("** class doesn't exist **")
            return
        if len(my_data) == 1:
            print("** instance id missing **")
            return
        try:
            key = my_data[0] + "." + my_data[1]
            objs_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        if my_dictionary == "{":
            print("** attribute name missing **")
            return

        my_dictionary = my_dictionary.replace("'", '"')
        my_dictionary = json.loads(my_dictionary)
        my_instance = objs_dict[key]
        for my_key in my_dictionary:
            if hasattr(my_instance, my_key):
                data_type = type(getattr(my_instance, my_key))
                setattr(my_instance, my_key, my_dictionary[my_key])
            else:
                setattr(my_instance, my_key, my_dictionary[my_key])
        storage.save()

    def do_count(self, arg):
        """
        Counts number of instances of a class
        """
        counter = 0
        stored_dict = storage.all()
        for key in stored_dict:
            if arg in key:
                counter += 1
        print(counter)

    def default(self, arg):
        """handle new ways of inputing data"""
        val_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        arg = arg.strip()
        values = arg.split(".")
        if len(values) != 2:
            cmd.Cmd.default(self, arg)
            return
        class_name = values[0]
        command = values[1].split("(")[0]
        line = ""
        if command == "update" and values[1].split("(")[1][-2] == "}":
            inputs = values[1].split("(")[1].split(",", 1)
            inputs[0] = shlex.split(inputs[0])[0]
            line = "".join(inputs)[0:-1]
            line = class_name + " " + line
            self.do_update2(line.strip())
            return
        try:
            inputs = values[1].split("(")[1].split(",")
            for num in range(len(inputs)):
                if num != len(inputs) - 1:
                    line = line + " " + shlex.split(inputs[num])[0]
                else:
                    line = line + " " + shlex.split(inputs[num][0:-1])[0]
        except IndexError:
            inputs = ""
            line = ""
        line = class_name + line
        if command in val_dict.keys():
            val_dict[command](line.strip())


if __name__ == "__main__":
    HBNBCommand().cmdloop()
