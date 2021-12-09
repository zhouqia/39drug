# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class DrugItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


#     药品详细说明
class DrugInstructions(scrapy.Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_metadata in self.fields.items():
            if not field_metadata.get('default'):
                self.setdefault(field_name, '空')
            else:
                self.setdefault(field_name, field_metadata.get('default'))

    drugId = scrapy.Field()
    # 药品名称
    drugName = scrapy.Field()
    # 成份
    drugIngredients = scrapy.Field()
    # 性状
    drugProperties = scrapy.Field()
    # 适应症
    drugIndications = scrapy.Field()
    # 用法用量
    drugUsageAndDosage = scrapy.Field()
    # 不良反应
    drugAdverseReactions = scrapy.Field()
    # 禁忌
    drugTaboo = scrapy.Field()
    # 注意事项
    drugPrecautions = scrapy.Field()
    # 特殊人群用药
    drugForSpecialPopulations = scrapy.Field()
    # 药物相互作用
    drugInteractions = scrapy.Field()
    # 药理作用
    drugPharmacologicalEffects = scrapy.Field()
    # 贮藏
    drugStorage = scrapy.Field()
    # 规格
    drugSpecification = scrapy.Field()
    # 包装规格
    drugPackagingSpecifications = scrapy.Field()
    # 有效期
    drugExpiryDate = scrapy.Field()
    # 批准文号
    drugApprovalNumber = scrapy.Field()
    # 生产企业
    drugManufacturingCompany = scrapy.Field()
    # 药品所属分类
    drugType = scrapy.Field()


#     药品条码
class DrugBarcode(scrapy.Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_metadata in self.fields.items():
            if not field_metadata.get('default'):
                self.setdefault(field_name, '空')
            else:
                self.setdefault(field_name, field_metadata.get('default'))

    drugId = scrapy.Field()
    # 商品条码号
    barcodeNumber = scrapy.Field()
    # 商品名称
    drugName = scrapy.Field()
    # 公司名称
    companyName = scrapy.Field()
    # 参考价格
    proposedPrice = scrapy.Field()
    # 产品规格
    drugSpecification = scrapy.Field()
    # 包装单位
    packingUnit = scrapy.Field()
    # 备注信息
    remark = scrapy.Field()
