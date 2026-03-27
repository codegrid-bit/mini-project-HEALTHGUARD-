import os
import resend
import asyncio
from datetime import datetime
from typing import Dict

# Initialize Resend
resend.api_key = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')

async def send_email_async(to_email: str, subject: str, html_content: str) -> bool:
    """Send email asynchronously"""
    if not resend.api_key:
        print("⚠️ RESEND_API_KEY not configured - email not sent")
        return False
    
    params = {
        "from": SENDER_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    
    try:
        email = await asyncio.to_thread(resend.Emails.send, params)
        print(f"✅ Email sent to {to_email}: {email.get('id')}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def generate_welcome_email(user_name: str) -> str:
    """Generate welcome email HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #2A9D8F; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ background: #2A9D8F; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to HealthGuard AI</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>Thank you for joining HealthGuard AI - your partner in preventive health management.</p>
                <p>We're here to help you understand your diabetes and cholesterol risk through our AI-powered assessment system.</p>
                <p><strong>What's Next:</strong></p>
                <ul>
                    <li>Take our 25-question health quiz (5 minutes)</li>
                    <li>Get your personalized risk assessment</li>
                    <li>Receive tailored health recommendations</li>
                    <li>Track your progress over time</li>
                </ul>
                <p><strong>Important Disclaimer:</strong> HealthGuard AI is an informational tool only. It does not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.</p>
                <a href="#" class="button">Start Your Assessment</a>
            </div>
        </div>
    </body>
    </html>
    """

def generate_assessment_results_email(user_name: str, risk_level: str, diabetes_score: int, cholesterol_score: int) -> str:
    """Generate assessment results email"""
    risk_colors = {
        "Low": "#10b981",
        "Medium": "#f59e0b",
        "High": "#ef4444"
    }
    color = risk_colors.get(risk_level, "#6b7280")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #2A9D8F; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .risk-badge {{ background: {color}; color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block; }}
            .score-box {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2A9D8F; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Health Assessment Results</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>Your health assessment is complete. Here are your results:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span class="risk-badge">{risk_level} Risk</span>
                </div>
                <div class="score-box">
                    <strong>Diabetes Risk Score:</strong> {diabetes_score}%
                </div>
                <div class="score-box">
                    <strong>Cholesterol Risk Score:</strong> {cholesterol_score}%
                </div>
                <p><strong>Next Steps:</strong></p>
                {"<p>⚠️ We recommend getting blood tests done (LDL, HDL, Triglycerides, HbA1c) and consulting with a healthcare provider.</p>" if risk_level != "Low" else "<p>✅ Maintain your healthy lifestyle with regular exercise and balanced diet.</p>"}
                <p><em>Disclaimer: These results are for informational purposes only and should not be considered medical advice.</em></p>
            </div>
        </div>
    </body>
    </html>
    """

def generate_reminder_email(user_name: str, reminder_type: str = "blood_test") -> str:
    """Generate reminder email"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #E76F51; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .alert-box {{ background: #fff3cd; border-left: 4px solid #E76F51; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔔 Health Reminder</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <div class="alert-box">
                    <strong>It's time for your follow-up blood test!</strong>
                </div>
                <p>Based on your previous health assessment, we recommend getting your blood work done again to track your progress.</p>
                <p><strong>Recommended Tests:</strong></p>
                <ul>
                    <li>LDL Cholesterol (Bad cholesterol)</li>
                    <li>HDL Cholesterol (Good cholesterol)</li>
                    <li>Triglycerides</li>
                    <li>HbA1c (3-month blood sugar average)</li>
                </ul>
                <p>After getting your tests, log in to HealthGuard AI to upload your results for comprehensive analysis.</p>
                <p><em>Regular monitoring helps detect changes early and allows for timely interventions.</em></p>
            </div>
        </div>
    </body>
    </html>
    """

def generate_doctor_referral_email(user_name: str, blood_test_results: Dict) -> str:
    """Generate doctor referral email"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #ef4444; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .urgent {{ background: #fee2e2; border: 2px solid #ef4444; padding: 20px; margin: 20px 0; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Urgent: Doctor Consultation Recommended</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <div class="urgent">
                    <strong>Your recent blood test results indicate values that require medical attention.</strong>
                </div>
                <p>We strongly recommend scheduling an appointment with a healthcare provider as soon as possible to discuss your results and create a treatment plan.</p>
                <p><strong>Your Results:</strong></p>
                <ul>
                    <li>LDL: {blood_test_results.get('ldl', 'N/A')} mg/dL</li>
                    <li>HDL: {blood_test_results.get('hdl', 'N/A')} mg/dL</li>
                    <li>Triglycerides: {blood_test_results.get('triglycerides', 'N/A')} mg/dL</li>
                    <li>HbA1c: {blood_test_results.get('hba1c', 'N/A')}%</li>
                </ul>
                <p><strong>Important:</strong> This is not a diagnosis. Only a qualified healthcare provider can interpret your results in the context of your complete medical history.</p>
            </div>
        </div>
    </body>
    </html>
    """
