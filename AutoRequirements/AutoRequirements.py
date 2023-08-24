import os
import subprocess
from importlib.metadata import packages_distributions
import sys
import ctypes

# Function to get a list of installed packages from pip
def get_installed_packages():
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, text=True)
    installed_packages = result.stdout.splitlines()
    return [package for package in installed_packages]

# Function to process a Python file and extract import statements
def process_python_file(file_path):
    with open(file_path, "rb") as file:
        content = file.read().decode("utf-8", errors="replace")
        lines = content.split("\n")
        
        import_lines = []
        
        for line in lines:
            if "from" in line or "import" in line:
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "from":
                    try: # for some reason this sometimes doesnt work
                        x = parts[1]
                    except: 
                        print("Error: ", line, x)
                    try:
                        x = x.split(".")[0]
                    except:
                        pass
                    if x:
                        import_lines.append(x)

                elif len(parts) >= 1 and parts[0] == "import":
                    try: # for some reason this sometimes doesnt work
                        x = parts[1]
                    except: 
                        print("Error: ", line, x)
                    try:
                        x = x.split(".")[0]
                    except:
                        pass
                    if x:
                        if "," in x:
                            x = x.split(",")
                            for item in x:
                                if item.strip():
                                    import_lines.append(item.strip())
                        else:
                            import_lines.append(x)

    return import_lines


def main():
    os.chdir(os.getcwd())
    if os.path.exists("requirements.txt"):
        os.remove("requirements.txt")
    
    directory = os.getcwd()
    print("This program expects you to have all packages installed, otherwise it may not work as expected.", end="\n\n")

    imports = []
    
    # loop through all files in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") or filename.endswith(".pyw"):
                file_path = os.path.join(root, filename)
                
                #find all imports and add them to the list.
                new_imports = process_python_file(file_path)
                for item in new_imports:
                    if item not in imports:
                        imports.append(item)

    
    distribution_info = packages_distributions()
    
    standard_packages = []
    full_import_list = []
    
    for item in sys.builtin_module_names:
        standard_packages.append(item)
    for item in sys.stdlib_module_names:
        standard_packages.append(item)

    files_list = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if "." in filename:
                filename = filename.rsplit('.', 1)
            files_list += filename
        files_list += dirs

    for item in imports:
        try:
            if not item in standard_packages:
                if item in files_list:
                    while not confirm.lower() in ["y", "n"]:
                        confirm = input(f'Import "{item}" is a file or folder being imported, but also a package. Do you want to import it as a package? (y/n)')
                        if confirm.lower() == "y":
                            full_import_list.append(distribution_info[item][0])
                        elif confirm.lower() == "n":
                            print(f'"{item}" will not be added into requirements.txt', end="\n\n")
                        else:
                            print(f'Your input "{confirm}" is not valid. Please enter "y" or "n')
                        
                else:
                    full_import_list.append(distribution_info[item][0])
        except:
            if item in files_list:
                print(f'"{item}" is a file or folder being imported. [probably, though there is a chance it could be a package]', end="\n\n") 
            else:
                handle = ctypes.windll.kernel32.GetStdHandle(-11)
                ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x0004)
                print(f'"{item}" is not installed [and not found as a python file], but is being imported. make sure you have all your packages installed.')
                ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x0007)
                print("", end="\n")
                
    print("All imports:", end="\n\n")
   
    for item in full_import_list:
        print(item)
    print()
    
    packages = get_installed_packages()
    
    requiremens = []
    
    for item in full_import_list:
        for package in packages:
            if item == package.split("==")[0]:
                requiremens.append(package)
    
    with open("requirements.txt", "w") as file:
        for item in requiremens:
            file.write(item + "\n")
            
            
    print("Saved to requirements.txt")
    print("Done! You can now close this window.")
    input("Press enter to exit.")


if __name__ == "__main__":
    main()
