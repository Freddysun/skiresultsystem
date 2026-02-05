#!/usr/bin/env python3
"""
导入完整数据到数据库（基于 PDF 文本手动解析）
包含所有 PDF 中的完整参赛选手数据：
- U11 女子组: 23 名选手
- U13 男子组: 35 名选手
- 丁组 女子: 16 名选手
总计: 74 条成绩记录
"""
import sys
from pathlib import Path
import uuid
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, init_db
from models import Athlete, Organization, Competition, Event, Category, Result, GenderEnum, ResultStatusEnum
from dotenv import load_dotenv

load_dotenv()

def import_complete_data():
    """导入完整数据"""
    print("\n" + "="*80)
    print("导入完整数据到数据库")
    print("="*80 + "\n")
    
    # 初始化数据库
    print("初始化数据库...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # 清空现有数据
        print("清空现有数据...")
        db.query(Result).delete()
        db.query(Athlete).delete()
        db.query(Category).delete()
        db.query(Event).delete()
        db.query(Competition).delete()
        db.query(Organization).delete()
        db.commit()
        print("  已清空现有数据\n")
        
        # 1. 创建组织
        print("创建组织...")
        orgs = {}
        org_names = ['顺义区', '海淀区', '朝阳区', '丰台区', '延庆区', '西城区', '东城区', 
                     '通州区', '大兴区', '密云区', '经开区', '房山区', '昌平区', '石景山区', 
                     '怀柔区', '门头沟区']
        for org_name in org_names:
            org = Organization(id=str(uuid.uuid4()), name=org_name, type='区代表队')
            orgs[org_name] = org
            db.add(org)
        db.flush()
        print(f"  创建了 {len(orgs)} 个组织\n")
        
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
        print("  创建了 2 场比赛\n")
        
        # 3. 创建项目
        print("创建项目...")
        event1 = Event(id=str(uuid.uuid4()), competition_id=comp1.id, name='大回转', description='大回转项目')
        event2 = Event(id=str(uuid.uuid4()), competition_id=comp2.id, name='大回转', description='大回转项目')
        db.add(event1)
        db.add(event2)
        db.flush()
        print("  创建了 2 个项目\n")
        
        # 4. 创建组别
        print("创建组别...")
        cat_u11_f = Category(id=str(uuid.uuid4()), event_id=event1.id, name='U11', gender=GenderEnum.FEMALE, description='U11 女子组')
        cat_u13_m = Category(id=str(uuid.uuid4()), event_id=event1.id, name='U13', gender=GenderEnum.MALE, description='U13 男子组')
        cat_ding_f = Category(id=str(uuid.uuid4()), event_id=event2.id, name='丁组', gender=GenderEnum.FEMALE, description='丁组 女子')
        db.add(cat_u11_f)
        db.add(cat_u13_m)
        db.add(cat_ding_f)
        db.flush()
        print("  创建了 3 个组别\n")
        
        # 5. U11 女子组数据（23 名选手完成比赛）
        print("导入 U11 女子组数据...")
        u11_data = [
            (1, '姚知涵', '顺义区', '0:00:24.07', '0:00:24.02', '0:00:48.09', '0:00:00.00'),
            (2, '司悦希', '海淀区', '0:00:24.51', '0:00:24.58', '0:00:49.09', '0:00:01.00'),
            (3, '郑好', '朝阳区', '0:00:24.92', '0:00:25.28', '0:00:50.20', '0:00:02.11'),
            (4, '高翊宁', '丰台区', '0:00:25.52', '0:00:25.05', '0:00:50.57', '0:00:02.48'),
            (5, '盛兰心', '海淀区', '0:00:25.92', '0:00:24.83', '0:00:50.75', '0:00:02.66'),
            (6, '张聿含', '顺义区', '0:00:25.75', '0:00:25.78', '0:00:51.53', '0:00:03.44'),
            (7, '苏子喻', '顺义区', '0:00:24.92', '0:00:26.87', '0:00:51.79', '0:00:03.70'),
            (8, '赵希悦', '延庆区', '0:00:27.44', '0:00:24.91', '0:00:52.35', '0:00:04.26'),
            (9, '刘紫彰', '西城区', '0:00:26.20', '0:00:26.32', '0:00:52.52', '0:00:04.43'),
            (10, '张雯嘉', '东城区', '0:00:26.21', '0:00:26.32', '0:00:52.53', '0:00:04.44'),
            (11, '荆瑜宸', '通州区', '0:00:26.26', '0:00:26.80', '0:00:53.06', '0:00:04.97'),
            (12, '何雨恬', '朝阳区', '0:00:27.48', '0:00:26.04', '0:00:53.52', '0:00:05.43'),
            (13, '刘珺劼', '延庆区', '0:00:27.15', '0:00:26.58', '0:00:53.73', '0:00:05.64'),
            (14, '李若瑜', '大兴区', '0:00:28.27', '0:00:25.59', '0:00:53.86', '0:00:05.77'),
            (15, '国益萌', '延庆区', '0:00:28.57', '0:00:27.72', '0:00:56.29', '0:00:08.20'),
            (16, '陈美妍', '西城区', '0:00:28.98', '0:00:27.62', '0:00:56.60', '0:00:08.51'),
            (17, '何雨洛', '密云区', '0:00:29.60', None, None, None),
            (18, '毕雪蔓', '经开区', '0:00:31.12', None, None, None),
            (19, '许芳菲', '经开区', '0:00:32.22', None, None, None),
            (20, '刘承瑾', '顺义区', '0:00:35.87', None, None, None),
            (21, '王紫洋', '房山区', '0:00:36.30', None, None, None),
            (22, '孙孟兰', '房山区', '0:00:42.71', None, None, None),
            (23, '张颢凡', '顺义区', '0:02:34.16', None, None, None),
        ]
        
        for rank, name, org_name, run1, run2, total, behind in u11_data:
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
        
        print(f"  导入了 {len(u11_data)} 条 U11 女子组成绩\n")
        
        # 6. U13 男子组数据（35 名选手完成比赛）
        print("导入 U13 男子组数据...")
        u13_data = [
            (1, '王睿祺', '海淀区', '0:00:22.36', '0:00:22.29', '0:00:44.65', '0:00:00.00'),
            (2, '王梓墨', '海淀区', '0:00:22.66', '0:00:22.76', '0:00:45.42', '0:00:00.77'),
            (3, '国益霖', '延庆区', '0:00:22.49', '0:00:22.94', '0:00:45.43', '0:00:00.78'),
            (4, '丁天睿', '西城区', '0:00:23.08', '0:00:23.52', '0:00:46.60', '0:00:01.95'),
            (5, '池皓翔', '海淀区', '0:00:23.17', '0:00:23.61', '0:00:46.78', '0:00:02.13'),
            (6, '牧仁', '西城区', '0:00:23.26', '0:00:23.59', '0:00:46.85', '0:00:02.20'),
            (7, '李攸宁', '昌平区', '0:00:23.52', '0:00:23.75', '0:00:47.27', '0:00:02.62'),
            (8, '殷鼎昊', '朝阳区', '0:00:23.62', '0:00:23.78', '0:00:47.40', '0:00:02.75'),
            (9, '郝熹芃', '延庆区', '0:00:24.05', '0:00:23.58', '0:00:47.63', '0:00:02.98'),
            (10, '王思博', '延庆区', '0:00:23.71', '0:00:23.94', '0:00:47.65', '0:00:03.00'),
            (11, '张恒屹', '西城区', '0:00:23.52', '0:00:24.17', '0:00:47.69', '0:00:03.04'),
            (12, '张宇辰', '通州区', '0:00:24.00', '0:00:24.25', '0:00:48.25', '0:00:03.60'),
            (13, '须星然', '石景山区', '0:00:24.02', '0:00:24.35', '0:00:48.37', '0:00:03.72'),
            (14, '冯天泽', '怀柔区', '0:00:24.24', '0:00:24.18', '0:00:48.42', '0:00:03.77'),
            (15, '蔡银河', '西城区', '0:00:24.34', '0:00:25.51', '0:00:49.85', '0:00:05.20'),
            (16, '李一宸', '西城区', '0:00:24.66', '0:00:25.31', '0:00:49.97', '0:00:05.32'),
            (17, '周子晨', '通州区', '0:00:24.67', None, None, None),
            (18, '邱铉浩', '密云区', '0:00:24.71', None, None, None),
            (19, '杨舰霆', '海淀区', '0:00:24.93', None, None, None),
            (20, '张铭哲', '经开区', '0:00:24.94', None, None, None),
            (21, '李星睿', '东城区', '0:00:24.98', None, None, None),
            (22, '郑钦泽', '西城区', '0:00:25.19', None, None, None),
            (23, '朱英恺', '朝阳区', '0:00:25.51', None, None, None),
            (24, '张文翰', '密云区', '0:00:25.75', None, None, None),
            (25, '秦予辰', '大兴区', '0:00:26.76', None, None, None),
            (26, '张纭赫', '通州区', '0:00:27.14', None, None, None),
            (27, '沈靖程', '经开区', '0:00:28.07', None, None, None),
            (28, '祁嘉维', '东城区', '0:00:28.40', None, None, None),
            (29, '崔楚杭', '密云区', '0:00:29.31', None, None, None),
            (30, '李昀璟', '怀柔区', '0:00:30.00', None, None, None),
            (31, '王逸轩', '房山区', '0:00:30.79', None, None, None),
            (32, '刘轩宁', '大兴区', '0:00:30.89', None, None, None),
            (33, '俞文龙', '大兴区', '0:00:31.41', None, None, None),
            (34, '唐子琪', '门头沟区', '0:00:41.93', None, None, None),
            (35, '熊天放', '经开区', '0:02:19.28', None, None, None),
        ]
        
        for rank, name, org_name, run1, run2, total, behind in u13_data:
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
        
        print(f"  导入了 {len(u13_data)} 条 U13 男子组成绩\n")
        
        # 7. 丁组女子数据（16 名选手）
        print("导入丁组女子数据...")
        ding_data = [
            (1, '司悦希', '海淀区', '0:00:23.28', '0:00:23.60', '0:00:46.88', '0:00:00.00'),
            (2, '盛兰心', '海淀区', '0:00:24.17', '0:00:24.05', '0:00:48.22', '0:00:01.34'),
            (3, '赵希悦', '延庆区', '0:00:23.81', '0:00:24.65', '0:00:48.46', '0:00:01.58'),
            (4, '姚知涵', '顺义区', '0:00:24.37', '0:00:24.38', '0:00:48.75', '0:00:01.87'),
            (5, '高翊宁', '丰台区', '0:00:24.58', '0:00:24.18', '0:00:48.76', '0:00:01.88'),
            (6, '郑好', '朝阳区', '0:00:24.94', '0:00:24.59', '0:00:49.53', '0:00:02.65'),
            (7, '何雨恬', '朝阳区', '0:00:24.71', '0:00:25.56', '0:00:50.27', '0:00:03.39'),
            (8, '李若瑜', '大兴区', '0:00:25.09', '0:00:25.42', '0:00:50.51', '0:00:03.63'),
            (9, '刘珺劼', '延庆区', '0:00:24.96', '0:00:25.63', '0:00:50.59', '0:00:03.71'),
            (10, '张聿含', '顺义区', '0:00:25.41', '0:00:26.39', '0:00:51.80', '0:00:04.92'),
            (11, '荆瑜宸', '通州区', '0:00:26.39', '0:00:26.06', '0:00:52.45', '0:00:05.57'),
            (12, '张雯嘉', '东城区', '0:00:26.94', '0:00:26.83', '0:00:53.77', '0:00:06.89'),
            (13, '国益萌', '延庆区', '0:00:27.28', '0:00:27.18', '0:00:54.46', '0:00:07.58'),
            (14, '陈美妍', '西城区', '0:00:27.19', '0:00:28.26', '0:00:55.45', '0:00:08.57'),
            (15, '苏子喻', '顺义区', '0:00:54.92', '0:00:25.79', '0:01:20.71', '0:00:33.83'),
            (16, '刘紫彰', '西城区', '0:00:24.41', 'DQ', None, None),
        ]
        
        for rank, name, org_name, run1, run2, total, behind in ding_data:
            # 检查运动员是否已存在
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
            
            status = ResultStatusEnum.DSQ if run2 == 'DQ' else ResultStatusEnum.COMPLETED
            result = Result(
                id=str(uuid.uuid4()),
                athlete_id=athlete.id,
                competition_id=comp2.id,
                event_id=event2.id,
                category_id=cat_ding_f.id,
                rank=rank if status == ResultStatusEnum.COMPLETED else None,
                run1_time=run1,
                run2_time=run2 if run2 != 'DQ' else None,
                total_time=total,
                time_behind_leader=behind,
                status=status
            )
            db.add(result)
        
        print(f"  导入了 {len(ding_data)} 条丁组女子成绩\n")
        
        # 提交所有更改
        db.commit()
        
        print("="*80)
        print("导入完成！")
        print("="*80)
        
        # 显示统计
        athlete_count = db.query(Athlete).count()
        org_count = db.query(Organization).count()
        comp_count = db.query(Competition).count()
        result_count = db.query(Result).count()
        
        print(f"\n数据库统计:")
        print(f"  运动员: {athlete_count} 名")
        print(f"  组织: {org_count} 个")
        print(f"  比赛: {comp_count} 场")
        print(f"  成绩: {result_count} 条")
        print(f"\n各组别成绩数:")
        print(f"  U11 女子: {db.query(Result).filter(Result.category_id == cat_u11_f.id).count()} 条")
        print(f"  U13 男子: {db.query(Result).filter(Result.category_id == cat_u13_m.id).count()} 条")
        print(f"  丁组 女子: {db.query(Result).filter(Result.category_id == cat_ding_f.id).count()} 条\n")
        
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
    success = import_complete_data()
    sys.exit(0 if success else 1)
