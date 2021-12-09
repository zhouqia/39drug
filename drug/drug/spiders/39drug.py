# -*- coding:utf-8 -*-

import scrapy
import logging
from drug.items import DrugInstructions
from drug.items import DrugBarcode


# 累加器
def addNum_1():
    count = 0
    def ff(n):
        nonlocal count
        count += n
        return count
    return ff
add_num1 = addNum_1()
# 累加器
def addNum_2():
    count1 = 0
    def ff1(n):
        nonlocal count1
        count1 += n
        return count1
    return ff1
add_num2 = addNum_2()

def drugNum():
    count2 = 0
    def drug_f(n):
        nonlocal count2
        count2 += n
        return count2
    return drug_f
drug_num = drugNum()

class Drug(scrapy.Spider):
    name = "39drug"
    allowed_domains = ['ypk.39.net']
    start_urls = ['http://ypk.39.net/AllCategory']

# 默认执行方法(开始--1.获取分类列表)
    def parse(self, response, **kwargs):
        li_list = response.xpath("//div[@id='d1']/ul[2]/li")
        for li in li_list:
            type = li.xpath("./strong/a[1]/text()")
            href_list = li.xpath("./p[@class='disease-item']/a")
            # print(str(type))
            for href in href_list:
                child_type = href.xpath("./text()").get()
                # print(str(child_type))
                target_url = href.xpath("./@href").get()
                url = "http://ypk.39.net" + str(target_url)
                yield scrapy.Request(url, meta={"drug_type": target_url.replace('/', ''), 'child_type': str(child_type)}, callback=self.parse_type_list)

