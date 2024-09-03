# uv-monorepo-demo

### notes
- two types of projects:
    - library: a project designed to consolidate shared logic
        - libraries can consume other libraries
    - service: a project designed to run as a standalone executable
        - services can consume libraries
        - services cannot consume other services

- services are in `demo/apps`, libraries are in `demo/libs`
- each service and library manages its own 1. python version and 2. dependency version (rolls up into a `uv.lock` file per-project)
- services and libraries specify dependencies in their `pyproject.toml` files
- `build.py` will:
    - take a target project as input
    - parse local dependencies from the `pyproject.toml` file
    - compile local shared library dependencies as standalone wheels
    - copy local dependencies packaged as wheels into docker image, download external dependencies
    - compile as executable `pex` binary

### open questions
- enforce a single global version of python?
- enforce a single global version of ALL dependencies? (I don't think uv will do this automatically since each project has its own lockfile, need to confirm)
