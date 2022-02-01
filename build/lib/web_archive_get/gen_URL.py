

class parameter_pass:
    def __init__(self, url, matchType="exact") -> None:
        self.url = url
        self._to = None
        self._from = None
        self._limit = None
        self._sort = None
        self.matchType = matchType
        self._fls = []
        self._fliters = []

    def add_fliter_url(self,  value, operator=""):
        self._fliters.append(
            {
                "parameter": "url",
                "operator": operator,
                "value": value,
            })

    def add_fliter_mime(self,  value, operator=""):
        self._fliters.append(
            {
                "parameter": "mime",
                "operator": operator,
                "value": value,
            })

    def add_fliter_status(self,  value, operator=""):
        self._fliters.append(
            {
                "parameter": "status",
                "operator": operator,
                "value": value,
            })

    def add_fliter(self, value, operator=""):
        self._fliters.append(
            {
                "parameter": "url",
                "operator": operator,
                "value": value,
            })

    def add_from(self,  value):
        pass

    def add_to(self, value):
        pass

    def add_limit(self, value):
        pass

    def add_sort(self, value):
        pass

    def add_fl(self, value):
        pass

    def gen_page_count(self, url,  filter_ps=[], output="json"):
        url_ = url + "?url=" + self.url + "&showNumPages=true"
        for fliter in self._fliters:
            operator = fliter["operator"]
            parameter = fliter["parameter"]
            value = fliter["value"]
            for filter_p in filter_ps:
                if filter_p["operator"] == operator and filter_p["parameter"] == parameter:
                    operator = filter_p["replace_operator"]
                    parameter = filter_p["replace_parameter"]
                    value = filter_p["start"] + value + filter_p["end"]
            url_ = url_ + "&filter=" + operator + parameter + ":"+value + "&"
        if self._to is not None:
            url_ = url_ + "to=" + self._to + "&"
        if self._from is not None:
            url_ = url_ + "from=" + self._from + "&"
        if self._limit is not None:
            url_ = url_ + "limit=" + self._limit + "&"
        if self._sort is not None:
            url_ = url_ + "sort=" + self._sort + "&"
        if self.matchType is not None:
            url_ = url_ + "matchType=" + self.matchType + "&"
        url_ = url_ + "output=" + output
        return url_

    def parameter_page_n(self, url, count=None,  filter_ps=[], output="json"):
        url_ = url + "?url=" + self.url + "&page=" + str(count)
        for fliter in self._fliters:
            operator = fliter["operator"]
            parameter = fliter["parameter"]
            value = fliter["value"]
            for filter_p in filter_ps:
                if filter_p["operator"] == operator and filter_p["parameter"] == parameter:
                    operator = filter_p["replace_operator"]
                    parameter = filter_p["replace_parameter"]
                    value = filter_p["start"] + value + filter_p["end"]
            url_ = url_ + "&filter=" + operator + parameter + ":"+value + "&"
        if self._to is not None:
            url_ = url_ + "to=" + self._to + "&"
        if self._from is not None:
            url_ = url_ + "from=" + self._from + "&"
        if self._limit is not None:
            url_ = url_ + "limit=" + self._limit + "&"
        if self._sort is not None:
            url_ = url_ + "sort=" + self._sort + "&"
        if self.matchType is not None:
            url_ = url_ + "matchType=" + self.matchType + "&"
        url_ = url_ + "output=" + output
        return url_
