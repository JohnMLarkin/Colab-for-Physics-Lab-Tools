
# import ipykernel
# import urllib
# import json
import os
import shutil
from notebook import notebookapp
from requests import get


from .git_access import LocalRepo
from .git_access._run_cmd import run_cmd 

def convert_to_pdf(repo=None):
    for srv in notebookapp.list_running_servers():
        try:
            if srv['token'] == '' and not srv['password']:
                server = srv['url'] + 'api/sessions'
            else:
                server = srv['url'] + 'api/sessions?token=' + srv['token']
            nb_server_info = get(server).json()[0]
        except:
            pass
        nb_loc = nb_server_info['path']
        if 'fileId=' in nb_loc: # Looks like we are in Colab
            nb_name = nb_server_info['name']
            from google.colab import files
            gdrive_home = '/content/drive/MyDrive'
            nb_path = gdrive_home + '/Colab Notebooks/'
            tmp_path = '/tmp'

            # If the drive is not already mounted, attempt to mount it
            if not os.path.isdir(gdrive_home):
                from google.colab import drive
                drive.mount('/content/drive')

            if 'fileId=https%3A%2F%2Fgithub.com%2F' in nb_loc: # and file on GitHub
                print('Note: Conversion will be performed on the most recent commit of this notebook on GitHub, not the working copy.')
                nb_name_us = nb_name.replace("%20","_")
                nb_name_us = nb_name_us.replace("-","_")
                nb_name = nb_name.replace("%20"," ")
                if isinstance(repo,LocalRepo):
                    repo.pull()
                    shutil.copy(os.path.join(repo.repo_path, nb_name_us), os.path.join(tmp_path, nb_name))
                else:
                    print('Please pass a GitHub repo object as an argument.')
                    return
            else:
                if not os.path.isfile(os.path.join(nb_path, nb_name)):
                    raise ValueError(f"file '{nb_name}' not found in path '{nb_path}'")
                else:
                    shutil.copy(os.path.join(nb_path, nb_name), os.path.join(tmp_path, nb_name))
            
            # If PDF with the same name exists, remove it
            nb_file = os.path.join(tmp_path, nb_name)
            pdf_file = os.path.join(tmp_path, nb_name.split(".")[0] + ".pdf")
            if os.path.isfile(pdf_file):
                os.remove(pdf_file)
            
            # Install the packages required for conversion
            print("Installing required packages. This often takes 1-2 minutes.")
            run_cmd("apt update >> /dev/null && apt install texlive-xetex texlive-fonts-recommended texlive-generic-recommended >> /dev/null")

            # Attempt to convert to PDF (via LaTeX)
            print(f"Preparing to convert '{nb_name}'")
            run_cmd(f"jupyter nbconvert --output-dir='{tmp_path}' '{nb_file}' --to pdf")

            # Attempt to download
            files.download(pdf_file)
        else:
            print('Sorry. Only implemented for Colab.')
            return

    