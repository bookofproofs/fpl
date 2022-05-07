# Changes in the FPL IDE
## 1.6.6
* Refactoring
  * The syntax and semantical analysis and function was moved from FrameWithLineNumbers object to FplIde object, because it has to be done not for a single opened FPL file but for the whole FPL theory that might consist of many FPL files.
  * Consequently, the bindings Alt-Control-g and Alt-Control-l were deprecated.
* Bugfixes
  * Syntax highlighting was not available for files of the theory that were opened by the user in addition to the main FPL theory file.
## 1.6.5
* Bugfixes
  * Build current FPL discontinued since building a single file in the context of a whole theory is not feasible with respect to context-specific errors: we use build whole theory instead.
  * AttributeError save_file when building theory fixed.
  * Double-click on default constructors led to a run-time error since there was no position to jump to. Those default constructors are not in the source code and the objects are defined intrinsically.
* Refactoring
  * One central static method for writing files to disk in futils.py
## 1.6.4
* Bugfixes:
  * File names in error list are now error-location specific
  * Error-positions from other files were highlighted also in the currently opened file
  * Double-clicking the error of a file that was not opened did not work  
  * Highlighting of variables was broken
  * Affected symbol table test cases adjusted to the new positions
## 1.6.3
* Bugfixes:
  * no more duplicates of variable-related errors and warnings
* Feature:
  * Errors and warnings are now sorted by severity and occurance (file / line / column)  
## 1.6.2
* Refactoring:
  * A separate new class for the ObjectBrowser.py. Code separated from the main code in the fplide.py file.
  * Name column removed from the ObjectBrowser
* Bugfixes:
  * Wait cursor added
  * Namespaces sorted alphabetically
  * File names removed from object browser for pure outline lines that do not refer to actual source code. 
  * Event "double-click" instead of "click" bound to the Error List
* Feature:
  * Double-clicking the object browser will open a file of the theory and jump to the respective position in the source code.
## 1.6.1
* Bugfixes:
  * AttributeError: 'FplIde' object has no attribute 'fpl_source_transformer' when reformatting code corrected. 
  * Higlighting and (any previous) positions of errors in the FPL code are now correctly calculated after reformatting the code. 
  * When saving a file, the cursor stays at the last position in the editor end does not jump to its beginning. 
  * When closing a theory, the symbol table gets cleared so that it does not mix up with a new theory to be opened.   
## 1.6.0
* Feature: 
  * Command Build->Current FPL File - when there are FPL interpreter errors in an FPL file and the user corrects them in the editor, the menu command will re-interpret the file again and creates an amended error list.  
* Refactoring
  * Menu "File" deprecated (removed)
* Minor bug-fixes
## 1.5.0
* Feature: 
  * A user dialog for the menu command FPL Theory->Open
  * Command FPL Theory->Close
## 1.4.2
* Bugfix: Menu command Fpl Theory->New now corrects the disabled status of the menu after creating a new theory.
* Refactoring: New class IdeModel to store the state of the ide and main data or handler pointers.
## 1.4.1
* Bugfix: Menu command Fpl Theory->New now opens the FPL file after creating it.
## 1.4.0
* Feature: A user dialog for the menu command FPL Theory->New.
* Refactoring: 
  * A class for common dialogs, 
  * SettingsDialog renamed in DialogSettings
## 1.3.1
* Refactoring and re-design of the menu items (without implementation).
* Help guide file markdown added.
## 1.3.0
* Features: The object tree visualizes the structure of the mathematical theory opened in the IDE.
## 1.2.9
* Features: 
  * The error list now shows the diagnosis id of errors instead of the class name of the error
  * Object explorer shows an example of how it will be supposed to look like later.
  * A more readable font family in Error list
  * Tabs "Syntax Browser" and "Semantic Browser" discontinued
  * Tab "Output" renamed in "Debug"
* Bug fixes:
  * Each editor cursor column in the status bar starts at 1 (instead of 0)
  * Double-clicking an error from error list jumps to the correct starting column (instead of starting colum + 1) in the editor.
  * Errors are red underlined in code editor (preliminary implementation - only the first character)
* Reversed the order of items in release notes to make the last change appear first.
  * This CHANGES.md file
  * CHANGES.md file of the FPL grammar
  * CHANGES.md file of the FPL interpreter
* New CHANGES.md file added to poc/theories
## 1.2.8
* Bugfix highlighting
## 1.2.7
* Compatibility adjustments to the FPL interpreter version 1.4.1 
## 1.2.6
* Font error list changed
## 1.2.5
* Bugfix relative folders for importing package files
* Separation of syntax transforming and syntax analysis in the fpl interpreter (since version 1.2.0) reflected in the ide
## 1.2.4
* Settings window allows editing the settings
* Unified convention for importing tkinter in different classes 
* Bugfix indentation when entering new lines
* Automated entry of closing brackets, braces, and parentheses
## 1.2.3
* Indentation when pressing <tab>
* Outdentation when pressing <Shift-tab>
* Help menu added (about)
* Settings menu added (settings)
* Settings window will open and show the available settings, but no editing is yet possible.
## 1.2.2
* Performance improvements while typing: syntax highlighting, error list and syntax tree updates only on demand 
* Prettify code (experimental)
* Auto indent when opening new braces or parentheses (experimental)
* UTF-8 support 
## 1.2.1
* Key events for menu items (on Windows 10, press 'Alt')
* Bug fix closing application
* Security messages for saving files before quitting
## 1.2.0
* Saving bug corrected
* Error list and highlighting run in a separate thread changing dynamically with the user edits in a file
* Layout improvements
* Number of errors and number of warnings added
## 1.1.0
* Paned windows added 
* Line numbers in the editor added
* Status bar added
* Row and column in the status bar added
* Syntax highlighting for open files added
* Syntax tree clickable added (jumps to position in text)
* Text clickable added (jumps to position in syntax tree)
## 1.0.0 
* Initial IDE
* Open, Save, Save As, Exit menu bars
* Build menu bar
