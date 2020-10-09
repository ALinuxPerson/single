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

