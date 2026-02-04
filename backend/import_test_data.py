#!/usr/bin/env python3
"""导入测试数据到数据库
"""
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from services.recognition_service import RecognitionService
from database import SessionLocal, init_db
from models import Athlete, Organization, Competition, Event, Category, Result, GenderEnum
from dotenv import load_dotenv

load_dotenv()

def import_file_to_db(file_path: str, db):
    print(f"\n{'='*80}")
    print(f"导入文件: {os.path.basename(file_path)}")
    print(f"{'='*80}\n")
    
    recognition_service = RecognitionService()
    
    print("步骤 1: 提取 PDF 文本...")
    text = recognition_service._extract_pdf_text(file_path)
    print(f"提取文本长度: {len(text)} 字符\n")
    
    print("步骤 2: 使用 Bedrock Claude 提取结构化数据...")
    structured_data = recognition_service._extract_structured_data(text)
    
    if "error" in structured_data:
        print(f"提取失败: {structured_data['error']}")
        return False
    
    print("数据提取成功！\n")
    
    comp_data = structured_data.get('competition', {})
    event_data = structured_data.get('event', {})
    results_data = structured_data.get('results', [])
    
    print(f"比赛名称: {comp_data.get('name', 'N/A')}")
    print(f"比赛日期: {comp_data.get('date', 'N/A')}")
    print(f"项目名称: {event_data.get('name', 'N/A')}")
    print(f"成绩条数: {len(results_data)}\n")
    
    print("步骤 3: 导入数据到数据库...")
    
    try:
        comp_name = comp_data.get('name', '未知比赛')
        comp_date_str = comp_data.get('date')
        comp_date = None
        if comp_date_str:
            try:
                comp_date = datetime.strptime(comp_date_str, '%Y-%m-%d').date()
            except:
                pass
        
        competition = db.query(Competition).filter(
            Competition.name == comp_name
        ).first()
        
        if not competition:
            competition = Competition(
                id=str(uuid.uuid4()),
                name=comp_name,
                date=comp_date,
                location=comp_data.get('location', '北京'),
                season=comp_data.get('season', '2025')
            )
            db.add(competition)
            db.flush()
            print(f"  创建比赛: {comp_name}")
        else:
            print(f"  使用现有比赛: {comp_name}")
        
        event_name = event_data.get('name', '大回转')
        event = db.query(Event).filter(
            Event.name == event_name,
            Event.competition_id == competition.id
        ).first()
        
        if not event:
            event = Event(
                id=str(uuid.uuid4()),
                competition_id=competition.id,
                name=event_name,
                description=f"{event_name}项目"
            )
            db.add(event)
            db.flush()
            print(f"  创建项目: {event_name}")
        else:
            print(f"  使用现有项目: {event_name}")
        
        imported_count = 0
        skipped_count = 0
        
        for result_data in results_data:
            athlete_name = result_data.get('athlete_name')
            if not athlete_name:
                continue
            
            org_name = result_data.get('organization', '未知')
            category_name = result_data.get('category', 'U11')
            gender_str = result_data.get('gender', '女')
            
            organization = db.query(Organization).filter(
                Organization.name == org_name
            ).first()
            
            if not organization:
                organization = Organization(
                    id=str(uuid.uuid4()),
                    name=org_name,
                    type='俱乐部'
                )
                db.add(organization)
                db.flush()
            
            athlete = db.query(Athlete).filter(
                Athlete.name == athlete_name
            ).first()
            
            if not athlete:
                gender = GenderEnum.FEMALE if '女' in gender_str else GenderEnum.MALE
                athlete = Athlete(
                    id=str(uuid.uuid4()),
                    name=athlete_name,
                    gender=gender,
                    organization_id=organization.id
                )
                db.add(athlete)
                db.flush()
            
            gender = GenderEnum.FEMALE if '女' in gender_str else GenderEnum.MALE
            category = db.query(Category).filter(
                Category.name == category_name,
                Category.gender == gender,
                Category.event_id == event.id
            ).first()
            
            if not category:
                category = Category(
                    id=str(uuid.uuid4()),
                    event_id=event.id,
                    name=category_name,
                    gender=gender,
                    description=f"{category_name} {gender_str}"
                )
                db.add(category)
                db.flush()
            
            existing_result = db.query(Result).filter(
                Result.athlete_id == athlete.id,
                Result.competition_id == competition.id,
                Result.event_id == event.id,
                Result.category_id == category.id
            ).first()
            
            if existing_result:
                skipped_count += 1
                continue
            
            from models import ResultStatusEnum
            result = Result(
                id=str(uuid.uuid4()),
                athlete_id=athlete.id,
                competition_id=competition.id,
                event_id=event.id,
                category_id=category.id,
                rank=result_data.get('rank'),
                run1_time=result_data.get('run1_time'),
                run2_time=result_data.get('run2_time'),
                total_time=result_data.get('total_time'),
                time_behind_leader=result_data.get('time_behind_leader'),
                status=ResultStatusEnum.COMPLETED
            )
            db.add(result)
            imported_count += 1
        
        db.commit()
        
        print(f"\n导入完成:")
        print(f"  新增成绩: {imported_count} 条")
        print(f"  跳过重复: {skipped_count} 条")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*80)
    print("导入测试数据到数据库")
    print("="*80)
    
    print("\n初始化数据库...")
    init_db()
    
    db = SessionLocal()
    
    try:
        test_files = [
            "../test_files/s3_samples/高山滑雪大回转_U11_女子.pdf",
            "../test_files/s3_samples/11.非正式总成绩_高山滑雪大回转_丁组_女子.pdf",
            "../test_files/s3_samples/高山滑雪大回转_U13_男子.pdf"
        ]
        
        results = []
        for file_path in test_files:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            if os.path.exists(full_path):
                success = import_file_to_db(full_path, db)
                results.append((os.path.basename(file_path), success))
            else:
                print(f"\n文件不存在: {file_path}")
                results.append((os.path.basename(file_path), False))
        
        print("\n" + "="*80)
        print("导入总结")
        print("="*80)
        
        success_count = sum(1 for _, success in results if success)
        total_count = len(results)
        
        for filename, success in results:
            status = "[成功]" if success else "[失败]"
            print(f"  {status} - {filename}")
        
        print(f"\n总计: {success_count}/{total_count} 个文件导入成功")
        
        print("\n" + "="*80)
        print("数据库统计")
        print("="*80)
        
        athlete_count = db.query(Athlete).count()
        org_count = db.query(Organization).count()
        comp_count = db.query(Competition).count()
        event_count = db.query(Event).count()
        category_count = db.query(Category).count()
        result_count = db.query(Result).count()
        
        print(f"  运动员: {athlete_count} 名")
        print(f"  组织: {org_count} 个")
        print(f"  比赛: {comp_count} 场")
        print(f"  项目: {event_count} 个")
        print(f"  组别: {category_count} 个")
        print(f"  成绩: {result_count} 条")
        print()
        
    finally:
        db.close()

if __name__ == "__main__":
    main()