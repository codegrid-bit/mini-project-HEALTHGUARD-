from fastapi import FastAPI, APIRouter, Response, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from motor.motor_asyncio import AsyncIOMotorClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import logging
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
from quiz_questions import get_all_questions, calculate_quiz_score
from ml_predictor_enhanced import enhanced_predictor
from email_service import (
    send_email_async,
    generate_welcome_email,
    generate_assessment_results_email,
    generate_reminder_email,
    generate_doctor_referral_email
)
from pdf_generator import generate_health_report_pdf
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(
    mongo_url,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client[os.environ['DB_NAME']]

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

security = HTTPBearer()
scheduler = AsyncIOScheduler()

app = FastAPI(title="HealthGuard AI - Medical Grade API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int
    sex: str = "male"
    consent_privacy: bool = True
    consent_terms: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    age: int
    sex: str
    ethnicity: Optional[str] = None
    medications: Optional[List[str]] = None
    consent_privacy: bool = True
    consent_terms: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizSubmission(BaseModel):
    answers: Dict[str, bool]
    user_info: Optional[Dict[str, Any]] = None

class BloodTestData(BaseModel):
    ldl: float = Field(..., ge=0, le=500)
    hdl: float = Field(..., ge=0, le=200)
    triglycerides: float = Field(..., ge=0, le=1000)
    hba1c: float = Field(..., ge=0, le=20)
    glucose: Optional[float] = Field(None, ge=0, le=600)
    blood_pressure: Optional[float] = Field(None, ge=0, le=300)

class BloodTestSubmission(BaseModel):
    assessment_id: str
    blood_test: BloodTestData

class HealthAssessment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quiz_answers: Dict[str, bool]
    total_score: int
    diabetes_score: int
    cholesterol_score: int
    risk_level: str
    ml_version: str = "v2_enhanced"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BloodTest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    user_id: str
    ldl: float
    hdl: float
    triglycerides: float
    hba1c: float
    glucose: Optional[float] = None
    blood_pressure: Optional[float] = None
    analysis: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Reminder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    assessment_id: str
    reminder_type: str = "blood_test"
    due_date: datetime
    status: str = "pending"
    email_sent: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AuditLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    action: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== HELPER FUNCTIONS ====================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def log_audit(user_id: str, action: str, details: Dict[str, Any], ip_address: Optional[str] = None):
    audit_log = AuditLog(user_id=user_id, action=action, details=details, ip_address=ip_address)
    audit_dict = audit_log.model_dump()
    audit_dict['timestamp'] = audit_dict['timestamp'].isoformat()
    await db.audit_logs.insert_one(audit_dict)

def get_age_sex_adjusted_thresholds(age: int, sex: str) -> Dict[str, Any]:
    thresholds = {
        'ldl_optimal': 100, 'ldl_borderline': 130, 'ldl_high': 160, 'ldl_very_high': 190,
        'hdl_low_male': 40, 'hdl_low_female': 50, 'hdl_optimal': 60,
        'triglycerides_normal': 150, 'triglycerides_borderline': 200, 'triglycerides_high': 500,
        'hba1c_normal': 5.7, 'hba1c_prediabetes': 6.5,
    }
    if age > 65:
        thresholds['ldl_optimal'] = 110
        thresholds['ldl_borderline'] = 140
    thresholds['hdl_low'] = thresholds['hdl_low_male'] if sex == 'male' else thresholds['hdl_low_female']
    return thresholds

def analyze_blood_test_advanced(blood_test: BloodTestData, age: int, sex: str) -> Dict[str, Any]:
    thresholds = get_age_sex_adjusted_thresholds(age, sex)
    analysis = {
        "diabetes_risk": "Normal", "cholesterol_risk": "Normal",
        "recommendations": [], "requires_doctor": False, "detailed_analysis": {}
    }
    if blood_test.hba1c >= thresholds['hba1c_prediabetes']:
        analysis["diabetes_risk"] = "High - Diabetic Range"
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("⚠️ URGENT: Immediate doctor consultation required")
        analysis["detailed_analysis"]["hba1c"] = "Diabetic range - requires medical intervention"
    elif blood_test.hba1c >= thresholds['hba1c_normal']:
        analysis["diabetes_risk"] = "Medium - Pre-diabetic"
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("Consult doctor about pre-diabetes management")
        analysis["detailed_analysis"]["hba1c"] = "Pre-diabetic - lifestyle changes recommended"
    else:
        analysis["detailed_analysis"]["hba1c"] = "Normal range"
    if blood_test.ldl >= thresholds['ldl_very_high']:
        analysis["cholesterol_risk"] = "Very High"
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("⚠️ URGENT: Very high LDL requires immediate medical attention")
        analysis["detailed_analysis"]["ldl"] = f"Very high ({blood_test.ldl} mg/dL)"
    elif blood_test.ldl >= thresholds['ldl_high']:
        analysis["cholesterol_risk"] = "High"
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("Elevated LDL - doctor consultation recommended")
        analysis["detailed_analysis"]["ldl"] = f"High ({blood_test.ldl} mg/dL)"
    elif blood_test.ldl >= thresholds['ldl_borderline']:
        analysis["cholesterol_risk"] = "Borderline High"
        analysis["recommendations"].append("Monitor LDL levels and improve diet")
        analysis["detailed_analysis"]["ldl"] = f"Borderline high ({blood_test.ldl} mg/dL)"
    else:
        analysis["detailed_analysis"]["ldl"] = f"Optimal ({blood_test.ldl} mg/dL)"
    if blood_test.hdl < thresholds['hdl_low']:
        analysis["cholesterol_risk"] = "High" if analysis["cholesterol_risk"] == "Normal" else analysis["cholesterol_risk"]
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("Low HDL increases heart disease risk - consult doctor")
        analysis["detailed_analysis"]["hdl"] = f"Low ({blood_test.hdl} mg/dL)"
    elif blood_test.hdl >= thresholds['hdl_optimal']:
        analysis["detailed_analysis"]["hdl"] = f"Excellent ({blood_test.hdl} mg/dL)"
    else:
        analysis["detailed_analysis"]["hdl"] = f"Acceptable ({blood_test.hdl} mg/dL)"
    if blood_test.triglycerides >= thresholds['triglycerides_high']:
        analysis["cholesterol_risk"] = "Very High"
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("⚠️ CRITICAL: Extremely high triglycerides - urgent medical care needed")
        analysis["detailed_analysis"]["triglycerides"] = f"Dangerously high ({blood_test.triglycerides} mg/dL)"
    elif blood_test.triglycerides >= thresholds['triglycerides_borderline']:
        analysis["cholesterol_risk"] = "High" if analysis["cholesterol_risk"] in ["Normal", "Borderline High"] else analysis["cholesterol_risk"]
        analysis["requires_doctor"] = True
        analysis["recommendations"].append("High triglycerides require medical attention")
        analysis["detailed_analysis"]["triglycerides"] = f"High ({blood_test.triglycerides} mg/dL)"
    elif blood_test.triglycerides >= thresholds['triglycerides_normal']:
        analysis["recommendations"].append("Borderline high triglycerides - reduce sugar and alcohol intake")
        analysis["detailed_analysis"]["triglycerides"] = f"Borderline ({blood_test.triglycerides} mg/dL)"
    else:
        analysis["detailed_analysis"]["triglycerides"] = f"Normal ({blood_test.triglycerides} mg/dL)"
    return analysis

def get_lifestyle_recommendations(risk_level: str, diabetes_score: int, cholesterol_score: int) -> List[str]:
    recommendations = []
    if risk_level == "Low":
        recommendations = [
            "✅ Maintain a balanced Mediterranean-style diet",
            "✅ Include 25-30g of fiber daily",
            "✅ Limit saturated fats to <7% of daily calories",
            "✅ Engage in 150 minutes of moderate-intensity aerobic exercise weekly",
            "✅ Maintain a healthy BMI (18.5-24.9)",
            "✅ Stay hydrated with 6-8 glasses of water daily",
            "✅ Get 7-9 hours of quality sleep each night",
            "✅ Schedule annual health screenings and blood tests"
        ]
    else:
        if diabetes_score > 30:
            recommendations.extend([
                "🔸 Limit added sugars to <25g per day",
                "🔸 Choose low glycemic index foods",
                "🔸 Monitor portion sizes using the plate method",
                "🔸 Eat smaller, frequent meals to maintain stable blood sugar",
            ])
        if cholesterol_score > 30:
            recommendations.extend([
                "🔸 Increase omega-3 fatty acids (salmon, sardines, walnuts)",
                "🔸 Choose lean proteins (skinless poultry, fish, legumes)",
                "🔸 Use heart-healthy oils (olive, avocado, canola) instead of butter",
            ])
        recommendations.extend([
            "🔸 Engage in 30-60 minutes of cardiovascular exercise 5 days per week",
            "🔸 Quit smoking immediately",
            "🔸 Limit alcohol to ≤1 drink/day for women, ≤2 drinks/day for men",
            "🔸 Reduce sodium intake to <2300mg/day",
            "🔸 Monitor blood pressure regularly at home",
        ])
        if risk_level in ["Medium", "High"]:
            recommendations.insert(0, "⚠️ GET COMPREHENSIVE BLOOD TESTS: LDL, HDL, Triglycerides, HbA1c")
            if risk_level == "High":
                recommendations.insert(0, "🚨 URGENT: Consult with a healthcare provider within 1 week")
    return recommendations

# ==================== SCHEDULER TASK ====================

async def send_due_reminders():
    """Check for due reminders every minute and send emails"""
    try:
        now = datetime.now(timezone.utc).isoformat()
        due_reminders = await db.reminders.find(
            {"status": "pending", "email_sent": False, "due_date": {"$lte": now}},
            {"_id": 0}
        ).to_list(100)

        for reminder in due_reminders:
            user = await db.users.find_one({"id": reminder['user_id']}, {"_id": 0})
            if user:
                await send_email_async(
                    user['email'],
                    "⏰ HealthGuard AI - Time for Your Next Blood Test!",
                    generate_reminder_email(user['name'])
                )
                await db.reminders.update_one(
                    {"id": reminder['id']},
                    {"$set": {"email_sent": True, "status": "completed"}}
                )
                logger.info(f"✅ Reminder email sent to {user['email']}")
    except Exception as e:
        logger.error(f"❌ Reminder scheduler error: {str(e)}")

# ==================== AUTHENTICATION ROUTES ====================

@api_router.post("/auth/register")
async def register(user_data: UserRegister, background_tasks: BackgroundTasks):
    try:
        logger.info(f"📝 Registration attempt for: {user_data.email}")
        if not user_data.consent_privacy or not user_data.consent_terms:
            raise HTTPException(status_code=400, detail="Must accept privacy policy and terms of service")
        existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            name=user_data.name,
            email=user_data.email,
            age=user_data.age,
            sex=user_data.sex,
            consent_privacy=user_data.consent_privacy,
            consent_terms=user_data.consent_terms
        )
        user_dict = user.model_dump()
        user_dict['password'] = hash_password(user_data.password)
        user_dict['created_at'] = user_dict['created_at'].isoformat()
        await db.users.insert_one(user_dict)
        logger.info(f"✅ User saved to DB: {user_data.email}")
        await log_audit(user.id, "user_registered", {"email": user.email})
        background_tasks.add_task(
            send_email_async,
            user.email,
            "Welcome to HealthGuard AI",
            generate_welcome_email(user.name)
        )
        access_token = create_access_token({"sub": user.id})
        user_response = user.model_dump()
        user_response.pop('consent_privacy', None)
        user_response.pop('consent_terms', None)
        logger.info(f"✅ Registration successful: {user_data.email}")
        return {
            "user": user_response,
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user or not verify_password(credentials.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    await log_audit(user['id'], "user_login", {"email": user['email']})
    access_token = create_access_token({"sub": user['id']})
    user.pop('password', None)
    return {"user": user, "access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    current_user.pop('password', None)
    return current_user

# ==================== QUIZ ROUTES ====================

@api_router.get("/quiz/questions")
async def get_quiz_questions():
    return {"questions": get_all_questions()}

@api_router.post("/quiz/submit")
async def submit_quiz(submission: QuizSubmission, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    score_result = calculate_quiz_score(submission.answers)
    user_info = {
        'age': current_user.get('age', 30),
        'sex': current_user.get('sex', 'male'),
        'ethnicity': current_user.get('ethnicity', 'unknown')
    }
    try:
        ml_prediction = enhanced_predictor.predict_from_quiz(submission.answers, user_info)
        score_result.update(ml_prediction)
    except Exception as e:
        print(f"ML prediction failed, using basic scoring: {e}")
    assessment = HealthAssessment(
        user_id=current_user['id'],
        quiz_answers=submission.answers,
        total_score=score_result['total_score'],
        diabetes_score=score_result['diabetes_score'],
        cholesterol_score=score_result['cholesterol_score'],
        risk_level=score_result['risk_level'],
        ml_version=score_result.get('model_version', 'v1')
    )
    assessment_dict = assessment.model_dump()
    assessment_dict['created_at'] = assessment_dict['created_at'].isoformat()
    await db.assessments.insert_one(assessment_dict)
    await log_audit(current_user['id'], "quiz_submitted", {"risk_level": score_result['risk_level']})
    recommendations = get_lifestyle_recommendations(
        score_result['risk_level'], score_result['diabetes_score'], score_result['cholesterol_score']
    )
    if score_result['risk_level'] in ["Medium", "High"]:
        reminder = Reminder(
            user_id=current_user['id'],
            assessment_id=assessment.id,
            due_date=datetime.now(timezone.utc) + timedelta(days=60)
        )
        reminder_dict = reminder.model_dump()
        reminder_dict['due_date'] = reminder_dict['due_date'].isoformat()
        reminder_dict['created_at'] = reminder_dict['created_at'].isoformat()
        await db.reminders.insert_one(reminder_dict)
    background_tasks.add_task(
        send_email_async,
        current_user['email'],
        f"HealthGuard AI Assessment Results - {score_result['risk_level']} Risk",
        generate_assessment_results_email(
            current_user['name'], score_result['risk_level'],
            score_result['diabetes_score'], score_result['cholesterol_score']
        )
    )
    return {
        "assessment": assessment.model_dump(),
        "score_result": score_result,
        "recommendations": recommendations,
        "requires_blood_test": score_result['risk_level'] in ["Medium", "High"]
    }

# ==================== BLOOD TEST ROUTES ====================

@api_router.post("/blood-test/submit")
async def submit_blood_test(submission: BloodTestSubmission, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    assessment = await db.assessments.find_one(
        {"id": submission.assessment_id, "user_id": current_user['id']}, {"_id": 0}
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    analysis = analyze_blood_test_advanced(
        submission.blood_test, current_user.get('age', 30), current_user.get('sex', 'male')
    )
    blood_test = BloodTest(
        assessment_id=submission.assessment_id, user_id=current_user['id'],
        ldl=submission.blood_test.ldl, hdl=submission.blood_test.hdl,
        triglycerides=submission.blood_test.triglycerides, hba1c=submission.blood_test.hba1c,
        glucose=submission.blood_test.glucose, blood_pressure=submission.blood_test.blood_pressure,
        analysis=analysis
    )
    blood_test_dict = blood_test.model_dump()
    blood_test_dict['created_at'] = blood_test_dict['created_at'].isoformat()
    await db.blood_tests.insert_one(blood_test_dict)
    await log_audit(current_user['id'], "blood_test_uploaded", {
        "requires_doctor": analysis['requires_doctor'],
        "diabetes_risk": analysis['diabetes_risk'],
        "cholesterol_risk": analysis['cholesterol_risk']
    })

    # ⏰ Reminder set to 2 minutes for demo — change timedelta(minutes=2) to timedelta(days=90) for production
    reminder = Reminder(
        user_id=current_user['id'], assessment_id=submission.assessment_id,
        due_date=datetime.now(timezone.utc) + timedelta(minutes=2)
    )
    reminder_dict = reminder.model_dump()
    reminder_dict['due_date'] = reminder_dict['due_date'].isoformat()
    reminder_dict['created_at'] = reminder_dict['created_at'].isoformat()
    await db.reminders.insert_one(reminder_dict)
    logger.info(f"⏰ Reminder scheduled for {reminder_dict['due_date']}")

    email_data = {
        "ldl": submission.blood_test.ldl,
        "hdl": submission.blood_test.hdl,
        "triglycerides": submission.blood_test.triglycerides,
        "hba1c": submission.blood_test.hba1c
    }
    if analysis['requires_doctor']:
        email_content = generate_doctor_referral_email(
            current_user['name'],
            email_data,
            analysis.get('cholesterol_risk', 'High')
        )
        subject = "⚠️ HealthGuard AI - Doctor Consultation Recommended"
    else:
        email_content = generate_assessment_results_email(
            user_name=current_user['name'],
            risk_level="Low",
            diabetes_score=0,
            cholesterol_score=0
        )
        subject = "Your HealthGuard AI Blood Test Results"
    background_tasks.add_task(send_email_async, current_user['email'], subject, email_content)
    return {
        "blood_test": blood_test.model_dump(),
        "analysis": analysis,
        "next_test_date": reminder_dict['due_date']
    }

# ==================== HISTORY & REPORTS ====================

@api_router.get("/history/assessments")
async def get_assessments(current_user: dict = Depends(get_current_user)):
    assessments = await db.assessments.find(
        {"user_id": current_user['id']}, {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    return {"assessments": assessments}

@api_router.get("/history/blood-tests")
async def get_blood_tests(current_user: dict = Depends(get_current_user)):
    blood_tests = await db.blood_tests.find(
        {"user_id": current_user['id']}, {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    return {"blood_tests": blood_tests}

@api_router.get("/report/pdf")
async def generate_pdf_report(current_user: dict = Depends(get_current_user)):
    assessments = await db.assessments.find(
        {"user_id": current_user['id']}, {"_id": 0}
    ).sort("created_at", -1).to_list(1)
    if not assessments:
        raise HTTPException(status_code=404, detail="No assessments found")
    blood_tests = await db.blood_tests.find(
        {"user_id": current_user['id']}, {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    pdf_bytes = generate_health_report_pdf(current_user, assessments[0], blood_tests)
    await log_audit(current_user['id'], "pdf_report_generated", {})
    return Response(
        content=pdf_bytes, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=HealthGuard_Report_{current_user['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"}
    )

# ==================== REMINDER ROUTES ====================

@api_router.get("/reminders")
async def get_reminders(current_user: dict = Depends(get_current_user)):
    reminders = await db.reminders.find(
        {"user_id": current_user['id'], "status": "pending"}, {"_id": 0}
    ).sort("due_date", 1).to_list(100)
    return {"reminders": reminders}

@api_router.put("/reminders/{reminder_id}/complete")
async def complete_reminder(reminder_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.reminders.update_one(
        {"id": reminder_id, "user_id": current_user['id']},
        {"$set": {"status": "completed"}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reminder not found")
    await log_audit(current_user['id'], "reminder_completed", {"reminder_id": reminder_id})
    return {"message": "Reminder marked as complete"}

# ==================== ADMIN & COMPLIANCE ====================

@api_router.get("/admin/audit-logs")
async def get_audit_logs(current_user: dict = Depends(get_current_user), limit: int = 100):
    logs = await db.audit_logs.find(
        {"user_id": current_user['id']}, {"_id": 0}
    ).sort("timestamp", -1).to_list(limit)
    return {"audit_logs": logs}

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ml_models": {
            "diabetes": "v2_enhanced" if enhanced_predictor.diabetes_model else "unavailable",
            "cholesterol": "v2_enhanced" if enhanced_predictor.cholesterol_model else "unavailable"
        }
    }

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 HealthGuard AI Medical-Grade API Starting...")
    logger.info(f"✅ ML Models: {enhanced_predictor.diabetes_model is not None}")
    logger.info(f"✅ Email Service configured: {bool(os.environ.get('GMAIL_APP_PASS'))}")
    if not os.environ.get('GMAIL_USER') or not os.environ.get('GMAIL_APP_PASS'):
        logger.warning("⚠️ GMAIL_USER or GMAIL_APP_PASS missing — emails will NOT be sent!")
    scheduler.add_job(send_due_reminders, 'interval', minutes=1)
    scheduler.start()
    logger.info("✅ Reminder scheduler started — checking every 1 minute")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown()
    client.close()