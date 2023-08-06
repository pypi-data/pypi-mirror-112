import sys, getopt, os, shutil, json


def main():
    argv = sys.argv[1:]
    name = ''
    display_name = ''
    try:
        opts, args = getopt.getopt(argv, "n:d:", ["name=", "display_name="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg
        elif opt in ("-d", "--display_name"):
            display_name = arg
    if not name:
        name = input("Enter Name: ")
    if not display_name:
        display_name = input("Enter display name: ")
    if os.path.isdir(name):
        print("Action already exists with this name")
        sys.exit()
    shutil.copytree("../../example_integration", "../../"+name)
    new_action_file_name = name + '_action.py'
    new_action_name = name.title() + 'Action'
    new_test_action_file_name = 'test_'+name + '_action.py'
    for dirpath, dirs, files in os.walk("../../"+name):
        for file in files:
            if file == 'example_action.py':
                new_file = os.path.join(dirpath, new_action_file_name)
                os.rename(os.path.join(dirpath, file), new_file)
                with open(new_file, 'r') as f:
                    file_data = f.read()
                    f.close()
                file_data = file_data.replace('ExampleAction', name.title()+'Action')
                with open(new_file, 'w') as f:
                    f.write(file_data)
                    f.close()
            if file == 'test_example_action.py':
                new_test_file = os.path.join(dirpath, new_test_action_file_name)
                os.rename(os.path.join(dirpath, file), new_test_file)
                with open(new_test_file, 'r') as f:
                    file_data = f.read()
                    f.close()
                file_data = file_data.replace('example_action', name + '_action')
                file_data = file_data.replace('ExampleAction', new_action_name)
                with open(new_test_file, 'w') as f:
                    f.write(file_data)
                    f.close()
            if file == 'integration.json':
                json_file = os.path.join(dirpath, 'integration.json')
                with open(json_file, 'r') as f:
                    json_object = json.load(f)
                    f.close()
                    json_object["name"] = name
                    json_object["display_name"] = display_name
                    json_object["actions"][0]["name"] = name + '.' + name + '_action'
                    json_object["actions"][0]["module"] = name + '.src.' + name + '_action.' + new_action_name
                with open(json_file, 'w') as f:
                    json.dump(json_object, f)
                    f.close()


# if __name__ == "__main__":
#     create_integration(sys.argv[1:])
