# Goo: a dependency manager for Godot that just works

![ugly logo](goo.png)

Goo is a simple dependency/plugin manager for Godot written in Python that
aims to be really easy to use. For Goo to be functional it doesn't require
a whole new third-party plugin repository, since plugins can be installed
and updated from the official Godot Asset Library, or from Git repos hosted
on GitLab, GitHub, Codeberg, Sourcehut, etc.

## Why this exists
If you know exactly what you're doing and you have already used other
dependency management tools such as npm, this is not new to you. We recommend
you proceed directly to the installation.

### The problem
Godot has no dependency management, in this specific case, by "dependencies"
we mean "Godot plugins", which in some (or most) cases are analogous to NodeJS
packages or Rust crates. Godot, by not having dependency management, causes
developers to be forced to push the source code of all the dependencies
to the project's Git repo to make it functional, which makes the repository
take up more space and makes it difficult to update the dependencies (plugins),
especially if your project depends on several of them.

### The solution
Goo lets you easily install and update all the dependencies of your project,
and instead of pushing all the dependencies to GitLab or GitHub, you just
push a file named "goo.json", which contains a list of the dependencies that
Goo must install so your game works properly.

## Installation
### Requirements
* Install [Python 3.x](https://www.python.org/downloads/) (and pip)
* Install [Git](https://git-scm.com/)
### Linux
* Run `pip install goo-pm` and that's it.
### Windows
Do the same as for Linux (Goo is a CLI tool like npm, you must install it and
use it from the command prompt)

__Important__: If you're on Windows, make sure you installed Git and you added
the path to git.exe to the PATH environment variable of your system.
[More information here](https://www.answerlookup.com/how-add-git-windows-path-environment-variable).
### Mac OS
The same as for linux... I guess?

## Usage
* Use `goo init` in the root directory of your project to initialize Goo. By
default, Goo will assume you're using the latest stable version of Godot.
In case you're using an older or newer version, you need to specify it
by using the option `--gd-version "x.x.x"` or by changing the option
"godot-version" in the goo.json file.
* Use `goo install <plugin>` to install plugins (dependencies) from the
[Godot Asset Library](https://godotengine.org/asset-library/asset)
or from a Git repo. To install a plugin from the Asset Library, run
`goo install author/plugin_name` (example: `goo install "Jane Doe/My Plugin"`).
To install a plugin from a Git repo, run
`goo install https://url.to/the/plugin/repo`.
* Use `goo install` with no arguments to install the missing
dependencies of a project.
* Use `goo update` to update all the installed dependencies.
* Use `goo uninstall` to uninstall a plugin and remove it from
the dependency list file (goo.json)

## Goo only works properly with VALID plugins
### What is a valid plugin?
A valid Godot plugin must have a "plugin.cfg" file with information
about itself. If you make plugins for Godot, don't forget to
change the "version" value every time you release a new version
of your plugins (this is important because Goo reads that value to
know whether a plugin should be updated or not).

For more information about creating plugins, read
[this](https://docs.godotengine.org/en/stable/tutorials/plugins/editor/making_plugins.html).

## License
BSD Zero Clause. Read "LICENSE" for more info.
