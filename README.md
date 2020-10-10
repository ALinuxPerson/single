# The Single Package Manager
This is a package manager meant to unify all package managers in a system into one simple package manager for you to use.

# What are it's uses then?
There are several uses to this:
 - To unify all existing package managers into one package manager as said above
 - To make it easier to find packages without hunting down multiple package managers
 - To just make life easier 
 
# Well, who is this intended for?
The single package manager is intended for:
 - Developers
 - Hackers
 - Power users
 - Command line enthusiasts
 - Regular users
 - Your grandma
 - Your dog
 
# This seems cool! How do I install it?
Well, currently there is no easy way to install this as it is a work in progress right now and there are other
priorities that rank higher than easy installation. But in case you still want to install it:

## The dependencies
 - Python 3.6 to 3.9
 - Pip
 - Poetry
 
There are other dependencies, although it is handled by poetry. If you still want to see it though, see `pyproject.toml`
or see the 'Big Thanks' section at the bottom of this readme to see at least some dependencies.

# Installation

1. Clone this repository.

   ```bash
   $ git clone https://github.com/ALinuxPerson/single.git
   ```
   
2. Change directories into the repository.

   ```bash
   $ cd single
   ```

2. Build this using poetry.

   ```bash
   $ poetry build
   ```
   
3. Change directories into `dist`.

   ```bash
   $ cd dist
   ```
   
4. Install the file with the .whl extension using `pip` (or the .tar.gz if it doesn't work).

   ```bash
   $ pip install single-0.1.0-py3-none-any.whl
   ```
   
# How easy is it to use then?
It's simple! (note that this is subject to change; the code doing this isn't even created yet):

Install a package, let's say, `dummy`:
```bash
$ single install dummy
```

Let's uninstall a package:
```bash
$ single remove dummy
```

But what if we want to install a package from the provider `apt`?:
```bash
$ single install dummy --provider apt
```

# Cool, but what is a 'provider'? and probably other terms as well?
It's good that you know.

- A **provider** This stores the metadata for sources and packages, such as names, descriptions, etc. If a provider
  were a tree, the provider would provide metadata, sources, and packages, in which sources would provide packages.
  Little hard to understand? This is how it would look visually:
  ```
              ------------
              | Provider |
              ------------
             /     |      \
            /      |       \
           /       |        \
  ------------ ----------    -----------
  | Metadata | | Source | -> | Package |
  ------------ ----------    -----------
  ```
  Now what is a source and a package? Well...
- A **source** is an interface to interact with the single package manager in order to unify an existing package
  manager on your system. Basically, this is the thing that does the unifying in the first place.
- A **package** is well, basically just like any other package in any other package manager. It is self-explanatory.


# Roadmap
The roadmap is obsolete; go to [this link](https://github.com/ALinuxPerson/single/projects/1) instead.

# License
This project is licensed under the [GNU GPLv3 License](https://choosealicense.com/licenses/gpl-3.0/).

