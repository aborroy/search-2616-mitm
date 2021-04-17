from mitmproxy import http, ctx
from uuid import uuid4
from random import choice, randint, randrange
import time
from datetime import datetime, timedelta
import re
from json import dumps, loads
from os import environ
from json import dumps
from jinja2 import Environment, FileSystemLoader
import csv
import subprocess
import sys


class TextContent:

    def __init__(self):
        self.sentences = self.generate_sentences()
        self.template_generator = DocxTemplate(self.read_csv(), self.sentences)
        self.env = Environment(loader=FileSystemLoader('/tmp/'))
        self.metadata = self.read_metadata_csv()
        self.start_time = time.time()
        self.content_id = 0
        self.root_id, self.site_id = f"{uuid4()}", f"{uuid4()}"
        self.site = {}
        self.level_7 = f"{uuid4()}"
        self.level_7_count = 100
        self.docs_in_site = 0
        self.set_new_site()
        self.parent_assocs_crc = randint(1000000000, 9999999999)

    def request(self, flow: http.HTTPFlow) -> None:
        endpoint = flow.request.path
        port = 9999
        url = flow.request.url
        for each in ["172.17.0.1", "172.17.0.2", "172.17.0.3", "172.17.0.4", "172.17.0.5", "172.17.0.6"]:
            url = url.replace(each, environ['REPO_URL'])
        mock = True if int(time.time() - self.start_time) > 60 else False
        if mock and "textContent" in endpoint:
            rnd = randint(1, 100)
            text_content = self.get_text_content() if rnd < 90 else self.generate_template()
            flow.response = http.HTTPResponse.make(
                200,
                text_content,
                {"Content-Type": "text/plain", "charset": "UTF-8"}
            )
        elif mock and "alfresco/service/api/solr/metadata" in endpoint:
            body_req = flow.request.get_text()
            metadata_content = bytes(self.get_metadata_content(loads(body_req)), encoding="utf-8")
            flow.response = http.HTTPResponse.make(
                200,
                metadata_content,
                {"Content-Type": "application/json", "charset": "UTF-8"}
            )
        else:
            flow.request.url = url
            flow.request.port = port


    def set_new_site(self):
        self.site["site_name"] = f"Site-{int(time.time())}{randint(100,999)}"
        self.site["level_3"] = str(uuid4())
        self.site["level_4"] = str(uuid4())
        self.site["level_4_name"] = f"Test_{(uuid4())}"
        self.site["level_5"] = str(uuid4())
        self.site["level_5_name"] = f"L2_User{randint(1, 20)}"
        self.site["level_6"] = str(uuid4())
        self.site["level_6_name"] = f"L3_{randint(1, 20)}"
        self.docs_in_site = randint(5000, 100000)

    def set_new_level_7(self):
        self.level_7 = f"{uuid4()}"
        self.parent_assocs_crc = randint(1000000000, 9999999999)
        self.level_7_count = 100

    # def get_root_and_site_id(self):
    #     root_id, site_id = "", ""
    #     headers = {'Content-type': 'application/json'}
    #     url = "http://admin:admin@env-acs-index3-alb-796664598.eu-west-2.elb.amazonaws.com/alfresco/api/-default-/public/alfresco/versions/1/nodes/-my-/children?skipCount=0&maxItems=100"
    #     subprocess.check_call(["/usr/bin/python3.8", "-m", "pip", "install", "requests"])
    #     import requests
    #     res = requests.get(url, headers).json()
    #     for each in res["list"]["entries"]:
    #         if each["entry"]["name"] == "Sites":
    #             root_id = each["entry"]["parentId"]
    #             site_id = each["entry"]["id"]
    #     return root_id, site_id

    def generate_sentences(self):
        _tmp = []
        with open('/tmp/top-10000-english-words.txt') as f:
            words = f.readlines()
        words = [w.replace("\n", "").replace("\r", "") for w in words]
        for i in range(5, 15):
            for j in range(200):
                sentence = choice(words)
                for _ in range(i):
                    sentence += f" {choice(words)}"
                _tmp.append(sentence.capitalize())

        return _tmp

    def read_csv(self):
        with open('/tmp/city-names.txt') as f:
            city_names = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]
        with open('/tmp/female-first-names.txt') as f:
            female_first_names = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]
        with open('/tmp/last-names.txt') as f:
            last_names = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]
        with open('/tmp/male-first-names.txt') as f:
            male_first_names = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]
        with open('/tmp/state-names.txt') as f:
            state_names = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]
        with open('/tmp/street-addresses.txt') as f:
            street_addresses = [w.replace("\n", "").replace("\r", "") for w in f.readlines()]

        data = {'city_names': city_names, 'female_names': female_first_names, 'last_names': last_names,
                'male_names': male_first_names, 'state_names': state_names, 'street_addresses': street_addresses}

        return data

    def read_metadata_csv(self):
        METADATA_FIELDNAMES = 'name', 'created', 'creator', "modified", "modifier", "accessed", "title", "description", \
                              "publisher", 'contributor', 'type', 'from', "hits", "to", "identifier"

        file_names = 'docx', 'pptx', 'pdf', 'jpg'
        records = []
        for each in file_names:
            with open(f"/tmp/{each}.csv") as f:
                for entry in csv.DictReader(f, delimiter=",", fieldnames=METADATA_FIELDNAMES, restval=""):
                    records.append(entry)
        return records

    def get_text_content(self):
        text_content = ""
        paragraph_count = randint(10, 60)
        for i in range(paragraph_count):
            sentence_count = randint(3, 7)
            for j in range(sentence_count):
                text_content += f"{choice(self.sentences)}. "
            text_content += "\n\n"

        return bytes(text_content, encoding="utf-8")

    def generate_template(self):
        template_name = "template_" + str(randint(1, 3))
        template = self.env.get_template(template_name + ".txt")
        return bytes(template.render(template_generator=self.template_generator), encoding="utf-8")

    def get_metadata_content(self, body_req):
        metadata_content = {"nodes": []}
        if "toNodeId" in list(body_req.keys()):
            if self.docs_in_site <= 0:
                self.set_new_site()
            if self.level_7_count <= 0:
                self.set_new_level_7()
            self.docs_in_site -= 1
            self.level_7_count -= 1
            _id = body_req["toNodeId"]
            metadata_content["nodes"].append(self.generate_metadata(_id))
        elif "nodeIds" in list(body_req.keys()):
            ids = body_req["nodeIds"]
            for _id in ids:
                if self.docs_in_site <= 0:
                    self.set_new_site()
                if self.level_7_count <= 0:
                    self.set_new_level_7()
                self.docs_in_site -= 1
                self.level_7_count -= 1

                metadata_content["nodes"].append(self.generate_metadata(_id))

        return dumps(metadata_content)

    def generate_metadata(self, _id):
        metadata_model = self.choose_metadata_model(33, 33)
        if metadata_model == "A":
            _metadata = self.generate_A_model(_id, choice(self.metadata))
        elif metadata_model == "B":
            _metadata = self.generate_B_model(_id, choice(self.metadata))
        else:
            _metadata = self.generate_C_model(_id, choice(self.metadata))
        return _metadata

    @staticmethod
    def choose_metadata_model(a, b):
        rnd = randint(1, 100)
        if rnd < a:
            return 'A'
        elif rnd < a + b:
            return 'B'
        else:
            return 'C'

    @staticmethod
    def mimetype_mapper(extension):
        mimetype_dict = {
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pdf": "application/pdf",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "jpg": "image/jpeg"
        }
        return mimetype_dict.get(extension)

    def generate_A_model(self, _id, metadata):
        name = metadata["name"]
        _metadata = {
            "id": _id,
            "tenantDomain": "",
            "nodeRef": f"workspace://SpacesStore/{metadata['identifier']}",
            "type": "cm:content",
            "aclId": 11,
            "txnId": 1,
            "aspects": ["cm:titled", "cm:dublincore", "cm:countable", "cm:auditable", "sys:referenceable", "sys:localized", "cm:author", "cm:effectivity"],
            "paths": [{"apath": f"/{self.root_id}/{self.site_id}/{self.site['site_name']}/{self.site['level_3']}/{self.site['level_4']}/{self.site['level_5']}/{self.site['level_6']}/{self.level_7}",
                       "path": "/{http://www.alfresco.org/model/application/1.0}company_home/{http://www.alfresco.org/model/site/1.0}sites/{http://www.alfresco.org/model/content/1.0}" + self.site["site_name"] + "/{http://www.alfresco.org/model/content/1.0}documentLibrary/{http://www.alfresco.org/model/content/1.0}" + self.site['level_4_name'] + "/{http://www.alfresco.org/model/content/1.0}" + self.site['level_5_name'] + "/{http://www.alfresco.org/model/content/1.0}" + self.site['level_6_name'] + "/{http://www.alfresco.org/model/content/1.0}" + name.replace(" ", "_x0020")}],
            "ancestors": [f"workspace://SpacesStore/{self.root_id}", f"workspace://SpacesStore/{self.site_id}", f"workspace://SpacesStore/{self.site['site_name']}", f"workspace://SpacesStore/{self.site['level_3']}", f"workspace://SpacesStore/{self.site['level_4']}", f"workspace://SpacesStore/{self.site['level_5']}", f"workspace://SpacesStore/{self.site['level_6']}", f"workspace://SpacesStore/{self.level_7}"],
            "namePaths": [{"namePath": ["Company Home", "Sites", self.site["site_name"], "documentLibrary", self.site['level_4_name'], self.site['level_5_name'], self.site['level_6_name'], name]}],
            "parentAssocsCrc": self.parent_assocs_crc,
            "owner": metadata["creator"],
            "parentAssocs": [
                "workspace://SpacesStore/" + self.site["level_6"] + "|workspace://SpacesStore/" + metadata["identifier"]
                + "|{http://www.alfresco.org/model/content/1.0}contains|{http://www.alfresco.org/model/content/1.0}"
                + name + "|true|-1"
            ]
        }
        created = str(metadata["created"]) if "Z" in str(metadata["created"]) else str(metadata["created"]) + "Z"
        modified = str(metadata["modified"]) if "Z" in str(metadata["modified"]) else str(metadata["modified"]) + "Z"
        accessed = str(metadata["accessed"]) if "Z" in str(metadata["accessed"]) else str(metadata["accessed"]) + "Z"
        self.content_id += 1
        _metadata["properties"] = {
            "{http://www.alfresco.org/model/system/1.0}store-protocol": "workspace",
            "{http://www.alfresco.org/model/system/1.0}node-dbid": str(_id),
            "{http://www.alfresco.org/model/content/1.0}content": {
                "contentId": str(self.content_id),
                "encoding": "UTF-8",
                "locale": "en_GB_",
                "mimetype": self.mimetype_mapper(name.split(".")[1]),
                "size": str(randint(100000, 10000000))
            },
            "{http://www.alfresco.org/model/content/1.0}name": name,
            "{http://www.alfresco.org/model/content/1.0}modified": modified,
            "{http://www.alfresco.org/model/content/1.0}creator": metadata["creator"],
            "{http://www.alfresco.org/model/content/1.0}description": [{"locale": "en_", "value": metadata["description"]}],
            "{http://www.alfresco.org/model/content/1.0}created": created,
            "{http://www.alfresco.org/model/content/1.0}accessed": accessed,
            "{http://www.alfresco.org/model/system/1.0}store-identifier": "SpacesStore",
            "{http://www.alfresco.org/model/content/1.0}title": [{"locale": "en_", "value": metadata["title"]}],
            "{http://www.alfresco.org/model/system/1.0}locale": "en_GB_",
            "{http://www.alfresco.org/model/content/1.0}modifier": metadata["modifier"],
            "{http://www.alfresco.org/model/system/1.0}node-uuid": metadata["identifier"]
        }
        return _metadata

    def generate_B_model(self, _id, metadata):
        _metadata = self.generate_A_model(_id, metadata)
        _from = str(metadata["from"]) if "Z" in str(metadata["from"]) else str(metadata["from"]) + "Z"
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}publisher"] = metadata["publisher"]
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}contributor"] = metadata["contributor"]
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}type"] = metadata["type"]
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}from"] = _from
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}hits"] = str(metadata["hits"])
        return _metadata

    def generate_C_model(self, _id, metadata):
        _metadata = self.generate_B_model(_id, metadata)
        _to = str(metadata["to"]) if "Z" in str(metadata["to"]) else str(metadata["to"]) + "Z"
        _metadata["properties"]["{http://www.alfresco.org/model/content/1.0}to"] = _to
        return _metadata


