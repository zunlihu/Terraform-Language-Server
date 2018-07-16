# Terraform-Language-Server

During developing the vscode extension, there are some related projects to provide data support for the vscode-terraform extension, 
including data source spider and etc. 
These scripts also can be used in other project involving in data collection.

These scripts can achieve the following functions:

- Data Spider through API or URL source code.
- Data Extractor for key words.
- Data Analyzer to produce statistical result.

## Data Spider
During the project, we need to get .tf files from GitHub and terraform resource, data and module paramters information from 
https://www.terraform.io/.
Therefore, there are two kinds of data spider designed in the project. One is accessing data through 
[GitHub API v3](https://developer.github.com/v3/), and another is parsing the source code of particular URL.

#### GitHub API v3
GitHub as an excellent code hosting platform, provides clear [API information](https://api.github.com/). 
Related parameter settings and crawlable data information can be found in [GitHub Developer Guide](https://developer.github.com/v3/). 

Parameters used in our project:
per_page: 100

#### URL

## Data Extractor


## Data Analyzer
