import os
import django

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sambililacore.settings')
django.setup()

from curriculum.models import Curriculum, CurriculumLevel, SubjectTemplate, CurriculumSubject

def seed_zambian_structure():
    print("Starting Zambian curriculum seed process...")

    # 1. Define Curricula
    primary_cur, _ = Curriculum.objects.get_or_create(
        name="Zambian Primary Education", 
        defaults={'is_active': True, 'display_order': 1}
    )
    secondary_cur, _ = Curriculum.objects.get_or_create(
        name="Zambian Secondary Education", 
        defaults={'is_active': True, 'display_order': 2}
    )

    # 2. Setup Primary Levels (Grades 1-7)
    for i in range(1, 8):
        CurriculumLevel.objects.get_or_create(
            curriculum=primary_cur, 
            level_number=i, 
            defaults={
                'name': f"Grade {i}", 
                'stage': 'primary'
            }
        )

    # 3. Setup Secondary Levels (Form 1 - Form 5)
    # Mapping to stages: Forms 1-2 (Junior), Forms 3-5 (Senior)
    for i in range(1, 6):
        stage = 'junior_secondary' if i <= 2 else 'senior_secondary'
        CurriculumLevel.objects.get_or_create(
            curriculum=secondary_cur, 
            level_number=i, 
            defaults={
                'name': f"Form {i}", 
                'stage': stage,
                'streams_applicable': True 
            }
        )

    # 4. Create Zambian Subject Templates
    subjects_to_create = [
        {"code": "MATH", "name": "Mathematics"},
        {"code": "ENG", "name": "English Language"},
        {"code": "ZAM-LANG", "name": "Zambian Languages"},
        {"code": "SCI", "name": "Integrated Science"},
        {"code": "SOC", "name": "Social Studies"},
        {"code": "RE", "name": "Religious Education"},
        {"code": "CPE", "name": "Creative & Technology Studies"}
    ]
    
    subject_objs = {}
    for sub in subjects_to_create:
        obj, _ = SubjectTemplate.objects.get_or_create(
            code=sub['code'], 
            defaults={'name': sub['name']}
        )
        subject_objs[sub['code']] = obj

    # 5. Link to a Primary Level (Grade 1 Example)
    grade1 = CurriculumLevel.objects.get(curriculum=primary_cur, name="Grade 1")
    
    for code, obj in subject_objs.items():
        CurriculumSubject.objects.get_or_create(
            curriculum=primary_cur, 
            level=grade1, 
            subject_template=obj, 
            defaults={'is_compulsory': True}
        )
    
    print("Zambian curriculum seeded successfully (Grades 1-7 & Form 1-5).")

if __name__ == "__main__":
    seed_zambian_structure()
