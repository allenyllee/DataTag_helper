# AI Clerk Helper

## How to use

### Setup Environments

Navigate the directory where you cloned the repo and pip install the dependencies

Create conda env

```shell
conda create --name AI_Clerk_helper python=3.6

conda activate AI_Clerk_helper
```

must first install wxpython before Gooey to avoid strange error

[Installation via pip fails needing pathlib2 · Issue #474 · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/issues/474)

```shell
conda install wxpython
conda install -c conda-forge gooey

pip install -r project_requirements.txt
pip install -r requirements.txt
```

### Running from .py file

```shell
python AIClerk_helper.py
```

## Building Executable by pyinstaller

### Install pyinstaller

[Gooey/Packaging-Gooey.md at master · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/blob/master/docs/packaging/Packaging-Gooey.md)

Packing Gooey into a standalone executable is super straight forward thanks to PyInstaller. It is the only dependency you'll need and can be installed via the following.

```shell
pip install pyinstaller==3.5
```

### Building with .spec file

From the command line, run

```shell
pyinstaller -F --windowed build-win.spec

```

- `-F` tells PyInstaller to create a single bundled output file
- `--windowed` disables the terminal which would otherwise launch when you opened your app.

And that's it. Inside of the `dist/` directory, you'll find a beautiful stand-alone executable that you can distribute to your users.

## Building Windows Executable from Linux

### Setup Requirements

1. add wine apt repository

   [Ubuntu - WineHQ Wiki](https://wiki.winehq.org/Ubuntu)

    ```shell
    sudo dpkg --add-architecture i386
    wget -O - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add -
    sudo add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
    ```

2. Install unmet dependence: `faudio`

    ```shell
    sudo add-apt-repository ppa:cybermax-dexter/sdl2-backport
    ```

3. Install wine 5.9

    [How to Install Wine Devel 4.8 in Ubuntu 19.04 / 18.04 | UbuntuHandbook](http://ubuntuhandbook.org/index.php/2019/05/nstall-wine-4-8-ubuntu-19-04-18-04/)

    ```shell
    sudo apt install --install-recommends winehq-devel
    ```

4. install python in wine

    [python - compiling .py into windows AND mac executables on Ubuntu - Stack Overflow](https://stackoverflow.com/questions/17709813/compiling-py-into-windows-and-mac-executables-on-ubuntu)

    ```shell
    wine --version
    winecfg

    wget https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe
    wine python-3.6.8-amd64.exe
    ```

5. install wxpython, gooey, pyinstaller and other requirements

    ```shell
    wine pip install wxpython
    wine pip install gooey
    wine pip install -r project_requirements.txt
    wine pip install pyinstaller==3.5
    ```

6. activate upx compression:

    [Releases · upx/upx](https://github.com/upx/upx/releases)

    ```shell
    wget https://github.com/upx/upx/releases/download/v3.96/upx-3.96-win64.zip
    unzip -j "upx-3.96-win64.zip" "upx-3.96-win64/upx.exe" -d "./"
    ```

    note: upx may cause dll corruption, you may want to disable UPX, see:

    - [Onefile builds not working on Windows 10, Error loading Python dll · Issue #3600 · pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller/issues/3600)
    - [python - Error when creating executable file with pyinstaller - Stack Overflow](https://stackoverflow.com/questions/38811966/error-when-creating-executable-file-with-pyinstaller)
    - [python - DLL load failure with Python3 (32bit)+PyInstaller+UPX (32bit) under Windows 10 (64bit) - Stack Overflow](https://stackoverflow.com/questions/59034735/dll-load-failure-with-python3-32bitpyinstallerupx-32bit-under-windows-10)
    - [Dependency Walker (depends.exe) Home Page](https://www.dependencywalker.com/)

### Building Executable

```shell
wine pyinstaller -F --windowed build-win.spec
```

debug mode

[Using PyInstaller — PyInstaller 3.6 documentation](https://pyinstaller.readthedocs.io/en/stable/usage.html#how-to-generate)

```shell
wine pyinstaller -F --windowed build-win.spec -d bootloader
```

### Running Windows Executable through wine

```shell
wine ./dist/AI_Clerk_helper.exe
```

![Screenshot-of-AI_Clerk_helper](./assets/Snipaste_2020-06-01_19-59-29.png)

## changelog

### v0.7.0

- 新增批次處理txt檔功能

    ![AI_Clerk_helper_v0.7](./assets/Deepin%20截圖_AI_Clerk_helper.py_20201214223220.png)

    注意：第一層的txt會自動忽略，只會加入第二層以下的txt

    ![folder_structure](assets/Deepin%20截圖_選取範圍_20201214234918.png)

- 已標註資料轉換輸出之 excel檔新增多種視圖：

    a. 以標註者為單位，一次呈現多位標著者之選項及句子標註結果
    ![sent_doc_cmp](./assets/Deepin%20截圖_libreoffice_20201214225512.png)

    b. 以選項為單位，比較多位標註者之結果
    ![doc_label_cmp](./assets/Deepin%20截圖_libreoffice_20201214224606.png)

    c. 以句子為單位，比較不同標註者結果
    ![sent_label_cmp](./assets/Deepin%20截圖_libreoffice_20201214224717.png)

    d. 以句子編號為單位，比較不同標註者結果
    ![sent_label_cmp(wide)](./assets/Deepin%20截圖_libreoffice_20201214224838.png)

    e. 將句子按類別及編號水平展開呈現
    ![sentence_label(wide)](./assets/Deepin%20截圖_libreoffice_20201214225322.png)

    f. 將句子按類別水平展開呈現
    ![sentence_label](./assets/Deepin%20截圖_libreoffice_20201214225227.png)

- 未標註 excel 檔轉換成json 時，輸出 TextID mapping

    原本的 TextID 是從 excel 中的 Content 全文計算md5 hash得到，
    但是因為excel中可能存在非法字元及表情符號，
    後來輸出的文章會經過移除非法字元及將表情符號轉成文字的處理，
    因此有可能無法還原成原始的全文，造成無法計算得到原始的TextID。
    所以另外計算一個TextID 是透過將全文移除非法字元及表情符號後再計算md5，
    並且輸出處理後的TextID 與原始TextID 的對應表，
    如此當文章同一篇文章經過處理後，因原始 TextID不同而對不上時，
    可透過 TextID mapping 比較處理後的TextID，
    應該就能對回同一篇文章。

    ![TextID mapping](assets/Deepin%20截圖_選取範圍_20201214232728.png)

### v0.6.1

- Symptom1: 修復 Windows 下合併檔案出現 openpyxl.utils.exceptions.IllegalCharacterError

    Rootcause: The previous generated excel file contains illegal character \_x0008\_, which is an OOXML escape character[1].

    Solution: remove these illegal characters before write to excel[2].

- Symptom2: 修復當 json 檔中有 \_xHHHH\_ 這類字串(以純文字形式出現)時，輸出的 excel 檔會自動轉換成 \_xHHHH\_ 的 unicode 字元(僅在 Windows 下發生，在 linux 下會將純文字的底線(underscore, _) 再跳脫一次，轉換成 \_x005F_x0008\_ [1] 儲存到 excel)

    Rootcause: maybe openpyxl bug?

    Solution: this is a workaround. when dataframe read from json file by read_json(), look for \_xHHHH\_ pattern in this dataframe, and unescape it[3] before write to excel.

- References

    [1]:[VTBString Class (DocumentFormat.OpenXml.VariantTypes) | Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.varianttypes.vtbstring?view=openxml-2.8.1)

    > [ISO/IEC 29500-1 1st Edition]
    >
    > **bstr (Basic String)**
    >
    > This element defines a binary basic string variant type, which can store any valid Unicode character. Unicode characters that cannot be directly represented in XML as defined by the XML 1.0 specification, shall be escaped using the Unicode numerical character representation escape character format \_xHHHH\_, where H represents a hexadecimal character in the character's value. [*Example*: The Unicode character 8 is not permitted in an XML 1.0 document, so it shall be escaped as \_x0008\_. *end example*] To store the literal form of an escape sequence, the initial underscore shall itself be escaped (i.e. stored as \_x005F\_). [*Example*: The string literal *\_x0008\_* would be stored as *\_x005F_x0008\_*. *end example*]
    >
    > The possible values for this element are defined by the W3C XML Schema *string* datatype.

    [2]:[(1条消息)openpyxl.utils.exceptions.IllegalCharacterError 错误原因分析及解决办法_村中少年的专栏-CSDN博客](https://blog.csdn.net/javajiawei/article/details/97147219)

    > 进入python命令行模式，输入如下：
    >
    > ```python
    > >>> import sys
    > >>> help('openpyxl')
    >
    > ```
    >
    > 可得openpyxl模块的路径如下`/usr/local/lib/python2.7/site-packages/openpyxl`，查看该目录下的cell子目录中的cell.py文件，定位到具体错误代码为：
    >
    > ```python
    > def check_string(self, value):
    >     """Check string coding, length, and line break character"""
    >     if value is None:
    >         return
    >     # convert to unicode string
    >     if not isinstance(value, unicode):
    >         value = unicode(value, self.encoding)
    >     value = unicode(value)
    >     # string must never be longer than 32,767 characters
    >     # truncate if necessary
    >     value = value[:32767]
    >     if next(ILLEGAL_CHARACTERS_RE.finditer(value), None):
    >         raise IllegalCharacterError
    >     return value
    >
    > ```
    >
    > 其中`ILLEGAL_CHARACTERS_RE`的定义在文件的开头，如下：
    >
    > ```python
    > ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    >
    > ```
    >
    > 这里面的非法字符都是八进制，可以到对应的ASCII表中查看，的确都是不常见的不可显示字符，例如退格，响铃等，在此处被定义为excel中的非法字符。\
    > 解决上述错误有两种方法，如下：\
    > 1，既然检测到excel中存在`[\000-\010]|[\013-\014]|[\016-\037]`这些非法的字符，因此可以将字符串中的非法字符替换掉即可，在重新写入excel即可。如下：
    >
    > ```python
    > text= ILLEGAL_CHARACTERS_RE.sub(r'', text)
    > ```
    >

    [3]:[openpyxl.utils.escape — openpyxl 3.0.5 documentation](https://openpyxl.readthedocs.io/en/stable/_modules/openpyxl/utils/escape.html)

    > ```python
    > def unescape(value):
    >     r"""
    >     Convert escaped strings to ASCII: _x000a_ == \n
    >     """
    >
    >
    >     ESCAPED_REGEX = re.compile("_x([0-9A-Fa-f]{4})_")
    >
    >     def _sub(match):
    >         """
    >         Callback to unescape chars
    >         """
    >         return chr(int(match.group(1), 16))
    >
    >     if "_x" in value:
    >         value = ESCAPED_REGEX.sub(_sub, value)
    >
    >     return value
    > ```

### v0.6

- 新增合併檔案功能

    ![merge file](./assets/Deepin%20截圖_AI_Clerk_helper.py_20200916201632.png)

### v0.5

- 新增 train/test 切割功能

    ![train test split 1](./assets/Deepin%20截圖_選取範圍_20200916175230.png)

    ![train test split 2](./assets/Deepin%20截圖_選取範圍_20200916175730.png)

### v0.4.1

- 修正當某個欄位漏標時，會產生error而停止輸出
    解法：將漏標的欄位填入nan，方便其他人使用輸出後的檔案做檢查

### v0.4

1. 新增原文欄位(移除tag 標籤)

    ![add Content(remove tag)](assets/Deepin%20截圖_選取範圍_20200910203302.png)

2. 多選選項直接以文字格式用逗號分隔儲存在同一格中

    ![multiple options](assets/Deepin%20截圖_選取範圍_20200910203330.png)

3. 句子與其標註攤平成兩欄(Sent_Label, Sentence)，沒有句子標註的TextID 則此兩欄留空白

    ![vertical sent view](assets/Deepin%20截圖_選取範圍_20200910203417.png)

### v0.3

- 將已標註檔案json 檔下載回來後，轉換成excel檔

    轉換後的 excel 內容分三頁：第一頁是contents，包含作者，標題、內文、標註者等；第二頁是document label，也就是類別標註；第三頁是sentence label 句子標註，因為句子有很多類，每類數量不一，我是將之橫向展開成不同欄

    ![convert json to excel](./assets/Snipaste_2020-07-15_18-37-31.png)

## Troubleshooting

- [setuptools 45.0.0 may cause PyInstaller 3.3 packaged executable fail to launch · Issue #1963 · pypa/setuptools](https://github.com/pypa/setuptools/issues/1963)

    > Fixed by adding a hidden import:
    >
    > ```python
    > a = Analysis(...,
    >             hiddenimports=['pkg_resources.py2_warn'],
    >             ...)
    > ```

- INTERNAL ERROR: cannot create temporary directory!

    ![INTERNAL ERROR: cannot create temporary directory!](./assets/Deepin%20截圖_選取範圍_20200601201922.png)

    maybe the problem of pyinstaller under wine...

    > [PyInstaller 3.6 breaks WINE compatibility when using onefile · Issue #4628 · pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller/issues/4628)
    >
    > Just downgrade to pyinstaller 3.5 anything works fine, no matter on Wine or on Windows.

- How do you resolve 'hidden imports not found!' warnings in pyinstaller for scipy?

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

- Required arguments shown as optional

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

## References

### Gooey

- [chriskiehl/Gooey: Turn (almost) any Python command line program into a full GUI application with one line](https://github.com/chriskiehl/Gooey)

### Gooey Options

- [Gooey/Gooey-Options.md at master · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/blob/master/docs/Gooey-Options.md)

### examples

- [chriskiehl/GooeyExamples: Example programs to Demonstrate Gooey's functionality](https://github.com/chriskiehl/GooeyExamples)

### mutually_exclusive_group

- [Gooey/all_widgets_subparser.py at 66f154decb8cd7d140a702277d8c262c4d8194cc · chriskiehl/Gooey](https://github.com/chriskiehl/Gooey/blob/66f154decb8cd7d140a702277d8c262c4d8194cc/gooey/tests/integration/programs/all_widgets_subparser.py#L75-L80)

- [python - How to define a mutually exclusive group of two positional arguments? - Stack Overflow](https://stackoverflow.com/questions/15530117/how-to-define-a-mutually-exclusive-group-of-two-positional-arguments)

- [Python argparse mutual exclusive group - Stack Overflow](https://stackoverflow.com/questions/17909294/python-argparse-mutual-exclusive-group)

### widget example

FileChooser, DirChooser, FileSaver, MultiFileChooser, DateChooser, TimeChooser

- [GooeyExamples/widget_demo.py at d0606a8d543babe1cff5db215d4d37e26888b490 · chriskiehl/GooeyExamples](https://github.com/chriskiehl/GooeyExamples/blob/d0606a8d543babe1cff5db215d4d37e26888b490/examples/widget_demo.py#L39-L54)

### dynamic update

- [GooeyExamples/dynamic_updates.py at master · chriskiehl/GooeyExamples](https://github.com/chriskiehl/GooeyExamples/blob/master/examples/dynamic_updates.py)
