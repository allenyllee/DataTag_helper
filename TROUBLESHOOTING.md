# Troubleshooting


## PyInstaller

### setuptools 45.0.0 may cause PyInstaller 3.3 packaged executable fail to launch

see: [setuptools 45.0.0 may cause PyInstaller 3.3 packaged executable fail to launch · Issue #1963 · pypa/setuptools](https://github.com/pypa/setuptools/issues/1963)

> Fixed by adding a hidden import:
>
> ```python
> a = Analysis(...,
>             hiddenimports=['pkg_resources.py2_warn'],
>             ...)
> ```

### INTERNAL ERROR: cannot create temporary directory!

![INTERNAL ERROR: cannot create temporary directory!](./assets/Deepin%20截圖_選取範圍_20200601201922.png)

maybe the problem of pyinstaller under wine...

> [PyInstaller 3.6 breaks WINE compatibility when using onefile · Issue #4628 · pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller/issues/4628)
>
> Just downgrade to pyinstaller 3.5 anything works fine, no matter on Wine or on Windows.

### How do you resolve 'hidden imports not found!' warnings in pyinstaller for scipy?

> [python - How do you resolve 'hidden imports not found!' warnings in pyinstaller for scipy? - Stack Overflow](https://stackoverflow.com/questions/49559770/how-do-you-resolve-hidden-imports-not-found-warnings-in-pyinstaller-for-scipy])
>
> You need to go into the hook-scipy.py (or create one) and have it look like this:
>
> ```python
> from PyInstaller.utils.hooks import collect_submodules
> from PyInstaller.utils.hooks import collect_data_files
> hiddenimports = collect_submodules('scipy')
>
> datas = collect_data_files('scipy')
> ```
>
> then go into the hook-sklearn.metrics.cluster.py file and modify it to look like this:
>
> ```python
> from PyInstaller.utils.hooks import collect_data_files
>
> hiddenimports = ['sklearn.utils.sparsetools._graph_validation',
>                  'sklearn.utils.sparsetools._graph_tools',
>                  'sklearn.utils.lgamma',
>                  'sklearn.utils.weight_vector']
>
> datas = collect_data_files('sklearn')
> ```
>
> ---
> you can specify hooks file dir used in --additional-hooks-dir in the spec file's hookspath -- [allenyllee](https://stackoverflow.com/users/1851492/allenyllee "399 reputation")


## Gooey

### Required arguments shown as optional

> [Required arguments shown as optional · Issue #447 · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/issues/447)
>
> Here is code to reproduce:
>
> ```python
> from gooey import Gooey, GooeyParser
> @Gooey
> def main():
>     p=GooeyParser()
>     p.add_argument('-s',required=True, widget='FileChooser')
>     p.add_argument('-l',widget='DirChooser')
>     p.parse_args()
> if __name__=='__main__':
>     main()
>
> ```
>
> It still exists on 1.0.3-release as well.
>
> However, note that the arguments are not treated as optional; it's only the title "optional argument" which bothers you.
>
> As a workaround, you can create a single argument_group (optionally name it.)
>
> like this:
>
> ```python
> from gooey import Gooey, GooeyParser
> @Gooey
> def main():
>     p=GooeyParser()
>     g=p.add_argument_group()
>     g.add_argument('-s',required=True, widget='FileChooser')
>     g.add_argument('-l',widget='DirChooser')
>     p.parse_args()
> if __name__=='__main__':
>     main()
>
> ```

[Required non-positional fields show as optional · Issue #368 · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/issues/368)

[Support non-boolean mutually exclusive options · Issue #208 · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/issues/208)


## Docker setup

### How to activate a Conda environment in your Dockerfile

see: [Activating a Conda environment in your Dockerfile](https://pythonspeed.com/articles/activate-conda-dockerfile/)

The solution I use is to add

```dockerfile
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
```

after `conda create` and before any `conda install`

and at the end of dockerfile, add

```dockerfile
# Initialize conda in bash config fiiles:
RUN conda init bash
RUN echo "conda activate AI_Clerk_helper" >> ~/.bashrc
```

this will setup automatic `conda activate myenv` every time when you have login shell.

### How to use xvfb to execute command headlessly in dockerfile

see: [xvfb的安装、配置、运行（Linux）_Nobody_Wang的博客-CSDN博客_xvfb](https://blog.csdn.net/Nobody_Wang/article/details/60887659)

I use below code to headlessly run python installer under the wine:

```bash
xvfb-run --server-args="-screen 0, 1024x768x24" wine python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
```
