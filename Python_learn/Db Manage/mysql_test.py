# -*- coding: utf-8 -*-

"""
中烨风控数据导入数据库
"""

from dbhelper import DBHelper
from excelhelper import ExcelHelper
from sendmail import SendMail
from getconfig import GetConfig
from datetime import datetime
import time


def is_continue(msg):
    check_continue = input('%s,是否继续执行[Y/n]?' % msg).strip()
    if check_continue == 'Y':
        pass
    elif check_continue == 'n':
        exit('退出: %s。' % msg)
    else:
        exit('退出执行程序')


if __name__ == '__main__':

    # 记录开始执行时间点
    start_time = int(time.time())

    # 获取配置的参数
    file_dir = GetConfig('rsk', 'file_dir')
    file_name = GetConfig('rsk', 'file_name')
    work_dir = GetConfig('rsk', 'work_dir')
    table_name = GetConfig('rsk', 'table_name')
    create_sql = GetConfig('rsk', 'create_sql')
    insert_sql = GetConfig('rsk', 'insert_sql')
    update_separator_sql = GetConfig('rsk', 'update_separator_sql')

    db_config = 'rds_gydba'
    host = GetConfig(db_config, 'host')
    port = int(GetConfig(db_config, 'port'))
    user = GetConfig(db_config, 'user')
    password = GetConfig(db_config, 'password')
    db = GetConfig('yunying', 'db')

    in_type = 1
    if in_type == 1:
        dt = datetime.today().strftime('%Y%m%d')
    elif in_type == 2:
        dt = 'manual'
    file_name = file_name.replace('yymmdd', dt)
    table_name = "%s_%s" % (table_name, dt)

    # 连接数据库
    dbhelper = DBHelper(host, port, user, password, db)
    cur = dbhelper.conn_db()

    # 打开excel,获取数据
    excelhelper = ExcelHelper(file_dir, file_name)
    file = excelhelper.file_abspath()
    data = excelhelper.get_excel_data(sheet_index=0, column_index=3)

    # >>>>> 数据库
    # 判断表是否存在，不存在则创建，存在则清空表数据
    import_table_exists = dbhelper.table_exists(table_name)
    if import_table_exists == 0:
        with open("%s/%s" % (work_dir, create_sql), 'r', encoding='utf-8') as ct:
            create_table_sql = ct.read()
            create_table_sql = create_table_sql % table_name
            dbhelper.exec(create_table_sql)
    else:
        truncate_table_sql = "truncate table %s;" % table_name
        dbhelper.exec(truncate_table_sql)

    # 数据导入数据的表中
    with open("%s/%s" % (work_dir, insert_sql), 'r', encoding='utf-8') as ins:
        insert_data_sql = ins.read()
        insert_data_sql = insert_data_sql % (table_name, ','.join(data))
        # print(insert_data_sql)
        dbhelper.exec(insert_data_sql)

    # 数据清洗
    # 1 导入的数据是否为0
    max_column_sql = "select count(1) from %s;" % table_name
    dbhelper.exec(max_column_sql)
    max_column = dbhelper.get_total()
    if max_column == 0:
        exit('退出执行: 导入的数据量为0.')

    # 2 导入的公司名称是否重复
    repeat_company_sql = "select group_concat(distinct company_name) as repeat_name from %s " \
                         "group by company_name having count(*)>1;" % table_name
    dbhelper.exec(repeat_company_sql)
    repeat_companys = [repeat_company[0] for repeat_company in cur.fetchall()]
    if repeat_companys:
        exit("退出执行:导入的公司名称有重复.\n如下:\n%s" % '\n'.join(repeat_companys))

    # 3 更新导入数据中的间隔符号
    with open("%s/%s" % (work_dir, update_separator_sql), 'r', encoding='utf-8') as f:
        update_product_separator = f.read()
        update_product_separator = update_product_separator % table_name
        dbhelper.exec(update_product_separator)

    # 4 导入新增的公司信息
    new_company_sql = """
    SELECT COUNT(*) as cnt
    FROM %s a
    LEFT JOIN usr_company b
     ON a.`company_name` = b.`name`
    WHERE b.id IS NULL;
    """ % table_name
    dbhelper.exec(new_company_sql)
    new_company = dbhelper.get_total()
    if new_company > 0:
        # 插入新的公司ID
        insert_new_company_sql = """
        INSERT INTO usr_company(`name`,company_type_id,company_opentype,created_by,updated_by)
        SELECT a.company_name, 1 AS company_type_id, 5 AS company_opentype, 0 AS created_by, 0 AS updated_by
        FROM %s a
        LEFT JOIN usr_company b
         ON a.`company_name` = b.`name`
        WHERE b.id IS NULL;
        """ % table_name
        dbhelper.exec(insert_new_company_sql)
    # 5 更新导入表中的新表的ID
    update_import_company_sql = """
    UPDATE %s a
    INNER JOIN `usr_company` b
     ON a.`company_name` = b.name
    SET a.company_id = b.`id`;
    """ % table_name
    dbhelper.exec(update_import_company_sql)
    # 6 更新风控等级id
    update_rsk_sql = """
    UPDATE %s a
    INNER JOIN `rsk_info_rating` b
     ON a.`final_rsk` = b.`rank`
    SET a.`rsk_id`=b.id;
    """ % table_name
    dbhelper.exec(update_rsk_sql)

    # 7 拆分商品数据(中间使用的临时表)
    tmp_table_exists = dbhelper.table_exists('tmp_split_products')
    if tmp_table_exists == 0:
        create_table = """CREATE TABLE `tmp_split_products` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `sxy` VARCHAR(10) DEFAULT NULL,
          `cid` INT(11) DEFAULT NULL,
          `cname` VARCHAR(200) DEFAULT NULL,
          `pnames` VARCHAR(200) DEFAULT NULL,
          PRIMARY KEY (`id`)
        );
        """
        dbhelper.exec(create_table)
    else:
        dbhelper.exec("truncate table tmp_split_products;")

    tmp_table_exists = dbhelper.table_exists('tmp_split_product_list')
    if tmp_table_exists == 0:
        create_table = """CREATE TABLE `tmp_split_product_list` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `sxy` VARCHAR(100) DEFAULT NULL,
          `cid` BIGINT(20) DEFAULT NULL,
          `cname` VARCHAR(100) DEFAULT NULL,
          `pname` VARCHAR(100) DEFAULT NULL,
          `pid` BIGINT(20) DEFAULT NULL,
          `input_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        )COMMENT='风控-拆分产品结果';
            """
        dbhelper.exec(create_table)
    else:
        dbhelper.exec("truncate table tmp_split_products;")

    # 7.1 重新拆分数据：区分买卖商品
    instert_split_sql = """
    INSERT INTO tmp_split_products(sxy,cid,cname,pnames)
    SELECT 'buy', company_id ,company_name, buy_product
    FROM %s
    WHERE IFNULL(buy_product,'') != ''
    UNION ALL
    SELECT 'sell', company_id ,company_name, sell_product
    FROM %s
    WHERE IFNULL(sell_product,'') != '';
    """ % (table_name, table_name)
    dbhelper.exec(instert_split_sql)

    # 7.2 将商品分隔的展开
    dbhelper.exec("call sp_rsk_products_split();")

    # 7.3 更新商品的ID
    update_product_sql = """
    UPDATE tmp_split_product_list a
    INNER JOIN prd_product b
     ON a.`pname` = b.`product_name`
    SET a.pid=b.id;
    """
    dbhelper.exec(update_product_sql)

    # 导入数据到指定位置
    # 新增下游
    new_xy_sql = """
    SELECT COUNT(*) as new_xy
    FROM (
    SELECT pid,100 AS usr_company_id,cid,cname, 4 AS biz_type, IF(sxy='buy',2,3) AS trade_limit,0 AS created_by
    ,0 AS updated_by
    FROM `tmp_split_product_list`
    WHERE sxy = 'sell' AND pid IS NOT NULL
    ) a
    LEFT JOIN inf_counterparty_limit b
     ON a.pid=b.prd_product_id AND a.usr_company_id=b.usr_company_id AND a.cid = b.counterparty_id 
     AND a.biz_type=b.biz_type AND a.trade_limit = b.trade_limit AND b.valid=1
    WHERE b.id IS NULL;
    """
    dbhelper.exec(new_xy_sql)
    new_xy_total = dbhelper.get_total()
    if new_xy_total > 0:
        new_xy_insert_sql = """
        INSERT INTO inf_counterparty_limit(prd_product_id,usr_company_id,counterparty_id,counterparty_name,biz_type,trade_limit,created_by,updated_by)
        SELECT a.pid, a.usr_company_id, a.cid, a.cname, a.biz_type, a.trade_limit, a.created_by, a.updated_by
        FROM (
        SELECT pid,100 AS usr_company_id,cid,cname, 4 AS biz_type, IF(sxy='buy',2,3) AS trade_limit,0 AS created_by,0 AS updated_by
        FROM `tmp_split_product_list`
        WHERE sxy = 'sell' AND pid IS NOT NULL
        ) a
        LEFT JOIN inf_counterparty_limit b
         ON a.pid=b.prd_product_id AND a.usr_company_id=b.usr_company_id AND a.cid = b.counterparty_id AND a.biz_type=b.biz_type AND a.trade_limit = b.trade_limit AND b.valid=1
        WHERE b.id IS NULL;
        """
        dbhelper.exec(new_xy_insert_sql)

    # 新增上游
    new_sy_sql = """
    SELECT COUNT(*) as cnt
    FROM (
    SELECT pid,100 AS usr_company_id,cid,cname, 4 AS biz_type, IF(sxy='buy',2,3) AS trade_limit,0 AS created_by
    ,0 AS updated_by
    FROM `tmp_split_product_list`
    WHERE sxy = 'buy' AND pid IS NOT NULL
    ) a
    LEFT JOIN inf_counterparty_limit b
     ON a.pid=b.prd_product_id AND a.usr_company_id=b.usr_company_id AND a.cid = b.counterparty_id 
     AND a.biz_type=b.biz_type AND a.trade_limit = b.trade_limit AND b.valid=1
    WHERE b.id IS NULL;
    """
    dbhelper.exec(new_sy_sql)
    new_sy_total = dbhelper.get_total()

    if new_sy_total > 0:
        new_sy_insert_sql = """
        INSERT INTO inf_counterparty_limit(prd_product_id,usr_company_id,counterparty_id,counterparty_name,biz_type
        ,trade_limit,created_by,updated_by)
        SELECT a.pid, a.usr_company_id, a.cid, a.cname, a.biz_type, a.trade_limit, a.created_by, a.updated_by
        FROM (
        SELECT pid,100 AS usr_company_id,cid,cname, 4 AS biz_type, IF(sxy='buy',2,3) AS trade_limit,0 AS created_by
        ,0 AS updated_by
        FROM `tmp_split_product_list`
        WHERE sxy = 'buy' AND pid IS NOT NULL
        ) a
        LEFT JOIN inf_counterparty_limit b
         ON a.pid=b.prd_product_id AND a.usr_company_id=b.usr_company_id AND a.cid = b.counterparty_id 
         AND a.biz_type=b.biz_type AND a.trade_limit = b.trade_limit AND b.valid=1
        WHERE b.id IS NULL;
        """
        dbhelper.exec(new_sy_insert_sql)

    # 判断导入的数据是否符合导入
    rsk_exists_sql = """
    SELECT GROUP_CONCAT(DISTINCT final_rsk)
    FROM %s
    WHERE rsk_id IS NULL;
    """ % table_name
    dbhelper.exec(rsk_exists_sql)
    rsk_not_in_table = cur.fetchone()[0]
    if rsk_not_in_table:
        msg = "新增的数据中的风控等级不存在数据库字典中：\n%s\n" % rsk_not_in_table
        is_continue(msg)

    # 判断是否有到期时间是空的
    expired_time_sql = """
    SELECT COUNT(*) as cnt
    FROM %s
    WHERE expired_date IS NULL;
    """ % table_name
    dbhelper.exec(expired_time_sql)
    expired_time_not_exists = dbhelper.get_total()
    if expired_time_not_exists > 0:
        exit('退出:存在到期时间为空的数据。')

    # 判断是否存在评级信息变更
    rsk_modify_sql = """
    SELECT COUNT(*) as cnt
    FROM %s a
    INNER JOIN rsk_rating b
     ON a.company_id=b.company_id AND 
     (a.rsk_id != b.rating_id OR 
     DATE_FORMAT(DATE_SUB(a.expired_date,INTERVAL 6 MONTH),"%%Y%%m%%d") != DATE_FORMAT(b.latest_rating_time,"%%Y%%m%%d")
     )
     AND b.valid=1;
    """ % table_name
    dbhelper.exec(rsk_modify_sql)
    rsk_modify = dbhelper.get_total()

    # 记录变更前的信息
    log_table_exists = dbhelper.table_exists('rsk_rating_log')
    if log_table_exists == 0:
        create_log_table = """
        CREATE TABLE `rsk_rating_log` (
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `company_id` bigint(20) DEFAULT NULL,
          `before_rating_id` bigint(20) DEFAULT NULL,
          `after_rating_id` bigint(20) DEFAULT NULL,
          `before_date` datetime DEFAULT NULL,
          `after_date` datetime DEFAULT NULL,
          `source` varchar(50) DEFAULT NULL,
          PRIMARY KEY (`id`)
        )comment '风控数据变更记录';
        """
        dbhelper.exec(create_log_table)

    update_rskid = 0
    update_rsk_date = 0
    if rsk_modify > 0:
        log_insert_sql = """
        INSERT INTO rsk_rating_log(company_id,before_rating_id,after_rating_id,before_date, after_date,source)
        SELECT a.company_id,b.rating_id AS before_rating_id,a.rsk_id AS after_rating_id
        ,b.latest_rating_time AS before_date,DATE_SUB(a.expired_date,INTERVAL 6 MONTH) AS after_date
        ,'%s' AS source
        FROM %s a
        INNER JOIN rsk_rating b
         ON a.company_id=b.company_id 
         AND (a.rsk_id != b.rating_id OR 
         DATE_FORMAT(DATE_SUB(a.expired_date,INTERVAL 6 MONTH),"%%Y%%m%%d") 
         != DATE_FORMAT(b.latest_rating_time,"%%Y%%m%%d"))
         AND b.valid=1;
        """ % (table_name, table_name)
        dbhelper.exec(log_insert_sql)

        # 变更风控等级的数量
        update_rsk_id_sql = """
        SELECT COUNT(*) as cnt
        FROM %s a
        INNER JOIN rsk_rating b
         ON a.company_id=b.company_id AND a.rsk_id != b.rating_id
         AND b.valid=1;
        """ % table_name
        dbhelper.exec(update_rsk_id_sql)
        update_rskid = dbhelper.get_total()
        if update_rskid > 0:
            update_rsk_id_sql = """
            UPDATE %s a
            INNER JOIN rsk_rating b
             ON a.company_id=b.company_id AND a.rsk_id != b.rating_id
             AND b.valid=1
            SET b.rating_id=a.`rsk_id`;
            """ % table_name
            dbhelper.exec(update_rsk_id_sql)

        # 变更风控评级时间
        update_rsk_date_sql = """
        SELECT COUNT(*) as cnt
        FROM %s a
        INNER JOIN rsk_rating b
         ON a.company_id=b.company_id AND 
            DATE_FORMAT(DATE_SUB(a.expired_date,INTERVAL 6 MONTH),"%%Y%%m%%d") != DATE_FORMAT(b.latest_rating_time,"%%Y%%m%%d")
         AND b.valid=1;
        """ % table_name
        dbhelper.exec(update_rsk_date_sql)
        update_rsk_date = dbhelper.get_total()
        if update_rsk_date > 0:
            update_rsk_date_sql = """
            UPDATE %s a
            INNER JOIN rsk_rating b
             ON a.company_id=b.company_id AND 
             DATE_FORMAT(DATE_SUB(a.expired_date,INTERVAL 6 MONTH),"%%Y%%m%%d") != DATE_FORMAT(b.latest_rating_time,"%%Y%%m%%d")
             AND b.valid=1
            SET b.latest_rating_time= DATE_SUB(a.expired_date,INTERVAL 6 MONTH);
            """ % table_name
            dbhelper.exec(update_rsk_date_sql)

    # 新增风控数据
    new_rsk_info_sql = """
    SELECT COUNT(*) as cnt
    FROM %s a
    LEFT JOIN rsk_rating b
     ON a.`company_id`=b.`company_id`
      AND b.`valid`=1
    WHERE b.id IS NULL;
    """ % table_name
    dbhelper.exec(new_rsk_info_sql)
    new_rsk_info = dbhelper.get_total()
    if new_rsk_info > 0:
        new_rsk_info_sql = """
        INSERT INTO rsk_rating(company_id,rating_id,latest_rating_time,created_by,updated_by)
        SELECT a.company_id,a.rsk_id,DATE_SUB(a.expired_date,INTERVAL 6 MONTH) AS expired_date,0 AS created_by,0 AS updated_by
        FROM %s a
        LEFT JOIN rsk_rating b
         ON a.`company_id`=b.`company_id`
          AND b.`valid`=1
        WHERE b.id IS NULL;
        """ % table_name
        dbhelper.exec(new_rsk_info_sql)

    # 检测导入后的交易对手是否有重复
    is_repeat_counterparty = """
    SELECT COUNT(*) AS cnt
    FROM inf_counterparty_limit 
    WHERE valid=1
    GROUP BY prd_product_id,usr_company_id,counterparty_id,counterparty_name,biz_type,trade_limit
    HAVING COUNT(*)>1;
    """
    dbhelper.exec(is_repeat_counterparty)
    is_repeat_counterparty = dbhelper.get_total()

    # 检测导入后的风控数据是否重复
    is_repeat_rsk = """
    SELECT COUNT(*) cnt
    FROM rsk_rating
    WHERE valid=1
    GROUP BY company_id,rating_id,latest_rating_time
    HAVING COUNT(*)>1;
    """
    dbhelper.exec(is_repeat_rsk)
    is_repeat_rsk = dbhelper.get_total()


    # 拉黑处理
    rating_black_count = 0
    black_counterparty_total = 0

    if in_type == 1:
        last_import_table = """
        SELECT MAX(REPLACE(table_name,'imp_rsk_list_','')) AS col
        FROM information_schema.`TABLES`
        WHERE TABLE_SCHEMA='mall' AND table_name LIKE 'imp_rsk_list_%%' AND table_name NOT IN( 'imp_rsk_list_manual', '%s');   
        """ % table_name
        dbhelper.exec(last_import_table)
        last_import_table_name = cur.fetchone()
        last_import_table_name = "imp_rsk_list_%s" % str(last_import_table_name[0])

        # 判断是否有拉黑数据
        black_sql = """
        SELECT count(a.company_id) as cnt
        FROM %s a
        LEFT JOIN %s b
         ON a.`company_id`=b.company_id
        WHERE b.company_id IS NULL
        """ % (last_import_table_name, table_name)
        dbhelper.exec(black_sql)
        black_company = dbhelper.get_total()

        if black_company > 0:
            msg = "发现存在拉黑数据."
            is_continue(msg)

            # 拉黑的评级信息置为无效
            rating_black_sql = """
            SELECT COUNT(*) as cnt
            FROM rsk_rating a
            INNER JOIN (
            SELECT a.company_id
            FROM %s a
            LEFT JOIN %s b
             ON a.`company_id`=b.company_id
            WHERE b.company_id IS NULL
            ) b
             ON a.`company_id` = b.company_id
            WHERE a.valid=1;
            """ % (last_import_table_name, table_name)
            dbhelper.exec(rating_black_sql)
            rating_black_count = dbhelper.get_total()

            if rating_black_count > 0:
                rating_black_sql = """
                UPDATE rsk_rating a
                INNER JOIN (
                SELECT a.company_id
                FROM %s a
                LEFT JOIN %s b
                 ON a.`company_id`=b.company_id
                WHERE b.company_id IS NULL
                ) b
                 ON a.`company_id` = b.company_id
                SET a.valid = 0
                WHERE a.valid=1; 
                """ % (last_import_table_name, table_name)
                dbhelper.exec(rating_black_sql)

            # 拉黑交易对手信息更新为无效
            black_counterparty_sql = """
            SELECT COUNT(*) as cnt
            FROM inf_counterparty_limit a
            INNER JOIN ( SELECT a.company_id 
            FROM %s a 
            LEFT JOIN %s b  
            ON a.`company_id`=b.company_id 
            WHERE b.company_id IS NULL 
            ) b  ON a.`counterparty_id` = b.company_id
            WHERE a.`valid`=1;
            """ % (last_import_table_name, table_name)
            dbhelper.exec(black_counterparty_sql)
            black_counterparty_total = dbhelper.get_total()

            if black_counterparty_total > 0:
                black_counterparty_sql = """
                UPDATE inf_counterparty_limit a
                INNER JOIN (
                SELECT a.company_id
                FROM %s a
                LEFT JOIN %s b
                 ON a.`company_id`=b.company_id
                WHERE b.company_id IS NULL
                ) b 
                 ON a.`counterparty_id` = b.company_id
                 SET a.`valid`=0
                WHERE a.`valid`=1;
                """ % (last_import_table_name, table_name)
                dbhelper.exec(black_counterparty_sql)

    # 记录操作记录结果
    if in_type == 1:
        record_name = table_name
    elif in_type == 2:
        record_time = datetime.now().strftime("%Y%m%d%H%M")
        record_name = '%s_%s' % (table_name, record_time)

    record_log = """
    INSERT INTO `tmp_rsk_update_result` (`dt`,`ince_company`,rsk_changes,`rating_lv_change`
    ,`expired_time_change`,`ince_rsk`,`ince_sy`
    ,`ince_xy`,file_name,rating_black_count,limit_black_count)
    values (%d,%d,%d,%d,%d,%d,%d,%d,'%s',%d,%d);
    """ % (start_time, new_company, rsk_modify, update_rskid, update_rsk_date, new_rsk_info, new_sy_total
                            , new_xy_total, record_name, rating_black_count, black_counterparty_total)
    dbhelper.exec(record_log)

    # 关闭数据库连接
    dbhelper.close()

    # 打印结果:
    message = """
新增公司数量                  %d
新增评级数量                  %d
评级更新数量                  %d
评级等级变更的数量             %d
评级时间变更数量               %d
新增上游数量                  %d
新增下游数量                  %d
导入数据表名称                %s
评级拉黑数量                  %d
交易对手拉黑数量               %d
    """ % (new_company, new_rsk_info, rsk_modify, update_rskid, update_rsk_date
                            , new_sy_total, new_xy_total, record_name, rating_black_count, black_counterparty_total)
    print(message)
