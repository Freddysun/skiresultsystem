#!/usr/bin/env python3
"""
导入示例数据到数据库（不使用 AI）
"""
import sys
from pathlib import Path
import uuid
from datetime import datetime, date

sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, init_db
from models import Athlete, Organization, Competition, Event, Category, Result, GenderEnum, ResultStatusEnum
from dotenv import load_dotenv

load_dotenv()

def import_sample_data():
    """导入示例数据"""
    print("\n" + "="*80)
    print("导入示例数据到数据库")
    print("="*80 + "\n")
    
    print("初始化数据库...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # 1. 创建组织
        print("创建组织...")
        orgs = {
            '顺义区': Organization(id=str(uuid.uuid4()), name='顺义区', type='区代表队'),
            '海淀区': Organization(id=str(uuid.uuid4()), name='海淀区', type='区代表队'),
            '朝阳区': Organization(id=str(uuid.uuid4()), name='朝阳区', type='区代表队'),
            '丰台区': Organization(id=str(uuid.uuid4()), name='丰台区', type='区代表队'),
            '延庆区': Organization(id=str(uuid.uuid4()), name='延庆区', type='区代表队'),
            '西城区': Organization(id=str(uuid.uuid4()), name='西城区', type='区代表队'),
        }
        for org in orgs.values():
            db.add(org)
        db.flush()
        print(f"  创建了 {len(orgs)} 个组织")
        
        # 2. 创建比赛
        print("创建比赛...")
        comp1 = Competition(
            id=str(uuid.uuid4()),
            name='北京市青少年滑雪冠军赛',
            date=date(2025, 1, 1),
            location='北京',
            season='2025'
        )
        comp2 = Competition(
            id=str(uuid.uuid4()),
            name='北京市青少年滑雪锦标赛',
            date=date(2025, 12, 28),
            location='北京',
            season='2025'
        )
        db.add(comp1)
        db.add(comp2)
        db.flush()
        print("  创建了 2 场比赛")
        
        # 3. 创建项目
        print("创建项目...")
        event1 = Event(
            id=str(uuid.uuid4()),
            competition_id=comp1.id,
            name='大回转',
            description='大回转项目'
        )
        event2 = Event(
            id=str(uuid.uuid4()),
            competition_id=comp2.id,
            name='大回转',
            description='大回转项目'
        )
        db.add(event1)
        db.add(event2)
        db.flush()
        print("  创建了 2 个项目")
        
        # 4. 创建组别
        print("创建组别...")
        cat_u11_f = Category(
            id=str(uuid.uuid4()),
            event_id=event1.id,
            name='U11',
            gender=GenderEnum.FEMALE,
            description='U11 女子组'
        )
        cat_u13_m = Category(
            id=str(uuid.uuid4()),
            event_id=event1.id,
            name='U13',
            gender=GenderEnum.MALE,
            description='U13 男子组'
        )
        cat_ding_f = Category(
            id=str(uuid.uuid4()),
            event_id=event2.id,
            name='丁组',
            gender=GenderEnum.FEMALE,
            description='丁组 女子'
        )
        db.add(cat_u11_f)
        db.add(cat_u13_m)
        db.add(cat_ding_f)
        db.flush()
        print("  创建了 3 个组别")
        
        # 5. U11 女子组 - 完整数据
        print("创建 U11 女子组成绩...")
        u11_data = [
            ('姚知涵', '顺义区', 1, '0:00:24.07', '0:00:24.02', '0:00:48.09', '0:00:00.00'),
            ('司悦希', '海淀区', 2, '0:00:24.51', '0:00:24.58', '0:00:49.09', '0:00:01.00'),
            ('郑好', '朝阳区', 3, '0:00:24.92', '0:00:25.28', '0:00:50.20', '0:00:02.11'),
            ('高翊宁', '丰台区', 4, '0:00:25.12', '0:00:25.45', '0:00:50.57', '0:00:02.48'),
            ('盛兰心', '海淀区', 5, '0:00:25.23', '0:00:25.52', '0:00:50.75', '0:00:02.66'),
            ('赵希悦', '延庆区', 6, '0:00:25.45', '0:00:25.68', '0:00:51.13', '0:00:03.04'),
            ('李思琪', '西城区', 7, '0:00:25.67', '0:00:25.89', '0:00:51.56', '0:00:03.47'),
            ('王雨涵', '海淀区', 8, '0:00:25.89', '0:00:26.12', '0:00:52.01', '0:00:03.92'),
            ('张欣怡', '朝阳区', 9, '0:00:26.15', '0:00:26.34', '0:00:52.49', '0:00:04.40'),
            ('刘诗涵', '顺义区', 10, '0:00:26.42', '0:00:26.58', '0:00:53.00', '0:00:04.91'),
        ]
        
        for name, org_name, rank, run1, run2, total, behind in u11_data:
            athlete = Athlete(
                id=str(uuid.uuid4()),
                name=name,
                gender=GenderEnum.FEMALE,
                organization_id=orgs[org_name].id
            )
            db.add(athlete)
            db.flush()
            
            result = Result(
                id=str(uuid.uuid4()),
                athlete_id=athlete.id,
                competition_id=comp1.id,
                event_id=event1.id,
                category_id=cat_u11_f.id,
                rank=rank,
                run1_time=run1,
                run2_time=run2,
                total_time=total,
                time_behind_leader=behind,
                status=ResultStatusEnum.COMPLETED
            )
            db.add(result)
        
        print(f"  创建了 {len(u11_data)} 条 U11 女子组成绩")
        
        # 6. U13 男子组 - 完整数据
        print("创建 U13 男子组成绩...")
        u13_data = [
            ('王睿祺', '海淀区', 1, '0:00:22.36', '0:00:22.29', '0:00:44.65', '0:00:00.00'),
            ('王梓墨', '海淀区', 2, '0:00:22.66', '0:00:22.76', '0:00:45.42', '0:00:00.77'),
            ('国益霖', '延庆区', 3, '0:00:22.49', '0:00:22.94', '0:00:45.43', '0:00:00.78'),
            ('丁天睿', '西城区', 4, '0:00:23.15', '0:00:23.45', '0:00:46.60', '0:00:01.95'),
            ('池皓翔', '海淀区', 5, '0:00:23.28', '0:00:23.50', '0:00:46.78', '0:00:02.13'),
            ('李明轩', '朝阳区', 6, '0:00:23.45', '0:00:23.72', '0:00:47.17', '0:00:02.52'),
            ('张浩然', '顺义区', 7, '0:00:23.68', '0:00:23.95', '0:00:47.63', '0:00:02.98'),
            ('刘子豪', '丰台区', 8, '0:00:23.92', '0:00:24.18', '0:00:48.10', '0:00:03.45'),
            ('陈俊杰', '西城区', 9, '0:00:24.15', '0:00:24.42', '0:00:48.57', '0:00:03.92'),
            ('赵宇航', '海淀区', 10, '0:00:24.38', '0:00:24.65', '0:00:49.03', '0:00:04.38'),
        ]
        
        for name, org_name, rank, run1, run2, total, behind in u13_data:
            athlete = Athlete(
                id=str(uuid.uuid4()),
                name=name,
                gender=GenderEnum.MALE,
                organization_id=orgs[org_name].id
            )
            db.add(athlete)
            db.flush()
            
            result = Result(
                id=str(uuid.uuid4()),
                athlete_id=athlete.id,
                competition_id=comp1.id,
                event_id=event1.id,
                category_id=cat_u13_m.id,
                rank=rank,
                run1_time=run1,
                run2_time=run2,
                total_time=total,
                time_behind_leader=behind,
                status=ResultStatusEnum.COMPLETED
            )
            db.add(result)
        
        print(f"  创建了 {len(u13_data)} 条 U13 男子组成绩")
        
        # 7. 丁组女子 - 完整数据
        print("创建丁组女子成绩...")
        ding_data = [
            ('司悦希', '海淀区', 1, '0:00:23.28', '0:00:23.60', '0:00:46.88', '0:00:00.00'),
            ('盛兰心', '海淀区', 2, '0:00:24.17', '0:00:24.05', '0:00:48.22', '0:00:01.34'),
            ('赵希悦', '延庆区', 3, '0:00:23.81', '0:00:24.65', '0:00:48.46', '0:00:01.58'),
            ('姚知涵', '顺义区', 4, '0:00:24.25', '0:00:24.50', '0:00:48.75', '0:00:01.87'),
            ('高翊宁', '丰台区', 5, '0:00:24.36', '0:00:24.40', '0:00:48.76', '0:00:01.88'),
            ('郑好', '朝阳区', 6, '0:00:24.52', '0:00:24.68', '0:00:49.20', '0:00:02.32'),
            ('李思琪', '西城区', 7, '0:00:24.78', '0:00:24.92', '0:00:49.70', '0:00:02.82'),
            ('王雨涵', '海淀区', 8, '0:00:25.05', '0:00:25.18', '0:00:50.23', '0:00:03.35'),
            ('张欣怡', '朝阳区', 9, '0:00:25.32', '0:00:25.45', '0:00:50.77', '0:00:03.89'),
            ('刘诗涵', '顺义区', 10, '0:00:25.58', '0:00:25.72', '0:00:51.30', '0:00:04.42'),
        ]
        
        for name, org_name, rank, run1, run2, total, behind in ding_data:
            athlete = db.query(Athlete).filter(Athlete.name == name).first()
            if not athlete:
                athlete = Athlete(
                    id=str(uuid.uuid4()),
                    name=name,
                    gender=GenderEnum.FEMALE,
                    organization_id=orgs[org_name].id
                )
                db.add(athlete)
                db.flush()
            
            result = Result(
                id=str(uuid.uuid4()),
                athlete_id=athlete.id,
                competition_id=comp2.id,
                event_id=event2.id,
                category_id=cat_ding_f.id,
                rank=rank,
                run1_time=run1,
                run2_time=run2,
                total_time=total,
                time_behind_leader=behind,
                status=ResultStatusEnum.COMPLETED
            )
            db.add(result)
        
        print(f"  创建了 {len(ding_data)} 条丁组女子成绩")
        
        db.commit()
        
        print("\n" + "="*80)
        print("导入完成！")
        print("="*80)
        
        athlete_count = db.query(Athlete).count()
        org_count = db.query(Organization).count()
        comp_count = db.query(Competition).count()
        event_count = db.query(Event).count()
        category_count = db.query(Category).count()
        result_count = db.query(Result).count()
        
        print(f"\n数据库统计:")
        print(f"  运动员: {athlete_count} 名")
        print(f"  组织: {org_count} 个")
        print(f"  比赛: {comp_count} 场")
        print(f"  项目: {event_count} 个")
        print(f"  组别: {category_count} 个")
        print(f"  成绩: {result_count} 条\n")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = import_sample_data()
    sys.exit(0 if success else 1)
