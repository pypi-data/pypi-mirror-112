# h5p-plugin

Plugin for rendering h5p components in Sphinx.

Given h5p components, the plugin can be used to easily and with short syntax render h5p components inside .rst files and .md files.

Syntax for rendering in .rst files is:  
**.. iframe:: id**  
id has to match with the given h5p components folder name.

Syntax for rendering in .md files is:

**```{eval-rst}**

**.. iframe:: id**

**```**


## Configuring h5p path

In order for plugin to find the right path to h5p component folder, the path needs to be specified in projects conf file.
In conf file, create variable named html_template_url and assign path to it. 