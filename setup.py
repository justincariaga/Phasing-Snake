import cx_Freeze

executables = [cx_Freeze.Executable(
    script="main.py")]

cx_Freeze.setup(
    name="Phasing Snake",
    version="1.0",
    author="Teenage Phasers",
    description="swoosh",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":[
                                "cover_art.jpg"
                                ]}},
    executables = executables
    )