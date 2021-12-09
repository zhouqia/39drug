# -*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import logging
from drug.items import DrugInstructions
from drug.items import DrugBarcode

# 累加器
def addDbNum():
    count = 0
    def ff(n):
        nonlocal count
        count += n
        return count
    return ff
add_db_num = addDbNum()

def addDbNum1():
    count1 = 0
    def ff1(n):
        nonlocal count1
        count1 += n
        return count1
    return ff1
add_db_num1 = addDbNum1()

# 药品说明
class DrugPipeline:
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host='10.1.1.156', user='root', passwd='iPh@23ysq!', db='drug', port=3306, charset='utf8')
        # 创建游标
        self.conn.autocommit(False)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, DrugInstructions):
            # logging.warn("第" + str(add_db_num(1)) + "次详情信息入db  drugId=" + item['drugId'])
            insert_sql = """
            insert ignore into drug_details(
            id,
            drug_name,
            drug_ingredients,
            drug_properties,
            drug_indications,
            drug_usage_and_dosage,
            drug_adverse_reactions,
            drug_taboo,
            drug_precautions,
            drug_for_special_populations,
            drug_interactions,
            drug_pharmacological_effects,
            drug_storage,
            drug_specification,
            drug_packaging_specifications,
            drug_expiry_date,
            drug_approval_number,
            drug_manufacturing_company,
            drug_type
            ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            try:
                # 执行插入数据到数据库操作
                self.cursor.execute(insert_sql, (item['drugId'],
                                                 item['drugName'],
                                                 item['drugIngredients'],
                                                 item['drugProperties'],
                                                 item['drugIndications'],
                                                 item['drugUsageAndDosage'],
                                                 item['drugAdverseReactions'],
                                                 item['drugTaboo'],
                                                 item['drugPrecautions'],
                                                 item['drugForSpecialPopulations'],
                                                 item['drugInteractions'],
                                                 item['drugPharmacologicalEffects'],
                                                 item['drugStorage'],
                                                 item['drugSpecification'],
                                                 item['drugPackagingSpecifications'],
                                                 item['drugExpiryDate'],
                                                 item['drugApprovalNumber'],
                                                 item['drugManufacturingCompany'],
                                                 item['drugType']
                                                 )
                                    )
                # 提交，不进行提交无法保存到数据库
                self.conn.commit()
            except Exception as e:
                print("Reason:", e)
        elif isinstance(item, DrugBarcode):
            # logging.warn("第" + str(add_db_num1(1)) + "次条码信息入db  drugId=" + item['drugId'])
            insert_sql = """
            insert ignore into drug_barcode(
            id,
            barcode_number,
            drug_name,
            company_name,
            proposed_price,
            drug_specification,
            packing_unit,
            remark
            ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """
            try:
                self.cursor.execute(insert_sql, (item['drugId'],
                                                 item['barcodeNumber'],
                                                 item['drugName'],
                                                 item['companyName'],
                                                 item['proposedPrice'],
                                                 item['drugSpecification'],
                                                 item['packingUnit'],
                                                 item['remark']
                                                 )
                                    )
                # 提交，不进行提交无法保存到数据库
                self.conn.commit()
            except Exception as e:
                print("Reason:", e)
        else:
            return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

