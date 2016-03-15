# coding: utf-8

"""
Copyright 2015 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ref: https://github.com/swagger-api/swagger-codegen
"""

from __future__ import absolute_import

import os
import sys
import json
import mimetypes

from datetime import datetime
from datetime import date

# python 2 and python 3 compatibility library
from six import iteritems

import requests
import sphere_engine
import simplejson

try:
    # for python3
    from urllib.parse import quote
except ImportError:
    # for python2
    from urllib import quote

class ApiClient(object):
    
    access_token = None
    endpoint = None
    version = None
    
    host = None
    host_protocol = 'https'
    
    default_headers = {}
    
    """
    Generic API client for Swagger client library builds.

    Swagger generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the Swagger
    templates.

    NOTE: This class is auto generated by the swagger code generator program.
    Ref: https://github.com/swagger-api/swagger-codegen
    Do not edit the class manually.

    
    """
    def __init__(self, access_token, endpoint, version, api_type):
        """
        Constructor of the class.
        
        :param host: The base path for the server to call.
        :param header_name: a header to pass when making calls to the API.
        :param header_value: a header value to pass when making calls to the API.
        """
        
        self.access_token = access_token
        self.endpoint = endpoint
        self.version = version
        self.host = self.create_host(api_type, endpoint, version)
        
        # Set default User-Agent.
        self.user_agent = 'SphereEngine/3.0.0'

    def create_host(self, api_type, endpoint, version):
        
        host = '%s://%s.api.%s.sphere-engine.com/api/%s' % (
            self.host_protocol,
            endpoint,
            'compilers' if api_type == 'compilers' else 'problems',
            version
        )
        
        return host
    
    def call_api(self, resource_path, method,
                   path_params=None, query_params=None, header_params=None,
                   post_params=None, files=None,
                   response_type=None, auth_settings=None, callback=None):
        """
        Call method
        
            @param resource_path: sdfasdf
            :param resource_path dfawef
            :param method GET|POST
            :param path_params
            :param query_params
        """

        # headers parameters
        header_params = header_params or {}
        header_params.update(self.default_headers)
        #if self.cookie:
        #    header_params['Cookie'] = self.cookie
        if header_params:
            header_params = self.sanitize_for_serialization(header_params)

        # path parameters
        if path_params:
            for k, v in iteritems(path_params):
                replacement = quote(str(self.to_path_value(v)))
                resource_path = resource_path.replace('{' + k + '}', replacement)

        # query parameters
        #if query_params:
        #    query_params = {k: self.to_path_value(v)
        #                    for k, v in iteritems(query_params)}
        if not query_params:
            query_params = {}
        if self.access_token:
            query_params['access_token'] = self.access_token

        # post parameters
        if post_params or files:
            post_params = self.sanitize_for_serialization(post_params)

        ## body
        #if body:
        #    body = self.sanitize_for_serialization(body)

        # request url
        url = self.host + resource_path

        # perform request and return response
        response_data = self.request(method, url,
                                     query_params=query_params,
                                     headers=header_params,
                                     post_params=post_params)#, body=body)
        
        try:
            data =  response_data.json()
        except simplejson.scanner.JSONDecodeError, e:
            raise sphere_engine.SphereEngineException(e)
        
        return data

        """
        # deserialize response data
        if response_type:
            deserialized_data = self.deserialize(response_data, response_type)
        else:
            deserialized_data = None

        if callback:
            callback(deserialized_data)
        else:
            return deserialized_data
        """

    def request(self, method, url, query_params=None, headers=None,
                post_params=None, body=None):
        """
        Makes the HTTP request using requests library.
        
        :raise requests.exceptions.RequestException
        :raise sphere_engine.SphereEngineException
        """
        
        r = None
        
        if method == "GET":
            r = requests.get(url, params=query_params, headers=headers)
        
        elif method == "HEAD":
            r = requests.head(url, params=query_params, headers=headers)
        
        #elif method == "OPTIONS":
        #    return self.rest_client.OPTIONS(url,
        #                                    query_params=query_params,
        #                                    headers=headers,
        #                                    post_params=post_params,
        #                                    body=body)
        
        elif method == "POST":
            r = requests.post(url, params=query_params, headers=headers, data=post_params, )
            
        elif method == "PUT":
            r = requests.put(url, params=query_params, headers=headers, data=post_params, )
        
        #elif method == "PATCH":
        #    return self.rest_client.PATCH(url,
        #                                  query_params=query_params,
        #                                  headers=headers,
        #                                  post_params=post_params,
        #                                  body=body)
        
        elif method == "DELETE":
            r = requests.delete(url, params=query_params, headers=headers)
        
        else:
            raise ValueError(
                "http method must be `GET`, `HEAD`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )
        
        if r.status_code not in range(200, 206):
            raise sphere_engine.SphereEngineException(r.reason, r.status_code)
        
        #print r.text
        #print r.status_code
        
        return r
            
            
            
            
            
            
            
            
            








    @property
    def user_agent(self):
        """
        Gets user agent.
        """
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        """
        Sets user agent.
        """
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    

    def to_path_value(self, obj):
        """
        Takes value and turn it into a string suitable for inclusion in
        the path, by url-encoding.

        :param obj: object or string value.

        :return string: quoted value.
        """
        if type(obj) == list:
            return ','.join(obj)
        else:
            return str(obj)

    def sanitize_for_serialization(self, obj):
        """
        Builds a JSON POST object.

        If obj is None, return None.
        If obj is str, int, float, bool, return directly.
        If obj is datetime.datetime, datetime.date
            convert to string in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is swagger model, return the properties dict.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        types = (str, int, float, bool, tuple)
        if sys.version_info < (3,0):
            types = types + (unicode,)
        if isinstance(obj, type(None)):
            return None
        elif isinstance(obj, types):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj)
                    for sub_obj in obj]
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        else:
            if isinstance(obj, dict):
                obj_dict = obj
            else:
                # Convert model obj to dict except
                # attributes `swagger_types`, `attribute_map`
                # and attributes which value is not None.
                # Convert attribute name to json key in
                # model definition for request.
                obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                            for attr, _ in iteritems(obj.swagger_types)
                            if getattr(obj, attr) is not None}

            return {key: self.sanitize_for_serialization(val)
                    for key, val in iteritems(obj_dict)}

    def deserialize(self, response, response_type):
        """
        Deserializes response into an object.

        :param response: RESTResponse object to be deserialized.
        :param response_type: class literal for
            deserialzied object, or string of class name.

        :return: deserialized object.
        """
        # handle file downloading
        # save response body into a tmp file and return the instance
        if "file" == response_type:
            return self.__deserialize_file(response)

        # fetch data from response object
        try:
            data = json.loads(response.data)
        except ValueError:
            data = response.data

        return data
        