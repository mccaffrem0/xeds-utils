# xeds-utils
##### Python utility for creating and handling eXtensible Electronic DataSheets.

### Requirements:
bitstream (pip install bitstream) (https://pypi.python.org/pypi/bitstream/2.0.3)

### Usage:
Run xeds.pyw

##### Building a Template
1. Select the "Build Template" tab from the top of the window. 
2. Select a parent element. First selection will always be "Template".
3. Add a property or subXEDS
    - For subXEDS:
        1. Check the "subXEDS" check box.
        2. Name the subXEDS
        3. Click "Add Element" or press Enter
    - For Property:
        1. Ensure that "subXEDS" is not checked.
        2. Fill in the name, bit length, datatype, and units of the property.
        3. Click "Add Element" or press Enter
4. Repeat steps 2, 3, and 4 until template is complete.
5. Click File -> Export XML to save your template.

##### Populating an XEDS
1. Select the "Create/Edit XEDS" tab from the top of the window. 
2. Click File -> Import XML and select a template.
3. Select a row that contains a Property (not a subXEDS).
4. Enter a value in the "Field Value"  entry box.
5. Press Enter
6. The value will be entered and the next element in the list will be selected, enter a new value or press Enter with an empty field to skip that element.
7. Repeat steps 3 - 6 until the XEDS is populated.
8. Click File -> Export XML to save your XEDS.
9. Click File -> Export Bitstream to create a hex file of your XEDS.

##### Verifying a system
*note: this software is a work in progress. current verification will only recognize an "article" property (enum) inside a "subsystem" subXEDS.*

1. Select the "Check System" tab from the top of the window. 
2. Click the "Add Files" button and select XML XEDS. Repeat until all desired subsystems are represented.
3. Click the "Verify XEDS" button. The console will report the results.
