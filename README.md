# Tools for Colab in the Physics Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI](https://img.shields.io/pypi/v/whit-phys-util)
![PyPI - Downloads](https://img.shields.io/pypi/dm/whit-phys-util)
![GitHub last commit](https://img.shields.io/github/last-commit/JohnMLarkin/Colab-for-Physics-Lab-Tools)

Tools to support the use of Google Colab + GitHub for teaching undergraduate physics labs. Support for private repositories enables the use of GitHub Classroom.

## Installation

This package is primarily intended for use within Google Colab. To install in a Colab notebook:
```
!pip install whit-phys-util
```

## Importing

To import the package after installation:
```python
import whit_phys_util
```

## Creating a GitHub credentials file

If you will be regularly connecting GitHub private repositories to Colab sessions, the recommendation is to create a file containing your GitHub info and store it in your Google Drive.

1. Create a file with the name `.env` or `dotenv` using the plain text editor of your choice.
2. This file should have the following format:
    ```
    # for git
    user_email = "yourname@host"
    user_name = "your_GitHub_user_name"
    gh_token = "GitHub_personal_access_token"
    ```
    In my case `"yourname@host"` was `"jlarkin@whitworth.edu"` and `"your_GitHub_user_name"` was `"JohnMLarkin"`.
3. Next, login to GitHub and select **Settings** from the menu hiding under your profile picture.
4. Select **Developer settings** from the sidebar and then **Personal access tokens**.
5. Click on the **Generate new token** button.
6. **Note** is your name for this token so you can remember what it does and where it is used. Picking something like `Colab repo link` makes that clear.
7. Check the **repo** box and then the **Generate token** button.
8. Copy this token and paste it into your `.env`/`dotenv` file in place of `GitHub_personal_access_token`.
9. Move this file to the top-level folder of your Google Drive.

## Working with a GitHub repository

### Clone a repository to Colab session storage

Replace `REPO_URL` with the URL to your private GitHub repository:
```python
repo = whit_phys_util.local_repository("REPO_URL")
```

If your Google Drive is not already mounted to this Colab session, you will be prompted to do so. If you created the GitHub credentials file as described above, this will then create a clone of the repository located in `/content/REPO_NAME`. Your current working directory will also be changed to this folder.

