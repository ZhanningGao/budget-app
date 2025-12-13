"""
数据库管理模块
使用SQLite作为后端数据库
支持持久存储（优先使用 /mnt 挂载的存储桶）
"""
import sqlite3
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# 持久存储路径（挂载的存储桶）
PERSISTENT_STORAGE = '/mnt'
PERSISTENT_DB_FILE = os.path.join(PERSISTENT_STORAGE, 'budget.db')
PERSISTENT_BACKUP_DIR = os.path.join(PERSISTENT_STORAGE, 'backups')

# 本地数据目录（容器内，作为备用）
LOCAL_DATA_DIR = os.getenv('DATA_DIR', '.')
LOCAL_DB_FILE = os.path.join(LOCAL_DATA_DIR, 'budget.db')
LOCAL_BACKUP_DIR = os.path.join(LOCAL_DATA_DIR, 'backups')

# 确定使用哪个数据库路径（优先持久存储）
def _get_db_paths():
    """获取数据库路径（优先持久存储）"""
    # 检查持久存储是否可用
    if os.path.exists(PERSISTENT_STORAGE) and os.path.isdir(PERSISTENT_STORAGE):
        # 持久存储可用，优先使用
        db_file = PERSISTENT_DB_FILE
        backup_dir = PERSISTENT_BACKUP_DIR
        use_persistent = True
    else:
        # 持久存储不可用，使用本地
        db_file = LOCAL_DB_FILE
        backup_dir = LOCAL_BACKUP_DIR
        use_persistent = False
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    
    return db_file, backup_dir, use_persistent

# 初始化数据库路径
DB_FILE, BACKUP_DIR, USE_PERSISTENT = _get_db_paths()

def _migrate_to_persistent_storage():
    """将本地数据库迁移到持久存储（如果持久存储可用且本地有数据）"""
    if not USE_PERSISTENT:
        return  # 持久存储不可用，无需迁移
    
    # 如果持久存储已有数据库，不迁移
    if os.path.exists(PERSISTENT_DB_FILE):
        return
    
    # 如果本地有数据库，迁移到持久存储
    if os.path.exists(LOCAL_DB_FILE):
        try:
            print(f"📦 迁移数据库到持久存储: {LOCAL_DB_FILE} -> {PERSISTENT_DB_FILE}")
            shutil.copy2(LOCAL_DB_FILE, PERSISTENT_DB_FILE)
            # 同时迁移 WAL 和 SHM 文件（如果存在）
            if os.path.exists(LOCAL_DB_FILE + '-wal'):
                shutil.copy2(LOCAL_DB_FILE + '-wal', PERSISTENT_DB_FILE + '-wal')
            if os.path.exists(LOCAL_DB_FILE + '-shm'):
                shutil.copy2(LOCAL_DB_FILE + '-shm', PERSISTENT_DB_FILE + '-shm')
            print(f"✅ 数据库已迁移到持久存储")
        except Exception as e:
            print(f"⚠️ 数据库迁移失败: {e}，继续使用本地数据库")
    
    # 迁移备份文件
    if os.path.exists(LOCAL_BACKUP_DIR):
        try:
            os.makedirs(PERSISTENT_BACKUP_DIR, exist_ok=True)
            for filename in os.listdir(LOCAL_BACKUP_DIR):
                if filename.startswith('backup_') and filename.endswith('.db'):
                    src = os.path.join(LOCAL_BACKUP_DIR, filename)
                    dst = os.path.join(PERSISTENT_BACKUP_DIR, filename)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)
            print(f"✅ 备份文件已迁移到持久存储")
        except Exception as e:
            print(f"⚠️ 备份文件迁移失败: {e}")

# 在模块加载时尝试迁移
_migrate_to_persistent_storage()

# 重新初始化路径（迁移后）
DB_FILE, BACKUP_DIR, USE_PERSISTENT = _get_db_paths()

