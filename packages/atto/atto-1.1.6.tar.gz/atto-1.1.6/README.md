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

