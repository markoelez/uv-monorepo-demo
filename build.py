import os
import tempfile
import subprocess
from pathlib import Path


def build_pex(project_path, output_dir, repo_root, wheel_dir):
    project_name = os.path.basename(project_path)
    requirements_file = Path(project_path) / "requirements.txt"

    # Generate requirements.txt using uv pip compile
    subprocess.run(
        [
            "uv",
            "pip",
            "compile",
            "pyproject.toml",
            "--output-file",
            str(requirements_file),
        ],
        cwd=project_path,
    )

    # Process the requirements file to use wheel files for local dependencies
    process_requirements(requirements_file, repo_root, wheel_dir)

    # Build PEX file
    output_pex = Path(output_dir) / f"{project_name}.pex"

    pex_command = [
        "pex",
        "-r",
        str(requirements_file),
        "-o",
        str(output_pex),
        "--python-shebang",
        "/usr/bin/env python3.11",
        "--python",
        "python3.11",
        "--platform",
        "macosx_14_0_x86_64-cp-311-cp311",
        "-m",
        "project1.main:main",
        "--sources-directory",
        str(project_path),
        "--sources-directory",
        str(repo_root / "demo" / "libs"),
        f"--find-links={wheel_dir}",
        "--inherit-path=fallback",
        "--disable-cache",
        "--no-emit-warnings",
        str(project_path),
    ]

    # Add wheels for local dependencies
    for wheel_file in os.listdir(wheel_dir):
        if wheel_file.endswith(".whl"):
            pex_command.append(str(Path(wheel_dir) / wheel_file))

    subprocess.run(pex_command, cwd=repo_root, check=True)

    print(f"Built PEX for {project_name}: {output_pex}")


def process_requirements(requirements_file, repo_root, wheel_dir):
    with open(requirements_file, "r") as f:
        lines = f.readlines()

    processed_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("../../"):
            # This is a local dependency added by uv pip compile
            rel_path = line.split("#")[0].strip()  # Remove comments
            abs_path = (repo_root / rel_path).resolve()
            wheel_file = find_wheel(wheel_dir, abs_path.name)
            if wheel_file:
                processed_lines.append(f"{wheel_file}\n")
            else:
                print(f"Warning: Wheel not found for {abs_path.name}")
        elif not line.startswith("#"):
            processed_lines.append(f"{line}\n")

    with open(requirements_file, "w") as f:
        f.writelines(processed_lines)


def find_wheel(wheel_dir, project_name):
    for file in os.listdir(wheel_dir):
        if file.startswith(project_name) and file.endswith(".whl"):
            return str(Path(wheel_dir) / file)
    return None


def build_wheel(project_path, output_dir):
    subprocess.run(
        [
            "uvx",
            "--from",
            "build",
            "pyproject-build",
            "--installer",
            "uv",
            "--outdir",
            output_dir,
        ],
        check=True,
        cwd=project_path,
    )


def main():
    repo_root = Path(__file__).parent.resolve()
    output_dir = repo_root / "dist"
    output_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as wheel_dir:
        # Build wheels for all local libraries
        local_libs = ["demo/libs/lib1"]  # Add all your local libraries here
        for lib in local_libs:
            build_wheel(repo_root / lib, wheel_dir)

        # Build PEX for project1
        build_pex(repo_root / "demo/apps/project1", output_dir, repo_root, wheel_dir)


if __name__ == "__main__":
    main()
