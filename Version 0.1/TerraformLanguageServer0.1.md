# Terraform Language Server v0.1
This version is seen as a baseline for the whole project.

## Function 
**Resource and data types auto completion for aws, azure, google cloud and etc.**

### Full completion

When you just type "", the language server can recommend a list of resource/data types for you.

- Resource types Completion

![](https://github.com/zunlihu/Terraform-Language-Server/blob/master/images/Version%200.1/resourceCompletion.png)

- Data types Completion

![](https://github.com/zunlihu/Terraform-Language-Server/blob/master/images/Version%200.1/dataCompletion.PNG)

### Half Completion
With the user continuing to type in the editor, the server will filter unrelated types, but the remaining list still in the recommended order.

![](https://github.com/zunlihu/Terraform-Language-Server/blob/master/images/Version%200.1/halfCompletion.png)

## Implementation Details
### Data Sources
428894 .tf files from GitHub.

### Data Analysis

Through frequency statistics, the resources and data types usage frequency can be get. 

**Note:**To get valid statistic result, we have to consider the comment in the data file. For example, # and /*...*/.

- Word Cloud

- Bar



### Apply to VS Code
VS Code have a lot of API for extentionbility.