class DocxTemplate:

    def __init__(self, data, sentences):
        self.data = data
        self.sentences = sentences

    def getName(self):
        rnd = randint(0, 1)
        if rnd == 0:
            f_name = choice(self.data['female_names'])
        else:
            f_name = choice(self.data['male_names'])
        name = f_name + " " + choice(self.data['last_names'])
        return name

    def getMoneyAmount(self):
        return randint(1000, 10000)

    def getStreetAddress(self):
        return choice(self.data['street_addresses'])

    def getCity(self):
        return choice(self.data['city_names'])

    def getState(self):
        return choice(self.data['state_names'])

    def getAddress(self):
        return self.getStreetAddress() + ", " + self.getCity() + ", " + self.getState()

    def getPhoneNumber(self):
        n = '0000000000'
        while '9' in n[3:6] or n[3:6] == '000' or n[6] == n[7] == n[8] == n[9]:
            n = str(randint(10 ** 9, 10 ** 10 - 1))
        return '+1 ' + n[:3] + '-' + n[3:6] + '-' + n[6:]

    def getYear(self):
        return randint(2000, 2020)

    def getWord(self, count=1):
        sentence = ""
        words = choice(self.sentences).split(" ")
        for i in range(count):
            sentence += choice(words) + " "
        return sentence.strip()

    def getDate(self):
        start = datetime.strptime('1/1/2000', '%m/%d/%Y')
        end = datetime.strptime('1/1/2020', '%m/%d/%Y')
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return str(start + timedelta(seconds=random_second)).split(" ")[0]

    def getInt(self, _min=1, _max=100):
        return randint(_min, _max)


addons = [
    TextContent()
]
