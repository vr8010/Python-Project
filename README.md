# Digital Footprint Risk Analyzer

A console-based Python application that analyzes digital habits and calculates a Digital Risk Score (0-100) based on multiple exposure factors.
## Project Architecture

## 📊 Flowchart

![Flowchart](flowchart.png)

## Features

- **Password Risk Analysis** (0-25 points): Evaluates password strength
- **Email Risk Analysis** (0-15 points): Checks for predictable patterns
- **Username Exposure Risk** (0-15 points): Identifies risky username patterns
- **Privacy Exposure Risk** (0-15 points): Assesses public information sharing
- **Behavior Risk** (0-10 points): Evaluates security habits
- **Breach Simulation** (0-20 points): Simulates potential breach risk

## Risk Classification

- **0-30**: Low Risk ✅
- **31-60**: Moderate Risk ⚠️
- **61-100**: High Risk 🚨

## Installation

No external libraries required! Just Python 3.x

## Usage

Run the application:

```bash
python main.py
```

### Menu Options

1. **Analyze Digital Risk**: Perform a new risk analysis
2. **View Previous Reports**: Display all saved reports
3. **Exit**: Close the application

## File Structure

- `main.py` - Main entry point and menu system
- `risk_engine.py` - Core risk analysis logic (OOP-based)
- `report_manager.py` - Report saving and retrieval
- `utils.py` - UI utility functions
- `reports.txt` - Stored analysis reports (auto-generated)

## Example Output

```
--------------------------------------------------
 Password Risk:        14/25
 Email Risk:           8/15
 Username Risk:        10/15
 Privacy Risk:         7/15
 Behavior Risk:        6/10
 Breach Simulation:    15/20
--------------------------------------------------
 TOTAL DIGITAL RISK SCORE: 60/100
 RISK LEVEL: MODERATE ⚠️
--------------------------------------------------

 RECOMMENDATIONS:
 - Increase password complexity
 - Avoid password reuse
 - Remove birth year from username
```

## Technical Details

- Pure Python implementation (no external dependencies)
- Object-Oriented design for Risk Engine
- File handling for persistent storage
- Input validation and error handling
- Clean console UI with formatting
