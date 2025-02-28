Overview  

This project is a web-based spreadsheet application designed to mimic the core functionalities and user interface of Google Sheets. It supports mathematical functions, data quality operations, cell formatting, drag-and-drop functionality, and more. The application is built with modern web technologies to ensure scalability, maintainability, and a smooth user experience. 
Tech Stack  

    Frontend : 
        HTML5 : For structuring the UI components.
        CSS3 : For styling the application to resemble Google Sheets' UI.
        JavaScript (Vanilla JS) : For implementing core functionalities like formula evaluation, cell dependency tracking, and UI interactions.
        Canvas API : Used for rendering the spreadsheet grid efficiently, ensuring performance even with large datasets.
         

    Backend  (Optional): 
        If extended to include persistence or advanced features, a backend could be implemented using Node.js  with Express.js  for API handling and MongoDB  or localStorage  for saving/loading spreadsheets.
         

    Libraries : 
        Math.js : For evaluating complex mathematical expressions and formulas.
        Natural Language Processing (NLP) : (Optional) For advanced formula parsing and error handling.
         

    Development Tools : 
        ES6+ : Modern JavaScript syntax for cleaner and more maintainable code.
        Linting : ESLint for enforcing coding standards.
        Testing : Manual testing and debugging tools for ensuring functionality.
         
     

Implementation Details  
1. Data Structures  

The application uses the following data structures to manage the spreadsheet state: 

    2D Array (spreadsheetData) : 
        A 2D array representing the grid of cells, where each cell stores its value (text, number, or formula result).
        Example: spreadsheetData[row][col] = "Hello".
         

    Cell Properties (cellProperties) : 
        A 2D array storing metadata for each cell, such as text alignment, font style, and color.
        Example: cellProperties[row][col] = { textAlign: "center", fontWeight: "bold" }.
         

    Formula Mapping (formulaInCell) : 
        A dictionary mapping cell names (e.g., "A1") to their corresponding formulas (e.g., "=SUM(A1:A10)").
        Example: formulaInCell["A1"] = "=A2+B2".
         

    Dependency Tracking (executionsDependentOnCell) : 
        A dictionary tracking which cells depend on others for recalculations when values change.
        Example: executionsDependentOnCell["A1"] = ["B1", "C1"].
         

    Row Heights and Column Widths : 
        Arrays (rowHeights, colWidths) to dynamically adjust row heights and column widths for better usability.
         
     

2. Core Functionalities  

    Spreadsheet Interface : 
        Implemented using the HTML <canvas> element for efficient rendering of the grid.
        Sticky headers for rows and columns to mimic Google Sheets' behavior.
        Drag-and-drop functionality for copying cell values and formulas.
         

    Mathematical Functions : 
        Implemented using Math.js  for evaluating formulas like SUM, AVERAGE, MAX, MIN, and COUNT.
        Example: =SUM(A1:A10) calculates the sum of values in the range A1 to A10.
         

    Data Quality Functions : 
        Functions like TRIM, UPPER, LOWER, REMOVE_DUPLICATES, and FIND_AND_REPLACE are implemented using JavaScript string manipulation methods.
        Example: =TRIM(A1) removes leading/trailing whitespace from the value in cell A1.
         

    Cell Dependencies : 
        Dependency tracking ensures that changes to a cell automatically update all dependent cells.
        Circular dependency detection prevents infinite loops during formula evaluation.
         

    Drag-and-Drop : 
        Implemented by tracking mouse events (mousedown, mousemove, mouseup) to allow users to drag and fill cells with values or formulas.
         

    Persistence : 
        Spreadsheets can be saved and loaded using localStorage for browser-based storage.
         
     

3. Key Algorithms  

    Formula Evaluation : 
        Formulas are parsed and evaluated using Math.js .
        Cell references (e.g., "A1") are replaced with their actual values before evaluation.
         

    Circular Dependency Detection : 
        Implemented using a recursive depth-first search (DFS) algorithm to detect cycles in cell dependencies.
         

    Range Parsing : 
        Ranges (e.g., "A1:B10") are parsed into start and end coordinates for iterating over cells.
         
     

4. User Interface  

    Toolbar : 
        Includes buttons for formatting options (bold, italic, alignment, etc.) and common actions (save, load).
         

    Formula Bar : 
        Allows users to enter and edit formulas directly.
         

    Grid Rendering : 
        Efficiently rendered using the Canvas API to handle large grids with minimal performance overhead.
         



2)   CDP Support Agent Chatbot

A chatbot designed to answer "how-to" questions related to Customer Data Platforms (CDPs) like Segment, mParticle, Lytics, and Zeotap. The chatbot extracts relevant information from official documentation to guide users on performing tasks or achieving specific outcomes within each platform.
Features

    How-to Questions: Answers user queries about specific tasks or features within CDPs.

    Documentation Extraction: Retrieves information from official CDP documentation.

    Cross-CDP Comparisons: Compares functionalities across different CDPs.

    Web Interface: Built with Flask for easy interaction.
