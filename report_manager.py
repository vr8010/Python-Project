"""
Report Manager - Handles saving and viewing reports
"""
from datetime import datetime
import os

class ReportManager:
    """Manages report storage and retrieval"""
    
    def __init__(self, filename='reports.txt'):
        self.filename = filename
    
    def save_report(self, analysis):
        """Save analysis report to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_text = f"""
{'='*50}
DIGITAL FOOTPRINT RISK ANALYSIS REPORT
Timestamp: {timestamp}
{'='*50}

RISK BREAKDOWN:
 Password Risk:        {analysis['password_risk']}/25
 Email Risk:           {analysis['email_risk']}/15
 Username Risk:        {analysis['username_risk']}/15
 Privacy Risk:         {analysis['privacy_risk']}/15
 Behavior Risk:        {analysis['behavior_risk']}/10
 Breach Simulation:    {analysis['breach_risk']}/20

TOTAL DIGITAL RISK SCORE: {analysis['total_score']}/100
RISK LEVEL: {analysis['risk_level']} {analysis['risk_emoji']}

RECOMMENDATIONS:
"""
        
        for rec in analysis['recommendations']:
            report_text += f" - {rec}\n"
        
        report_text += f"\n{'='*50}\n\n"
        
        # Append to file
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(report_text)
    
    def get_reports_list(self):
        """Return reports as a list of dicts for the API"""
        if not os.path.exists(self.filename):
            return []
        reports = []
        current = {}
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('Timestamp:'):
                    current['timestamp'] = line.replace('Timestamp:', '').strip()
                elif 'Password Risk:' in line:
                    current['password_risk'] = line.split(':')[1].strip()
                elif 'Email Risk:' in line:
                    current['email_risk'] = line.split(':')[1].strip()
                elif 'Username Risk:' in line:
                    current['username_risk'] = line.split(':')[1].strip()
                elif 'Privacy Risk:' in line:
                    current['privacy_risk'] = line.split(':')[1].strip()
                elif 'Behavior Risk:' in line:
                    current['behavior_risk'] = line.split(':')[1].strip()
                elif 'Breach Simulation:' in line:
                    current['breach_risk'] = line.split(':')[1].strip()
                elif 'TOTAL DIGITAL RISK SCORE:' in line:
                    current['total_score'] = line.split(':')[1].strip()
                elif 'RISK LEVEL:' in line:
                    current['risk_level'] = line.split(':')[1].strip()
                elif line.startswith('- '):
                    current.setdefault('recommendations', []).append(line[2:])
                elif line.startswith('=' * 10) and current.get('timestamp'):
                    reports.append(current)
                    current = {}
        return list(reversed(reports))

    def display_reports(self):
        """Display all previous reports"""
        if not os.path.exists(self.filename):
            print("\nNo previous reports found.")
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    print(content)
                else:
                    print("\nNo previous reports found.")
        except Exception as e:
            print(f"\nError reading reports: {e}")


#https://github.com/vr8010/Python-Project/edit/main/report_manager.py
