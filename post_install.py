import subprocess


def main():
    """Install pyxf using pip inside the Poetry environment."""
    print("Running post-install script: Installing pyxf...")
    try:
        subprocess.run(
            [
                "poetry",
                "run",
                "pip",
                "install",
                "--no-build-isolation",
                "git+https://github.com/AILab-FOI/pyxf.git",
            ],
            check=True,
        )
        print("✅ Successfully installed pyxf.")
    except subprocess.CalledProcessError as e:
        print("❌ Error installing pyxf:", e)
