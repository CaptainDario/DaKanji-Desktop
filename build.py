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
import platform
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

    pyinstaller = ""

    print("Building on", platform.system(), "...")
    #build for WINDOWS
    if(platform.system() == "Windows"):
        pyinstaller = os.path.join(".venv_rel", "Scripts", "pyinstaller.exe")

        data =  "--add-data .\\ui;ui "
        data += "--add-data .\\data;data "
        data += "--add-data .\\icons;icons "
        data += "--add-data .\\media\\banner.png;media "

        path = "--distpath=.\\build\\" + platform.system()

        icon = "--icon=.\\icons\\icon.ico"

        additional = "--noconfirm --noconsole"

        build_command_folder = " ".join([pyinstaller, data, path, "--name=" + name_folder, "--clean", icon, additional, r".\src\main.py"])
        build_command_file   = " ".join([pyinstaller, data, path, "--name=" + name_file, "--clean", "--onefile", icon, additional, r".\src\main.py"])
     
        # --- build folder-exe
        print(build_command_folder)
        subprocess.call(build_command_folder, shell=True)
        #remove spec
        if(os.path.exists(name_folder + ".spec")):
            os.remove(name_folder + ".spec")
        #remove temp folder
        if(os.path.exists(os.path.join("build", name_folder))):
            shutil.rmtree(os.path.join("build", name_folder))


        # --- build onefile-exe
        print(build_command_file)
        #subprocess.call(build_command_file)
        #remove spec
        if(os.path.exists(name_file + ".spec")):
            os.remove(name_file + ".spec")
        #remove temp folder
        if(os.path.exists(os.path.join("build", name_file))):
            shutil.rmtree(os.path.join("build", name_file))

    elif(platform.system() == "Linux"):
        activate_venv_cmd = ". " + os.path.join(".venv_rel", "bin", "pyinstaller")

        data =  "--add-data ./ui:ui "
        data += "--add-data ./data:data "
        data += "--add-data ./icons/banner.png:icons/banner.png "
        # bug in pyinstaller 4.1 -> can/shoule be removed with next stable release
        data += "--add-data ./.venv_rel/lib/python3.8/site-packages/PySide2/Qt/plugins:./PySide2/plugins"

        path = "--distpath=./build/" + platform.system()

        icon = "--icon=./icons/icon.ico"

        additional = "--noconfirm --noconsole"

        build_command_folder = " ".join([pyinstaller, data, path, "--name=" + name_folder, "--clean", icon, additional, "./src/main.py"])
        build_command_file   = " ".join([pyinstaller, data, path, "--name=" + name_file, "--clean", "--onefile", icon, additional, "./src/main.py"])
            
        # --- build folder-exe
        print(build_command_folder)
        subprocess.call(build_command_folder, shell=True)
        #remove spec
        os.remove(name_folder + ".spec")
        #remove temp folder
        shutil.rmtree(os.path.join("build", name_folder))


        # --- build onefile-exe
        print(build_command_file)
        subprocess.call(build_command_file, shell=True)
        #remove spec
        os.remove(name_file + ".spec")
        #remove temp folder
        shutil.rmtree(os.path.join("build", name_file))
        
    else:
        print("OS on which you are trying to build is not configured.")
        print("Please add a build configuration and submit a pull request: " + about.pull_url)
    
