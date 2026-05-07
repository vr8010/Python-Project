"""
Flask web server for Digital Footprint Risk Analyzer
"""
from flask import Flask, request, jsonify, render_template
from risk_engine import RiskEngine
from report_manager import ReportManager

app = Flask(__name__, template_folder='frontend', static_folder='frontend/static')
report_mgr = ReportManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    engine = RiskEngine(data)
    analysis = engine.analyze()
    report_mgr.save_report(analysis)
    return jsonify(analysis)

@app.route('/api/reports', methods=['GET'])
def get_reports():
    return jsonify(report_mgr.get_reports_list())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
