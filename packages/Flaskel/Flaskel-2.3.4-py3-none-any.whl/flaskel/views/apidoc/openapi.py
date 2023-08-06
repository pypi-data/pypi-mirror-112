class OpenApiBuilder:
    def __init__(self, title, version="1.0.0", description="", urls=None, **kwargs):
        """

        :param title:
        :param version:
        :param description:
        :param urls:
        :param paths:
        """
        self.title = title
        self.version = version
        self.description = description
        self.urls = urls or []
        self.default_tag = kwargs.get("default_tag") or "Services"
        self.content_type = kwargs.get("content_type") or "application/json"

        self._apidoc = {}

    @staticmethod
    def parameter(name, location="path", stype="integer", **kwargs):
        """

        :param name:
        :param location:
        :param stype:
        :return:
        """
        return {
            "in":          location,
            "name":        name,
            "required":    kwargs.get("required") or True,
            "description": kwargs.get("description") or "",
            "schema":      {
                "type": stype
            }
        }

    def response(self, code, content=None, **kwargs):
        """

        :param code:
        :param content:
        :param kwargs:
        :return:
        """
        content_type = kwargs.get("content_type") or self.content_type
        return {
            code: {
                "description": kwargs.get("description") or "",
                "content":     {
                    content_type: content or {}
                }
            }
        }

    def request_body(self, schema=None, example=None, **kwargs):
        """

        :param schema:
        :param example:
        :param kwargs:
        :return:
        """
        content_type = kwargs.get("content_type") or self.content_type
        return {
            "description": kwargs.get("description") or "",
            "required":    kwargs.get("required") or True,
            "content":     {
                content_type: {
                    "schema":  {"$ref": schema or ""},
                    "example": example or {}
                }
            }
        }

    def clear(self):
        """

        """
        self._apidoc = {}

    def build(self):
        """

        """
        return {
            "openapi": "3.0.1",
            "info":    {
                "title":       self.title,
                "description": self.description,
                "version":     self.version
            },
            "servers": [{"url": u} for u in self.urls],
            "paths":   self._apidoc
        }

    def add_service(self, method, url,
                    tags=None, params=None, responses=None,
                    request_body=None, **kwargs):
        """

        :param method:
        :param url:
        :param tags:
        :param params:
        :param responses:
        :param request_body:
        :return:
        """
        if request_body:
            kwargs["requestBody"] = request_body

        service = {
            method.lower(): {
                "tags":       tags or [self.default_tag],
                "parameters": params or [],
                "responses":  responses or {},
                **kwargs
            }
        }

        if url in self._apidoc:
            self._apidoc[url].update(service)
        else:
            self._apidoc.update({url: service})
