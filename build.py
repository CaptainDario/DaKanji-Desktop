#######################################################
#
# This script assumes that a virtual environment with
# all necessary packages AND pyinstaller is in a 
# folder .venv_rel\Scripts\pyinstaller.exe
#
#######################################################
import sys
sys.path.insert(0, "./src")
import about

import os
import shutil
import subprocess



def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)


if __name__ == "__main__":
    
    build_command_folder = ""
    build_command_file = ""

    name_folder = str(about.full_id) + "_folder"
    name_file   = str(about.full_id) + "_file"

    activate_venv_cmd = ""

    #build for WINDOWS
    if(os.name == "nt"):
        activate_venv_cmd = os.path.join(".venv_rel", "Scripts", "activate.bat")

        data =  "--add-data .\\ui;ui "
        data += "--add-data .\\data;data "
        data += "--add-data .\\icons;icons "

        path = "--distpath=.\\build\\windows"

        icon = "--icon=.\\icons\\icon.ico"

        additional = "--noconfirm --noconsole"

        build_command_folder = " ".join(["pyinstaller", data, path, "--name=" + name_folder, "--clean", icon, additional, ".\src\main.py"])
        build_command_file   = " ".join(["pyinstaller", data, path, "--name=" + name_file, "--clean", "--onefile", icon, additional, ".\src\main.py"])
    else:
        print("OS on which you are trying to build is not configured.")
        print("Please add a build configuration and submit a pull request: " + about.pull_url)
    
    
    # --- build folder-exe
    print(build_command_folder)
    subprocess.call(activate_venv_cmd + " &&" + build_command_folder)
    #remove spec
    os.remove(name_folder + ".spec")
    #remove temp folder
    shutil.rmtree(os.path.join("build", name_folder))


    # --- build onefile-exe
    print(build_command_file)
    subprocess.call(activate_venv_cmd + " &&" + build_command_file)
    #remove spec
    os.remove(name_file + ".spec")
    #remove temp folder
    shutil.rmtree(os.path.join("build", name_file))