# Changes in the FPL IDE
## 1.0.0 
* Initial IDE
* Open, Save, Save As, Exit menu bars
* Build menu bar
## 1.1.0
* Paned windows added 
* Line numbers in the editor added
* Status bar added
* Row and column in the status bar added
* Syntax highlighting for open files added
* Syntax tree clickable added (jumps to position in text)
* Text clickable added (jumps to position in syntax tree)
## 1.2.0
* Saving bug corrected
* Error list and highlighting run in a separate thread changing dynamically with the user edits in a file
* Layout improvements
* Number of errors and number of warnings added
## 1.2.1
* Key events for menu items (on Windows 10, press 'Alt')
* Bug fix closing application
* Security messages for saving files before quitting
## 1.2.2
* Performance improvements while typing: syntax highlighting, error list and syntax tree updates only on demand 
* Prettify code (experimental)
* Auto indent when opening new braces or parentheses (experimental)
* UTF-8 support 
## 1.2.3
* Indentation when pressing <tab>
* Outdentation when pressing <Shift-tab>
* Help menu added (about)
* Settings menu added (settings)
* Settings window will open and show the available settings, but no editing is yet possible.
## 1.2.4
* Settings window allows editing the settings
* Unified convention for importing tkinter in different classes 
* Bugfix indentation when entering new lines
* Automated entry of closing brackets, braces, and parentheses
## 1.2.5
* Bugfix relative folders for importing package files
* Separation of syntax transforming and syntax analysis in the fpl interpreter (since version 1.2.0) reflected in the ide
## 1.2.6
* Font error list changed
## 1.2.7
* Compatibility adjustments to the FPL interpreter version 1.4.1 
## 1.2.8
* Bugfix highlighting
