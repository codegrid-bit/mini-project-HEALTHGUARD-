import smtplib
import asyncio
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

async def send_email_async(to_email: str, subject: str, html_content: str) -> bool:
    """Send email asynchronously via Gmail SMTP"""
    GMAIL_USER = os.environ.get('GMAIL_USER', '')
    GMAIL_APP_PASS = os.environ.get('GMAIL_APP_PASS', '')

    if not GMAIL_USER or not GMAIL_APP_PASS:
        print("⚠️ GMAIL_USER or GMAIL_APP_PASS not configured - email not sent")
        return False

    print(f"📧 Attempting email to {to_email} | subject: {subject}")

    def _send():
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"HealthGuard AI <{GMAIL_USER}>"
        msg['To'] = to_email
        msg.attach(MIMEText(html_content, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASS)
            smtp.sendmail(GMAIL_USER, to_email, msg.as_string())

    try:
        await asyncio.to_thread(_send)
        print(f"✅ Email sent to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail auth failed - check GMAIL_USER and GMAIL_APP_PASS in .env")
        return False
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False


def generate_welcome_email(user_name: str) -> str:
    """Generate welcome email HTML"""
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')  # ✅ FIXED
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
                <a href="{frontend_url}/assessment" class="button">Start Your Assessment</a>
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


def generate_doctor_referral_email(user_name: str, blood_test_results: Dict, risk_level: str = "High") -> str:
    ldl = blood_test_results.get('ldl', 'N/A')
    hdl = blood_test_results.get('hdl', 'N/A')
    triglycerides = blood_test_results.get('triglycerides', 'N/A')
    hba1c = blood_test_results.get('hba1c', 'N/A')

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
      <div style="max-width:600px; margin:0 auto; padding:20px;">
        <div style="background:#ef4444; color:white; padding:30px; text-align:center; border-radius:8px 8px 0 0;">
          <h1>⚠️ Doctor Consultation Recommended</h1>
        </div>
        <div style="background:#f8f9fa; padding:30px;">
          <p>Hi {user_name},</p>
          <div style="text-align:center; margin:20px 0;">
            <span style="background:#ef4444; color:white; padding:10px 24px; border-radius:20px; font-weight:bold; font-size:16px;">
              {risk_level} Risk
            </span>
          </div>
          <div style="background:#fee2e2; border:2px solid #ef4444; padding:20px; margin:20px 0; border-radius:8px;">
            <strong>Your blood test results indicate values that require medical attention.</strong>
          </div>
          <p>We strongly recommend scheduling an appointment with a healthcare provider as soon as possible.</p>
          <p><strong>Your Results:</strong></p>
          <ul>
            <li>LDL: {ldl} mg/dL</li>
            <li>HDL: {hdl} mg/dL</li>
            <li>Triglycerides: {triglycerides} mg/dL</li>
            <li>HbA1c: {hba1c}%</li>
          </ul>
          <p><em>This is not a diagnosis. Only a qualified healthcare provider can interpret your results.</em></p>
        </div>
      </div>
    </body>
    </html>
    """