# 2.1.获取指定分类下面的药品列表
    def parse_type_list(self, response):
        drug_type = response.meta["drug_type"]
        child_type = response.meta["child_type"]
        page = int(response.xpath("//p[@class='drugs-left-r']/span/text()").get().replace('/', ''))
        cur_page = int(response.xpath("//p[@class='drugs-left-r']/span/i/text()").get())
        cur_url = response.url
        drug_num_n = drug_num(page * 16)
        logging.warn("药品分类:   " + child_type + " 总共页数：  " + str(page) + " 当前页数：   " + str(cur_page) + "    地址: " + response.url + "    此类药品数量：" + str(page * 16) + "    药品数量大致总数:" + str(drug_num_n))
        print("药品分类:   " + child_type + " 总共页数：  " + str(page) + " 当前页数：   " + str(cur_page) + "    地址: " + response.url + "    此类药品数量：" + str(page * 16) + "    药品数量大致总数:" + str(drug_num_n))

        for drug in response.xpath("//ul[@class='drugs-ul']/li"):
            drug_id = str(drug.xpath("./a/@href").get()).replace("http://ypk.39.net/", "").replace("/", "")

            # 说明书地址
            instructions_url = drug.xpath("./a/@href").get()
            if instructions_url is not None:
                logging.warn("drug_type: " + drug_type + "  药品有说明书信息，drug_id： " + str(drug_id) + " instructions_url:" + instructions_url)
                print("drug_type: " + drug_type + "  药品有说明书信息，drug_id： " + str(drug_id) + " instructions_url:" + instructions_url)
                yield scrapy.Request(str(instructions_url) + "manual/", meta={"drug_type": drug_type, "drug_id": drug_id}, callback=self.parse_instructions)
            else:
                logging.warn("drug_type: " + drug_type + "  药品没有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品没有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
            # 条码地址
            barcode_url = drug.xpath("./a/@href").get()
            if barcode_url is not None:
                logging.warn("drug_type: " + drug_type + "  药品有条码信息，drug_id： " + str(drug_id) + " barcode_url:" + barcode_url)
                print("drug_type: " + drug_type + "  药品有条码信息，drug_id： " + str(drug_id) + " barcode_url:" + barcode_url)
                yield scrapy.Request(str(barcode_url) + "gs1/", meta={"drug_id": drug_id}, callback=self.parse_barcode)
            else:
                logging.warn("drug_type: " + drug_type + "  药品没有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品没有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)

        # for num in range(cur_page+1, page+1):
        for num in range(page, cur_page, -1):
            logging.warn("药品分类:   " + child_type + "  总共页数：  " + str(page) + " 当前页数：   " + str(num) + " 地址：" + str(cur_url) + "p" + str(num)+"/")
            print("药品分类:   " + child_type + "  总共页数：  " + str(page) + " 当前页数：   " + str(num) + " 地址：" + str(cur_url) + "p" + str(num)+"/")
            yield scrapy.Request(str(cur_url) + "p" + str(num)+"/", meta={"drug_type": drug_type, "cur_page": num}, callback=self.parse_type_list_other_page)

# 2.2.非首页列表查询+药品查询
    def parse_type_list_other_page(self, response):
        # print(response.url)
        drug_type = response.meta["drug_type"]
        cur_page = response.meta["cur_page"]
        for drug in response.xpath("//ul[@class='drugs-ul']/li"):
            drug_id = str(drug.xpath("./a/@href").get()).replace("http://ypk.39.net/", "").replace("/", "")

            # 说明书地址
            instructions_url = drug.xpath("./a/@href").get()
            if instructions_url is not None:
                logging.warn("drug_type: " + drug_type + "  药品有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                yield scrapy.Request(str(instructions_url) + "manual/", meta={"drug_type": drug_type, "drug_id": drug_id},callback=self.parse_instructions)
            else:
                logging.warn("drug_type: " + drug_type + "  药品没有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品没有说明书信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
            # 条码地址
            barcode_url = drug.xpath("./a/@href").get()
            if barcode_url is not None:
                logging.warn("drug_type: " + drug_type + "  药品有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                yield scrapy.Request(str(barcode_url) + "gs1/", meta={"drug_id": drug_id}, callback=self.parse_barcode)
            else:
                logging.warn("drug_type: " + drug_type + "  药品没有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)
                print("drug_type: " + drug_type + "  药品没有条码信息，drug_id： " + str(drug_id) + " response.url:" + response.url)

# 3.1.获取指定药品的说明书信息
    def parse_instructions(self, response):
        add_num_1 = add_num1(1)
        logging.warn("处理说明书信息第" + str(add_num_1) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"])
        print("处理说明书信息第" + str(add_num_1) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"])
        drug_type = response.meta["drug_type"]
        drug_id = response.meta["drug_id"]
        drugInstructions = DrugInstructions()
        drugInstructions['drugId'] = drug_id

        data_list = response.xpath("//ul[@class='drug-explain']/li")
        for data in data_list:
            if data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【药品名称】") >= 0:
                drug_name = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_name is not None:
                    drugInstructions['drugName'] = drug_name.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【成份】") >= 0:
                drug_ingredients = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_ingredients is not None:
                    drugInstructions['drugIngredients'] = drug_ingredients.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【性状】") >= 0:
                drug_properties = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_properties is not None:
                    drugInstructions['drugProperties'] = drug_properties.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【适应症】") >= 0:
                drug_indications = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_indications is not None:
                    drugInstructions['drugIndications'] = drug_indications.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【用法用量】") >= 0:
                drug_usage_and_dosage = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_usage_and_dosage is not None:
                    drugInstructions['drugUsageAndDosage'] = drug_usage_and_dosage.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【不良反应】") >= 0:
                drug_adverse_reactions = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_adverse_reactions is not None:
                    drugInstructions['drugAdverseReactions'] = drug_adverse_reactions.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【禁忌】") >= 0:
                drug_taboo = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_taboo is not None:
                    drugInstructions['drugTaboo'] = drug_taboo.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【注意事项】") >= 0:
                drug_precautions = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_precautions is not None:
                    drugInstructions['drugPrecautions'] = drug_precautions.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【特殊人群用药】") >= 0:
                drug_for_special_populations = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_for_special_populations is not None:
                    drugInstructions['drugForSpecialPopulations'] = drug_for_special_populations.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【药物相互作用】") >= 0:
                drug_interactions = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_interactions is not None:
                    drugInstructions['drugInteractions'] = drug_interactions.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【药理作用】") >= 0:
                drug_pharmacological_effects = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_pharmacological_effects is not None:
                    drugInstructions['drugPharmacologicalEffects'] = drug_pharmacological_effects.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【贮藏】") >= 0:
                drug_storage = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_storage is not None:
                    drugInstructions['drugStorage'] = drug_storage.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【规格】") >= 0:
                drug_specification = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_specification is not None:
                    drugInstructions['drugSpecification'] = drug_specification.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【包装规格】") >= 0:
                drug_packaging_specifications = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_packaging_specifications is not None:
                    drugInstructions['drugPackagingSpecifications'] = drug_packaging_specifications.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【有效期】") >= 0:
                drug_expiry_date = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_expiry_date is not None:
                    drugInstructions['drugExpiryDate'] = drug_expiry_date.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【批准文号】") >= 0:
                drug_approval_number = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_approval_number is not None:
                    drugInstructions['drugApprovalNumber'] = drug_approval_number.strip()
            elif data.xpath("./p[@class='drug-explain-tit']/text()").extract_first().find("【生产企业】") >= 0:
                drug_manufacturing_company = data.xpath("./p[@class='drug-explain-txt']/text()").extract_first()
                if drug_manufacturing_company is not None:
                    drugInstructions['drugManufacturingCompany'] = drug_manufacturing_company.strip()
        # 药品所属分类
        drugInstructions['drugType'] = drug_type
        yield drugInstructions

# 3.2.获取指定药品的条码信息
    def parse_barcode(self, response):
        drug_id = response.meta["drug_id"]
        if response.xpath("//div[@class='barcode-all-r']").get() is not None:
            add_num_2 = add_num2(1)
            logging.warn("处理条码信息第" + str(add_num_2) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"] + "    有条码信息")
            print("处理条码信息第" + str(add_num_2) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"] + "    有条码信息")
            drugBarcode = DrugBarcode()
            drugBarcode['drugId'] = drug_id
            data_list = response.xpath("//div[@class='barcode-all-r']/p")
            for d in data_list:
                data = d.xpath("./text()").extract_first()
                if data.find("商品条码号") >= 0:
                    drugBarcode['barcodeNumber'] = data.strip()
                elif data.find("商品名称") >= 0:
                    drugBarcode['drugName'] = data.strip()
                elif data.find("公司名称") >= 0:
                    drugBarcode['companyName'] = data.strip()
                elif data.find("参考价格") >= 0:
                    drugBarcode['proposedPrice'] = data.strip()
                elif data.find("产品规格") >= 0:
                    drugBarcode['drugSpecification'] = data.strip()
                elif data.find("包装单位") >= 0:
                    drugBarcode['packingUnit'] = data.strip()
                elif data.find("备注信息") >= 0:
                    drugBarcode['remark'] = data.strip()
            yield drugBarcode
        else:
            add_num_2 = add_num2(1)
            logging.warn("处理条码信息第" + str(add_num_2) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"] + "    无条码信息")
            print("处理条码信息第" + str(add_num_2) + "次请求" + " response.code:" + str(response.status) + "    drug_id:" + response.meta["drug_id"] + "    无条码信息")



