QUIZ_QUESTIONS = [
    # Diabetes Questions (15)
    {
        "id": "d1",
        "category": "diabetes",
        "question": "Do you feel excessively thirsty even after drinking water?",
        "type": "boolean",
        "importance": "A classic sign of high sugar; the body tries to flush sugar via urine.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d2",
        "category": "diabetes",
        "question": "Do you urinate more than 7-8 times a day or wake up at night to urinate?",
        "type": "boolean",
        "importance": "Excess sugar in blood pulls fluids from tissues, increasing urination.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d3",
        "category": "diabetes",
        "question": "Have you experienced sudden, unexplained weight loss?",
        "type": "boolean",
        "importance": "Without insulin working, the body burns fat/muscle for energy.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "d4",
        "category": "diabetes",
        "question": "Is your vision frequently blurry or fuzzy?",
        "type": "boolean",
        "importance": "High blood sugar causes the lens in the eye to swell.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d5",
        "category": "diabetes",
        "question": "Do you have tingling or numbness in your hands or feet?",
        "type": "boolean",
        "importance": "Chronic high sugar damages nerves (Peripheral Neuropathy).",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "d6",
        "category": "diabetes",
        "question": "Do you feel extremely tired or exhausted, especially after eating?",
        "type": "boolean",
        "importance": "Indicates inability to process glucose properly.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d7",
        "category": "diabetes",
        "question": "Do cuts or bruises take more than 2 weeks to heal?",
        "type": "boolean",
        "importance": "High sugar levels impair blood circulation and immune response.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "d8",
        "category": "diabetes",
        "question": "Have you noticed dark, velvety patches on your neck or armpits?",
        "type": "boolean",
        "importance": "This is Acanthosis Nigricans, a physical sign of insulin resistance.",
        "weight": 5,
        "gender_target": "both"
    },
    {
        "id": "d9",
        "category": "diabetes",
        "question": "Are you over the age of 45?",
        "type": "boolean",
        "importance": "Risk increases significantly with age as metabolism slows.",
        "weight": 2,
        "gender_target": "both"
    },
    {
        "id": "d10",
        "category": "diabetes",
        "question": "Is your BMI higher than 25 (Overweight/Obese)?",
        "type": "boolean",
        "importance": "Excess fat causes insulin resistance.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "d11",
        "category": "diabetes",
        "question": "Did a parent or sibling have Type 2 Diabetes?",
        "type": "boolean",
        "importance": "Genetics plays a major role in glucose handling.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "d12",
        "category": "diabetes",
        "question": "Are you physically active less than 3 times a week?",
        "type": "boolean",
        "importance": "Inactivity leads to sugar buildup.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d13",
        "category": "diabetes",
        "question": "Have you ever had high blood pressure?",
        "type": "boolean",
        "importance": "Part of Metabolic Syndrome alongside diabetes.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "d14",
        "category": "diabetes",
        "question": "(For Women) Did you have gestational diabetes during pregnancy?",
        "type": "boolean",
        "importance": "Increases lifetime risk of Type 2 Diabetes by 50%.",
        "weight": 5,
        "gender_target": "female"
    },
    {
        "id": "d15",
        "category": "diabetes",
        "question": "Do you have Polycystic Ovary Syndrome (PCOS)?",
        "type": "boolean",
        "importance": "PCOS is heavily linked to insulin resistance.",
        "weight": 4,
        "gender_target": "female"
    },
    # Cholesterol Questions (10)
    {
        "id": "c1",
        "category": "cholesterol",
        "question": "Do you have a family history of early heart attacks (under age 55)?",
        "type": "boolean",
        "importance": "High cholesterol is often inherited.",
        "weight": 5,
        "gender_target": "both"
    },
    {
        "id": "c2",
        "category": "cholesterol",
        "question": "Do you notice yellowish bumps around your eyes (Xanthelasma)?",
        "type": "boolean",
        "importance": "These are actual deposits of cholesterol.",
        "weight": 5,
        "gender_target": "both"
    },
    {
        "id": "c3",
        "category": "cholesterol",
        "question": "Do you have yellowish or white bumps on your wrists, elbows, or knees?",
        "type": "boolean",
        "importance": "Tendon xanthomas indicate very high cholesterol levels.",
        "weight": 5,
        "gender_target": "both"
    },
    {
        "id": "c4",
        "category": "cholesterol",
        "question": "Do you notice a white or gray ring around your iris (corneal arcus)?",
        "type": "boolean",
        "importance": "Especially in people under 45, indicates high cholesterol.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "c5",
        "category": "cholesterol",
        "question": "Do you smoke or use tobacco products?",
        "type": "boolean",
        "importance": "Smoking lowers good HDL and damages artery walls.",
        "weight": 4,
        "gender_target": "both"
    },
    {
        "id": "c6",
        "category": "cholesterol",
        "question": "Do you experience chest pain during physical exertion?",
        "type": "boolean",
        "importance": "Suggests arteries may be narrowed by cholesterol plaque.",
        "weight": 5,
        "gender_target": "both"
    },
    {
        "id": "c7",
        "category": "cholesterol",
        "question": "Is your diet high in red meat and full-fat dairy?",
        "type": "boolean",
        "importance": "Saturated fats directly raise LDL cholesterol.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "c8",
        "category": "cholesterol",
        "question": "Is your waist circumference over 40 inches (men) or 35 inches (women)?",
        "type": "boolean",
        "importance": "Visceral fat correlates with high triglycerides.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "c9",
        "category": "cholesterol",
        "question": "Do you have high blood pressure?",
        "type": "boolean",
        "importance": "Scars arteries, allowing cholesterol to settle easily.",
        "weight": 3,
        "gender_target": "both"
    },
    {
        "id": "c10",
        "category": "cholesterol",
        "question": "Do you sit for more than 6 hours a day?",
        "type": "boolean",
        "importance": "Sedentary behavior lowers enzymes that burn fats.",
        "weight": 2,
        "gender_target": "both"
    }
]

def get_all_questions():
    """Returns the full list of quiz questions for the frontend"""
    return QUIZ_QUESTIONS

def calculate_quiz_score(answers: dict, user_gender: str = "both") -> dict:
    """Calculate risk score from quiz answers adjusted for gender"""
    total_score = 0
    max_possible_score = 0
    
    # Normalize gender
    user_gender = user_gender.lower() if user_gender else "both"

    diabetes_score = 0
    diabetes_max = 0
    cholesterol_score = 0
    cholesterol_max = 0

    for question in QUIZ_QUESTIONS:
        target = question.get("gender_target", "both").lower()

        # Skip logic
        if target != "both" and target != user_gender:
            continue 

        q_id = question['id']
        weight = question['weight']

        max_possible_score += weight
        if question['category'] == 'diabetes':
            diabetes_max += weight
        else:
            cholesterol_max += weight

        if answers.get(q_id) is True:
            total_score += weight
            if question['category'] == 'diabetes':
                diabetes_score += weight
            else:
                cholesterol_score += weight

    # Calculate percentages
    overall_percentage = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0
    diabetes_percentage = (diabetes_score / diabetes_max * 100) if diabetes_max > 0 else 0
    cholesterol_percentage = (cholesterol_score / cholesterol_max * 100) if cholesterol_max > 0 else 0

    if overall_percentage < 25:
        risk_level = "Low"
    elif overall_percentage < 50:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "total_score": round(overall_percentage),
        "diabetes_score": round(diabetes_percentage),
        "cholesterol_score": round(cholesterol_percentage),
        "risk_level": risk_level,
        "max_score": max_possible_score,
        "raw_score": total_score,
        "applied_gender": user_gender
    }