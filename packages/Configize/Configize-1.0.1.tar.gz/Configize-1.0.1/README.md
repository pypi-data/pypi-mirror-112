# configize

Python library to find and fetch YAML configuration for a program, respecting the XDG base directory specification.

## Example

```python
from configize import configize


# This will use $XDG_CONFIG_HOME
# The following files will be searched for, and the first existing file will be used:
# (Note, NAME is populated from the class kwarg 'Name')
# - $XDG_CONFIG_HOME/NAME.yaml
# - $XDG_CONFIG_HOME/NAME.yml
# - $XDG_CONFIG_HOME/NAME/NAME.yaml
# - $XDG_CONFIG_HOME/NAME/NAME.yml
# - $XDG_CONFIG_HOME/NAME/config.yaml
# - $XDG_CONFIG_HOME/NAME/config.yml
c = configize(Name="myproject")

# Alternatively, if using a custom path instead of XDG:
c = configize(Name="myproject", Path="/etc/myproject")

# the path field contains a pathlib.Path object to the config file
print(c.path)

# the config field contains a deserialized dict from the YAML file contents
print(c.config)
```
