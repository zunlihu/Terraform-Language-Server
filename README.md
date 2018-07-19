# Terraform-Language-Server

During developing the vscode extension, there are some related projects to provide data support for the vscode-terraform extension, 
including data source spider and etc. 
These scripts also can be used in other project involving in data collection.

These scripts can achieve the following functions:

- Data Spider through API or URL source code.
- Data Extractor for key words.
- Data Analyzer to produce statistical result.

## Data Spider for GitHub
During the project, we need to get .tf files from GitHub and terraform resource, data and module paramters information from 
https://www.terraform.io/.
Therefore, there are two kinds of data spider designed in the project. One is accessing data through 
[GitHub API v3](https://developer.github.com/v3/), and another is parsing the source code of particular URL.

GitHub as an excellent code hosting platform, provides clear [API information](https://api.github.com/). 
Related parameter settings and crawlable data information can be found in [GitHub Developer Guide](https://developer.github.com/v3/). 

### Prerequisites
Generate token: ```settings```->```Developer settings```->```Personal access tokens``` or directly open https://github.com/settings/tokens 

### Run in command line
```python spiderData_github.py --token ${your github token} --query "${what you want to search}"  --fileExtesnion ${file extesnion you want to download}```

Note: 
- There are still more other optional input arguments,  e.g. save path, search program language, sort target and order.... You can you ```-h``` for more information.
- Only first 1000 results can be returned, if you want more, please change searching condition or query items.

### Products or Results
- Download target files.
- Write the url of target files in ```url_list.txt```.

## Terraform JSON Generator

### Run in command line
```python generateALLTypesJSON.py --save_path ${SAVE_PATH}```

```python generateALLTypesJSON.py --save_path ${SAVE_PATH}```

```python generateALLTypesJSON.py --save_path ${SAVE_PATH}```

### Products or Results
- Generate JSON of different providers in separate files.
- Generate log file.

## 
