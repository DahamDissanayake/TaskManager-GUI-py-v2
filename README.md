# TaskManager-GUI-py-v2
A desktop-based task management app built using Python, featuring a simple command-line interface. Tasks can be added, viewed, updated, and deleted directly from the terminal. All task data is stored in a local text file, ensuring persistence across sessions. Ideal for users seeking a lightweight and efficient tool for managing personal tasks.

# Personal Task Manager GUI

A modern, user-friendly task management application built with Python and Tkinter, featuring a graphical interface with advanced filtering, sorting, and task management capabilities.

## Author
**Daham Dissanayake**  
*Date: April 20, 2025*  
*Student ID: w2152911*

## Features

### Core Functionality
- **Intuitive GUI**: Clean, modern interface built with Tkinter
- **Add Tasks**: Create new tasks with comprehensive details
- **Edit Tasks**: Modify existing task information
- **Delete Tasks**: Remove tasks with confirmation dialogs
- **Persistent Storage**: JSON-based data storage for reliability

### Advanced Features
- **Search & Filter**: Filter tasks by name, priority, or due date
- **Multi-Column Sorting**: Sort by name, priority, or due date (ascending/descending)
- **Column Headers**: Click column headers for quick sorting
- **Data Validation**: Comprehensive input validation and error handling
- **Responsive Design**: Resizable window with proper layout management

### Task Properties
- **Name**: Brief task title
- **Description**: Detailed task information
- **Priority**: High, Medium, or Low priority levels
- **Due Date**: YYYY-MM-DD format with validation

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- json (built-in Python module)
- datetime (built-in Python module)

## Installation

1. Ensure Python 3.x is installed on your system
2. Download the `S4_Task_Manager_GUI_w2152911.py` file
3. No additional dependencies required - uses only Python standard library

## Usage

### Starting the Application

```bash
python S4_Task_Manager_GUI_w2152911.py
```

### Main Interface

The application opens with a comprehensive interface featuring:

- **Search and Filter Panel**: Located at the top for easy access
- **Task Table**: Central display showing all tasks in a sortable table
- **Control Buttons**: Add, Edit, and Delete task buttons
- **Sort Options**: Quick sort buttons for different criteria

### Adding a New Task

1. Click the "Add New Task" button
2. Fill in the task details in the popup dialog:
   - **Task Name**: Enter a descriptive name (required)
   - **Description**: Add detailed information about the task
   - **Priority**: Select from High, Medium, or Low (defaults to Medium)
   - **Due Date**: Enter in YYYY-MM-DD format
3. Click "Add Task" to save or "Cancel" to abort

### Editing Tasks

1. Select a task from the table by clicking on it
2. Click the "Edit Task" button
3. Modify the task details in the popup dialog
4. Click "Update Task" to save changes or "Cancel" to abort

### Deleting Tasks

1. Select a task from the table
2. Click the "Delete Task" button
3. Confirm deletion in the popup dialog

### Filtering Tasks

Use the filter panel to narrow down your task list:

- **Filter by Name**: Enter partial or complete task names
- **Filter by Priority**: Select All, High, Medium, or Low
- **Filter by Due Date**: Enter specific date in YYYY-MM-DD format
- Click "Apply Filters" to update the display
- Click "Reset Filters" to clear all filters

### Sorting Tasks

Multiple sorting options available:

- **Column Headers**: Click any column header to sort by that field
- **Sort Buttons**: Use dedicated sort buttons for quick access
- **Toggle Order**: Click the same column/button again to reverse order

## File Structure

```
├── S4_Task_Manager_GUI_w2152911.py    # Main application file
└── tasks.json                         # Auto-generated task storage file
```

## Data Storage

Tasks are stored in JSON format in `tasks.json`:

```json
[
  {
    "name": "Complete Project",
    "description": "Finish the GUI task manager",
    "priority": "high",
    "due_date": "2025-05-01"
  }
]
```

### Storage Features
- **Automatic Saving**: Tasks are saved immediately after any changes
- **JSON Format**: Human-readable and easily portable
- **Error Recovery**: Graceful handling of corrupted or missing files

## Architecture

### Class Structure

**Task Class**
- Represents individual tasks
- Handles serialization to/from dictionaries
- Manages task properties

**TaskManager Class**
- Handles all task operations (CRUD)
- Manages file I/O operations
- Provides filtering and sorting functionality

**TaskManagerGUI Class**
- Creates and manages the Tkinter interface
- Handles user interactions and events
- Coordinates between GUI and TaskManager

### Key Design Patterns
- **MVC Architecture**: Clear separation between data, logic, and presentation
- **Object-Oriented Design**: Modular, maintainable code structure
- **Event-Driven Programming**: Responsive GUI interactions

## Validation & Error Handling

### Input Validation
- **Task Names**: Cannot be empty
- **Date Format**: Strict YYYY-MM-DD validation
- **Date Logic**: Validates actual calendar dates including leap years
- **Priority Levels**: Restricted to predefined options

### Error Recovery
- **File Not Found**: Creates new task list if storage file missing
- **JSON Corruption**: Recovers gracefully from invalid JSON
- **Invalid Selections**: User-friendly messages for improper operations

## Advanced Features

### Smart Filtering
- **Partial Matching**: Name filters work with partial text
- **Case Insensitive**: Flexible text matching
- **Multiple Criteria**: Combine different filter types

### Intelligent Sorting
- **Priority Logic**: Custom sort order (High → Medium → Low)
- **Date Sorting**: Chronological ordering with proper date parsing
- **Memory**: Remembers last sort column and direction

### User Experience
- **Modal Dialogs**: Focused task editing experience
- **Confirmation Prompts**: Prevents accidental deletions
- **Responsive Layout**: Adapts to window resizing
- **Keyboard Navigation**: Standard Tkinter keyboard shortcuts

## Troubleshooting

### Common Issues

**Application Won't Start**
- Ensure Python 3.x is installed
- Check that tkinter is available (usually included with Python)

**Tasks Don't Save**
- Verify write permissions in the application directory
- Check for disk space availability

**Date Validation Errors**
- Use exact YYYY-MM-DD format (e.g., 2025-05-01)
- Ensure dates are valid calendar dates
- Year must be between 1900-2100

## Performance Notes

- **Efficient Filtering**: In-memory operations for fast response
- **Minimal File I/O**: Only saves when tasks are modified
- **Lightweight Storage**: JSON format keeps file sizes small
- **Responsive UI**: Non-blocking operations for smooth interaction

## Future Enhancements

Potential improvements for future versions:

- **Task Categories**: Organize tasks by categories or projects
- **Due Date Reminders**: Notifications for approaching deadlines
- **Task Status**: Track completion status and progress
- **Export Options**: Export tasks to CSV, PDF, or other formats
- **Dark Theme**: Alternative UI theme options
- **Keyboard Shortcuts**: Custom hotkeys for common operations
- **Task Dependencies**: Link related tasks together
- **Calendar Integration**: Visual calendar view of due dates

## Compatibility

- **Python Versions**: 3.6+
- **Operating Systems**: Windows, macOS, Linux
- **Dependencies**: Python standard library only

## License

This project is open source and available for educational and personal use.

## Support

For questions, issues, or contributions:
- Review the code comments for detailed implementation notes
- Check the validation methods for input requirements
- Refer to the error messages for troubleshooting guidance

---

*This GUI version represents a significant upgrade from the command-line interface, providing a modern, user-friendly experience while maintaining all core functionality.*