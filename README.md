# uv-monorepo-demo

### goals
- allow for quick iteration on future projects
    - make it easy to share code between services
    - changes to services/libraries in monorepo should be easy to test
- simple build tooling
- simple dependency management/resolution

### proposed structure
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
    - generate a `requirements.txt` file using requirements specified in `pyproject.toml`
    - extract local shared library dependencies
    - compile local shared library dependencies as standalone wheels
    - compile executable `pex` binary using local wheels for local deps (this will happen in docker)
    - note: eventually we will publish docker images and run on kubernetes which will allow us to delete this entirely

### dev flow

run locally:
```
uv pip install -e demo/apps/project1
uv run python -m project1.main
```

```
uv pip install -e demo/apps/project2
uv run python -m project2.main
```

build pex (hardcoded to build project1):
```
uv run python build.py
```

### open questions
- enforce a single global version of python?
- enforce a single global version of ALL dependencies? (I don't think uv will do this automatically since each project has its own lockfile, need to confirm)
- can we improve how libraries are handled?
    - currently, we generate (implicitely versioned) wheels for libraries in a temporary directory and use that in the pex install
