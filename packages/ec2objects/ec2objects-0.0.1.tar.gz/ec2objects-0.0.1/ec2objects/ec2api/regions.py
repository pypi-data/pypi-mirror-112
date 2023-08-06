from __future__ import annotations

from .ec2apiconnection import EC2ApiConnection
from bs4 import BeautifulSoup
import os
import time
import queue
import threading
import datetime
import random
import json


class Regions(EC2ApiConnection):
    def __init__(self):
        EC2ApiConnection.__init__(self)

    def list_all_regions(self):
        params = {}
        params["Action"] = "DescribeRegions"
        params["Region"] = "us-east-1"
        response = self.get_request(params=params)
        if response:
            # OK, don't like xml - modifyting the response.content to json
            old_contect = response.content
            xml_content = BeautifulSoup(old_contect, "xml")
            region_name = xml_content.findAll("regionName")
            region_endpoint = xml_content.findAll("regionEndpoint")
            region_info_list = []
            for i in range(0, len(region_name)):
                region_info = {}
                region_info["regionName"] = region_name[i].get_text()
                region_info["regionEndpoint"] = region_endpoint[i].get_text()
                region_info_list.append(region_info)
            response._content = json.dumps(region_info_list)
        return response
