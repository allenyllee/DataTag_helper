# AI Cleark Helper

## setup

- [chriskiehl/GooeyExamples: Example programs to Demonstrate Gooey's functionality](https://github.com/chriskiehl/GooeyExamples)

### Installation Instructions

Navigate the directory where you cloned the repo and pip install the dependencies

Create conda env
```
conda create --name AI_Clerk_helper python=3.6

conda activate AI_Clerk_helper
```

must first install wxpython before Gooey to avoid strange error
[Installation via pip fails needing pathlib2 · Issue #474 · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/issues/474)
```
conda install wxpython
conda install -c conda-forge gooey

pip install -r project_requirements.txt
pip install -r requirements.txt
```

### Running the examples

```
python AIClerk_helper.py
```

## packaging

- [Gooey/Packaging-Gooey.md at master · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/blob/master/docs/packaging/Packaging-Gooey.md)


Packing Gooey into a standalone executable is super straight forward thanks to PyInstaller. It is the only dependency you'll need and can be installed via the following.
```
pip install pyinstaller
```

### Running the .spec file

From the command line, run

```
pyinstaller -F --windowed build-win.spec

```

-   `-F` tells PyInstaller to create a single bundled output file
-   `--windowed` disables the terminal which would otherwise launch when you opened your app.

And that's it. Inside of the `dist/` directory, you'll find a beautiful stand-alone executable that you can distribute to your users.

### issue

- [setuptools 45.0.0 may cause PyInstaller 3.3 packaged executable fail to launch · Issue #1963 · pypa/setuptools](https://github.com/pypa/setuptools/issues/1963)

Fixed by adding a hidden import:
```
a = Analysis(...,
             hiddenimports=['pkg_resources.py2_warn'],
             ...)
```

