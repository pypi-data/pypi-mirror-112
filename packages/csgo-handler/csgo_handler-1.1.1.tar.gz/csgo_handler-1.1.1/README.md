# csgo_handler

Program that detects when CSGO is launched or closed and runs a script.

This program only works on Linux as it depends on `inotify`.

## Configuration

The configuration file location respects XDG, and will try the following paths, in this order:
 - `$XDG_CONFIG_HOME/csgo_handler.yaml`
 - `$XDG_CONFIG_HOME/csgo_handler.yml`
 - `$XDG_CONFIG_HOME/csgo_handler/csgo_handler.yaml`
 - `$XDG_CONFIG_HOME/csgo_handler/csgo_handler.yml`
 - `$XDG_CONFIG_HOME/csgo_handler/config.yaml`
 - `$XDG_CONFIG_HOME/csgo_handler/config.yml`

 **NOTE**:
  - `$XDG_CONFIG_HOME` will default to `$HOME/.config` on most systems.
  - A lazy match is used, meaning the first file that exists will be used.

### Example configuration

```yaml
---

# Path to the 'csgo.sh' script
script_path: /opt/games/steamapps/common/Counter-Strike Global Offensive/csgo.sh

# Action to run when game starts
start_script:
  - /bin/bash
  - -c
  - nvidia-settings -a 'DigitalVibrance[DFP-5]=1023'

# Action to run when game stops
stop_script:
  - /bin/bash
  - -c
  - nvidia-settings -a 'DigitalVibrance[DFP-5]=0'
```

## Command-line parameters

The following parameters are present:

| Argument        | Short argument | Explanation                                | Default | Example                                  |
|-----------------|----------------|--------------------------------------------|---------|------------------------------------------|
| `--config`      | `-c`           | Override config path                       | `None`  | `csgo_handler -c /etc/csgo_handler.yaml` |
| `--config_path` | `-C`           | Search for config files within this folder | `None`  | `csgo_handler -C /etc/csgo_handler`      |
| `--daemon`      | `-D`           | Run as a daemon                            | `False` | `csgo_handler -D`                        |