def get_db_connection():
    """获取数据库连接，带错误处理和回退机制"""
    global DB_FILE, BACKUP_DIR, USE_PERSISTENT  # 在函数开始处声明 global
    
    max_retries = 3
    retry_delay = 1  # 秒
    
    for attempt in range(max_retries):
        try:
            # 检查数据库文件所在目录是否可写
            db_dir = os.path.dirname(DB_FILE)
            if not os.path.exists(db_dir):
                try:
                    os.makedirs(db_dir, exist_ok=True)
                except Exception as e:
                    print(f"⚠️ 无法创建数据库目录 {db_dir}: {e}")
                    # 如果持久存储不可用，尝试回退到本地存储
                    if USE_PERSISTENT:
                        print(f"⚠️ 持久存储不可用，尝试使用本地存储")
                        DB_FILE = LOCAL_DB_FILE
                        BACKUP_DIR = LOCAL_BACKUP_DIR
                        USE_PERSISTENT = False
                        db_dir = os.path.dirname(DB_FILE)
                        os.makedirs(db_dir, exist_ok=True)
            
            # 添加超时设置，避免数据库锁定
            conn = sqlite3.connect(DB_FILE, timeout=30.0)
            conn.row_factory = sqlite3.Row  # 使结果可以像字典一样访问
            # 启用WAL模式，提高并发性能
            conn.execute('PRAGMA journal_mode=WAL')
            return conn
        except sqlite3.OperationalError as e:
            error_msg = str(e).lower()
            if 'disk i/o error' in error_msg or 'io error' in error_msg:
                print(f"⚠️ 数据库I/O错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    # 如果是持久存储的问题，尝试回退到本地存储
                    if USE_PERSISTENT and attempt == 1:
                        print(f"⚠️ 持久存储I/O错误，尝试回退到本地存储")
                        DB_FILE = LOCAL_DB_FILE
                        BACKUP_DIR = LOCAL_BACKUP_DIR
                        USE_PERSISTENT = False
                        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
                else:
                    # 最后一次尝试失败，抛出更友好的错误
                    raise Exception(f"数据库I/O错误: 无法访问数据库文件。可能是存储挂载问题或权限问题。请检查存储配置。")
            else:
                # 其他操作错误，直接抛出
                raise
        except Exception as e:
            # 其他异常，直接抛出
            raise

def init_database():
    """初始化数据库，创建表结构"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建分类表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            order_index INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建项目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            seq_num INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            unit TEXT,
            budget_quantity TEXT,
            budget_cost REAL DEFAULT 0,
            current_investment REAL DEFAULT 0,
            final_cost REAL DEFAULT 0,
            diff REAL DEFAULT 0,
            remark TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_id ON items(category_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_seq_num ON items(seq_num)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_order ON categories(order_index)')
    
    conn.commit()
    conn.close()

def get_all_categories() -> List[Dict]:
    """获取所有分类"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY order_index, id')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_category_by_name(name: str) -> Optional[Dict]:
    """根据名称获取分类"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_category(name: str) -> int:
    """添加分类，返回分类ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查是否已存在
    existing = get_category_by_name(name)
    if existing:
        conn.close()
        return existing['id']
    
    # 获取最大order_index
    cursor.execute('SELECT MAX(order_index) as max_order FROM categories')
    result = cursor.fetchone()
    max_order = result['max_order'] if result and result['max_order'] is not None else 0
    
    cursor.execute(
        'INSERT INTO categories (name, order_index) VALUES (?, ?)',
        (name, max_order + 1)
    )
    category_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return category_id

def delete_category(category_id: int) -> str:
    """删除分类及其关联的项目，返回消息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取分类信息
    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    category = cursor.fetchone()
    if not category:
        conn.close()
        raise ValueError('分类不存在')
    
    category_name = category['name']
    
    # 统计该分类下的项目数量
    cursor.execute('SELECT COUNT(*) as count FROM items WHERE category_id = ?', (category_id,))
    item_count = cursor.fetchone()['count']
    
    # 删除分类（由于外键约束 ON DELETE SET NULL，关联的项目 category_id 会被设置为 NULL）
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    
    if item_count > 0:
        return f'分类"{category_name}"及其下的 {item_count} 个项目已删除'
    else:
        return f'分类"{category_name}"已删除'

def get_all_items() -> List[Dict]:
    """获取所有项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON i.category_id = c.id
        ORDER BY c.order_index, c.id, i.seq_num
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """根据ID获取项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON i.category_id = c.id
        WHERE i.id = ?
    ''', (item_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_item(item_data: Dict, category_name: str = None) -> int:
    """添加项目，返回项目ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取或创建分类
    if category_name:
        category_id = add_category(category_name)
    else:
        category_id = None
    
    # 获取该分类下的最大序号
    if category_id:
        cursor.execute('SELECT MAX(seq_num) as max_seq FROM items WHERE category_id = ?', (category_id,))
        result = cursor.fetchone()
        max_seq = result['max_seq'] if result and result['max_seq'] is not None else 0
        seq_num = max_seq + 1
    else:
        seq_num = item_data.get('序号', 1)
    
    # 解析数值字段
    budget_cost = float(item_data.get('预算费用', 0) or 0)
    current_investment = float(item_data.get('当前投入', 0) or 0)
    final_cost = float(item_data.get('最终花费', 0) or 0)
    diff = float(item_data.get('差价', 0) or 0)
    
    cursor.execute('''
        INSERT INTO items (
            category_id, seq_num, project_name, unit, budget_quantity,
            budget_cost, current_investment, final_cost, diff, remark
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        category_id,
        seq_num,
        item_data.get('项目', ''),
        item_data.get('单位', ''),
        item_data.get('预算数量', ''),
        budget_cost,
        current_investment,
        final_cost,
        diff,
        item_data.get('备注', '')
    ))
    
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def update_item(item_id: int, item_data: Dict, category_name: str = None):
    """更新项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取或创建分类
    if category_name:
        category_id = add_category(category_name)
    else:
        # 保持原有分类
        cursor.execute('SELECT category_id FROM items WHERE id = ?', (item_id,))
        result = cursor.fetchone()
        category_id = result['category_id'] if result else None
    
    # 解析数值字段
    budget_cost = float(item_data.get('预算费用', 0) or 0)
    current_investment = float(item_data.get('当前投入', 0) or 0)
    final_cost = float(item_data.get('最终花费', 0) or 0)
    diff = float(item_data.get('差价', 0) or 0)
    
    cursor.execute('''
        UPDATE items SET
            category_id = ?,
            seq_num = ?,
            project_name = ?,
            unit = ?,
            budget_quantity = ?,
            budget_cost = ?,
            current_investment = ?,
            final_cost = ?,
            diff = ?,
            remark = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        category_id,
        item_data.get('序号', 1),
        item_data.get('项目', ''),
        item_data.get('单位', ''),
        item_data.get('预算数量', ''),
        budget_cost,
        current_investment,
        final_cost,
        diff,
        item_data.get('备注', ''),
        item_id
    ))
    
    conn.commit()
    conn.close()

