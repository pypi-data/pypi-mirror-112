import setuptools
setuptools.setup(name='atto',
                version='1.1.8',
                description='Simple curses text editor',
                long_description_content_type='text/markdown',
                long_description=
"""
## atto - Simple curses text editor

### Installation
```
pip install atto
```
### Usage
#### As script
```
[user@localhost ~] atto "<filename>"
```
#### In your code
```python
import atto 
atto.edit('filename.txt')
```
### Keys
1. i to switch to insert mode
1. ESC to return from insert mode
1. F4 to exit without saving
1. F2 to save
1. F10 to save and exit
1. Arrow keys to move cursor

### License
atto is licensed under **GPL License**
### Requirements
1. `cursor`: Cross-platform library for showing and hiding cursor
### Changelog
#### 1.0.0
Initial release
#### 1.1.0
Major bug fixes,
Long lines handling improvements
#### 1.1.1
Fixed tab bugs
#### 1.1.2
Added --version command line switch
#### 1.1.3
Minor bug fixes
#### 1.1.4
Major bug fixes
#### 1.1.5
Patched version
#### 1.1.6
Added LICENSE file
#### 1.1.7
Minor bug fixes
#### 1.1.8
Added homepage
""",
                install_requires=['cursor'],
                packages=['atto'],
                classifiers=[
                    "Development Status :: 4 - Beta",
                    "Environment :: Console :: Curses",
                    "Intended Audience :: End Users/Desktop",
                    "License :: OSI Approved :: GNU General Public License (GPL)",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: 3",
                    "Topic :: Text Editors",
                    ],
                entry_points={
                    'console_scripts':['atto = atto:edit']
                    },
                author='Adam Jenca',
                author_email='jenca.adam@gmail.com',
                url='https://github.com/jenca-adam/atto/',
                )


