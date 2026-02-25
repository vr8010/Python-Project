"""
Digital Footprint Risk Analyzer
Main entry point for the application
"""
from risk_engine import RiskEngine
from report_manager import ReportManager
from utils import clear_screen, print_header, print_separator
import sys


def collect_user_input():
    """Collect user information for risk analysis"""
    print_header("DIGITAL FOOTPRINT RISK ANALYZER")
    print("Please provide the following information:\n")
    
    data = {}
    
    # Basic credentials
    data['email'] = input("Email address: ").strip()
    data['username'] = input("Username: ").strip()
    data['password'] = input("Password: ").strip()
    
    # Public information exposure
    print("\n--- Public Information Exposure ---")
    data['dob_public'] = input("Is your date of birth publicly visible? (yes/no): ").strip().lower() == 'yes'
    data['phone_public'] = input("Is your phone number publicly visible? (yes/no): ").strip().lower() == 'yes'
    data['address_public'] = input("Is your address publicly visible? (yes/no): ").strip().lower() == 'yes'
    data['email_public'] = input("Is your personal email publicly visible? (yes/no): ").strip().lower() == 'yes'
    
    # Behavior patterns
    print("\n--- Security Behavior ---")
    data['password_reuse'] = input("Do you reuse passwords across sites? (yes/no): ").strip().lower() == 'yes'
    data['clicks_unknown'] = input("Do you click on unknown links? (yes/no): ").strip().lower() == 'yes'
    data['public_wifi'] = input("Do you frequently use public WiFi? (yes/no): ").strip().lower() == 'yes'
    
    return data


def display_results(analysis):
    """Display the risk analysis results"""
    clear_screen()
    print_header("RISK ANALYSIS REPORT")
    print_separator()
    
    # Individual scores
    print(f" Password Risk:        {analysis['password_risk']}/25")
    print(f" Email Risk:           {analysis['email_risk']}/15")
    print(f" Username Risk:        {analysis['username_risk']}/15")
    print(f" Privacy Risk:         {analysis['privacy_risk']}/15")
    print(f" Behavior Risk:        {analysis['behavior_risk']}/10")
    print(f" Breach Simulation:    {analysis['breach_risk']}/20")
    
    print_separator()
    print(f" TOTAL DIGITAL RISK SCORE: {analysis['total_score']}/100")
    print(f" RISK LEVEL: {analysis['risk_level']} {analysis['risk_emoji']}")
    print_separator()
    
    # Recommendations
    if analysis['recommendations']:
        print("\n RECOMMENDATIONS:")
        for rec in analysis['recommendations']:
            print(f" - {rec}")
    
    print_separator()


def main_menu():
    """Display main menu and handle user choices"""
    report_mgr = ReportManager()
    
    while True:
        clear_screen()
        print_header("DIGITAL FOOTPRINT RISK ANALYZER")
        print("\n1. Analyze Digital Risk")
        print("2. View Previous Reports")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == '1':
            # Collect data and analyze
            user_data = collect_user_input()
            engine = RiskEngine(user_data)
            analysis = engine.analyze()
            
            # Display results
            display_results(analysis)
            
            # Save report
            report_mgr.save_report(analysis)
            print("\n✓ Report saved successfully!")
            
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # View previous reports
            clear_screen()
            report_mgr.display_reports()
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            print("\nThank you for using Digital Footprint Risk Analyzer!")
            sys.exit(0)
        else:
            print("\nInvalid option. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