def delete_items(item_ids: List[int]) -> str:
    """删除项目，返回消息"""
    if not item_ids:
        return ''
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查是否有分类行（项目名包含"合计"或"总计"的项目不能删除）
    placeholders = ','.join(['?'] * len(item_ids))
    cursor.execute(f'''
        SELECT id, project_name FROM items WHERE id IN ({placeholders})
    ''', item_ids)
    items = cursor.fetchall()
    
    protected_items = []
    deletable_items = []
    
    for item in items:
        project_name = item['project_name'] or ''
        if '合计' in project_name or '总计' in project_name:
            protected_items.append(item['id'])
        else:
            deletable_items.append(item['id'])
    
    if protected_items:
        return f'部分项目受保护，无法删除（合计行、总计行等）'
    
    if deletable_items:
        placeholders = ','.join(['?'] * len(deletable_items))
        cursor.execute(f'DELETE FROM items WHERE id IN ({placeholders})', deletable_items)
        conn.commit()
    
    conn.close()
    return '删除成功'

def renumber_items_in_category(category_id: int):
    """重新编号分类下的项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM items WHERE category_id = ? ORDER BY seq_num, id
    ''', (category_id,))
    items = cursor.fetchall()
    
    for index, item in enumerate(items, start=1):
        cursor.execute('UPDATE items SET seq_num = ? WHERE id = ?', (index, item['id']))
    
    conn.commit()
    conn.close()

def format_item_for_api(item: Dict) -> Dict:
    """格式化项目数据为API格式"""
    # 处理数值字段，确保0值也显示为空字符串（与前端一致）
    budget_cost = item.get('budget_cost')
    current_investment = item.get('current_investment')
    final_cost = item.get('final_cost')
    diff = item.get('diff')
    
    return {
        'id': item['id'],
        'category': item.get('category_name', '未分类'),
        '序号': item['seq_num'],
        '项目': item['project_name'],
        '单位': item['unit'] or '',
        '预算数量': item['budget_quantity'] or '',
        '预算费用': str(budget_cost) if budget_cost and budget_cost != 0 else '',
        '当前投入': str(current_investment) if current_investment and current_investment != 0 else '',
        '最终花费': str(final_cost) if final_cost and final_cost != 0 else '',
        '差价': str(diff) if diff and diff != 0 else '',
        '备注': item['remark'] or ''
    }

def get_data_for_api() -> Dict:
    """获取所有数据，格式化为API格式"""
    categories = get_all_categories()
    items = get_all_items()
    
    # 格式化分类列表（包含ID和名称）
    category_list = [cat['name'] for cat in categories]
    category_map = {cat['name']: cat['id'] for cat in categories}  # 分类名 -> ID映射
    
    # 格式化项目列表
    formatted_items = [format_item_for_api(item) for item in items]
    
    return {
        'categories': category_list,
        'category_map': category_map,  # 添加分类ID映射
        'items': formatted_items,
        'headers': ['序号', '项目', '单位', '预算数量', '预算费用', '当前投入', '最终花费', '差价', '备注']
    }

def import_from_excel_data(excel_data: Dict):
    """从Excel解析的数据导入到数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN TRANSACTION')
        
        # 清空现有数据
        cursor.execute('DELETE FROM items')
        cursor.execute('DELETE FROM categories')
        
        # 导入分类（直接在当前连接中插入，避免创建新连接）
        categories_map = {}  # 分类名 -> category_id
        
        # 获取最大order_index
        cursor.execute('SELECT MAX(order_index) as max_order FROM categories')
        result = cursor.fetchone()
        max_order = result['max_order'] if result and result['max_order'] is not None else 0
        
        for cat_name in excel_data.get('categories', []):
            if not cat_name or cat_name.strip() == '':
                continue
            max_order += 1
            cursor.execute(
                'INSERT INTO categories (name, order_index) VALUES (?, ?)',
                (cat_name, max_order)
            )
            category_id = cursor.lastrowid
            categories_map[cat_name] = category_id
        
        # 导入项目
        for item in excel_data.get('items', []):
            category_name = item.get('category', '未分类')
            if not category_name or category_name.strip() == '':
                category_name = '未分类'
            
            category_id = categories_map.get(category_name)
            if not category_id:
                # 如果分类不存在，创建它（在当前连接中）
                max_order += 1
                cursor.execute(
                    'INSERT INTO categories (name, order_index) VALUES (?, ?)',
                    (category_name, max_order)
                )
                category_id = cursor.lastrowid
                categories_map[category_name] = category_id
            
            # 解析数值字段
            budget_cost = float(item.get('预算费用', 0) or 0)
            current_investment = float(item.get('当前投入', 0) or 0)
            final_cost = float(item.get('最终花费', 0) or 0)
            diff = float(item.get('差价', 0) or 0)
            
            cursor.execute('''
                INSERT INTO items (
                    category_id, seq_num, project_name, unit, budget_quantity,
                    budget_cost, current_investment, final_cost, diff, remark
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                category_id,
                int(item.get('序号', 0)),
                item.get('项目', ''),
                item.get('单位', ''),
                item.get('预算数量', ''),
                budget_cost,
                current_investment,
                final_cost,
                diff,
                item.get('备注', '')
            ))
        
        # 提交事务
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def backup_database(description: str = '') -> Dict:
    """备份数据库，返回备份信息"""
    if not os.path.exists(DB_FILE):
        raise ValueError('数据库文件不存在')
    
    # 生成备份文件名（包含时间戳和描述）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if description:
        safe_desc = description.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
        backup_filename = f'backup_{timestamp}_{safe_desc}.db'
    else:
        backup_filename = f'backup_{timestamp}.db'
    
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # 复制数据库文件
    import shutil
    shutil.copy2(DB_FILE, backup_path)
    
    # 获取文件大小
    file_size = os.path.getsize(backup_path)
    
    return {
        'filename': backup_filename,
        'path': backup_path,
        'size': file_size,
        'created_at': datetime.now().isoformat(),
        'description': description
    }

def list_backups() -> List[Dict]:
    """列出所有备份文件"""
    backups = []
    
    if not os.path.exists(BACKUP_DIR):
        return backups
    
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith('backup_') and filename.endswith('.db'):
            backup_path = os.path.join(BACKUP_DIR, filename)
            try:
                stat = os.stat(backup_path)
                # 从文件名提取时间戳和描述
                parts = filename.replace('backup_', '').replace('.db', '').split('_', 2)
                timestamp_str = f"{parts[0]}_{parts[1]}" if len(parts) >= 2 else parts[0]
                description = parts[2] if len(parts) > 2 else ''
                
                backups.append({
                    'filename': filename,
                    'path': backup_path,
                    'size': stat.st_size,
                    'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'description': description
                })
            except Exception:
                continue
    
    # 按创建时间倒序排列（最新的在前）
    backups.sort(key=lambda x: x['created_at'], reverse=True)
    return backups

def restore_database(backup_filename: str) -> str:
    """从备份恢复数据库"""
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    if not os.path.exists(backup_path):
        raise ValueError(f'备份文件不存在: {backup_filename}')
    
    # 在恢复前先备份当前数据库
    try:
        current_backup = backup_database('before_restore')
        current_backup_msg = f'当前数据库已备份为: {current_backup["filename"]}'
    except Exception as e:
        current_backup_msg = f'警告: 无法备份当前数据库: {str(e)}'
    
    # 关闭所有数据库连接（通过创建新连接并立即关闭来确保）
    try:
        conn = get_db_connection()
        conn.close()
    except Exception:
        pass
    
    # 复制备份文件到数据库文件
    import shutil
    shutil.copy2(backup_path, DB_FILE)
    
    return f'数据库已从备份恢复: {backup_filename}. {current_backup_msg}'

def delete_backup(backup_filename: str) -> str:
    """删除备份文件"""
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    if not os.path.exists(backup_path):
        raise ValueError(f'备份文件不存在: {backup_filename}')
    
    if not backup_filename.startswith('backup_') or not backup_filename.endswith('.db'):
        raise ValueError('无效的备份文件名')
    
    os.remove(backup_path)
    return f'备份文件已删除: {backup_filename}'

def cleanup_old_backups(keep_count: int = 10) -> int:
    """清理旧备份，只保留最新的N个"""
    backups = list_backups()
    
    if len(backups) <= keep_count:
        return 0
    
    # 删除多余的备份
    deleted_count = 0
    for backup in backups[keep_count:]:
        try:
            os.remove(backup['path'])
            deleted_count += 1
        except Exception:
            continue
    
    return deleted_count

def update_category_order(category_orders: List[Dict[str, int]]):
    """更新分类排序
    Args:
        category_orders: [{'id': 1, 'order_index': 0}, {'id': 2, 'order_index': 1}, ...]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for cat_order in category_orders:
            cursor.execute(
                'UPDATE categories SET order_index = ? WHERE id = ?',
                (cat_order['order_index'], cat_order['id'])
            )
        conn.commit()
    finally:
        conn.close()

def update_item_order(category_id: int, item_orders: List[Dict[str, int]]):
    """更新项目排序
    Args:
        category_id: 分类ID
        item_orders: [{'id': 1, 'seq_num': 1}, {'id': 2, 'seq_num': 2}, ...]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for item_order in item_orders:
            cursor.execute(
                'UPDATE items SET seq_num = ? WHERE id = ? AND category_id = ?',
                (item_order['seq_num'], item_order['id'], category_id)
            )
        conn.commit()
    finally:
        conn.close()

