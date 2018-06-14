#Terraform Language Server
The Language Server protocol is used between a tool (the client) and a language smartness provider (the server) to integrate features like auto complete, goto definition, find all references and alike into the tool.

HashiCorp Terraform enables you to safely and predictably create, change, and improve infrastructure. It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

There is no full-featured language server protocol for terraform files,e.g. .tf or .hcl file. With the development of cloud technology and terraform, it is urgent and meaningful to improve such a language server for all terraform developers.

The terraform language server will be published in Visual Studio Code as an extension tool. The extension mainly work in two aspects:

 - **Language Intelligence**- Including syntax highlighting, **autocompletion**, **intelligent recommendation**, goto definition, find references and etc.
 - **Command Integration**- Including simple commands which can directly deploy resources in popular cloud platform such as aws, azure, google cloud and so on.