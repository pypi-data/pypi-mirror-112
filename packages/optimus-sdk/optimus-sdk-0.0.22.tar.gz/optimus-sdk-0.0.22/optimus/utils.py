from typing import List


class Dict(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value


def list_to_query_param(param_name: str, param: List[str]) -> str:
    tmp = ""
    if len(param) == 1:
        tmp = f"{param_name}={param[0]}"
    else:
        for i in param:
            tmp += f"{param_name}={i}&"
    if tmp.endswith("&"):
        tmp = tmp[0:-1]
    return tmp


def format_result(results):
    if isinstance(results, dict):
        return Dict(results)
    elif isinstance(results, list):
        tmp = []
        for i in results:
            tmp.append(Dict(i))
        return tmp
    else:
        return results


def list_dict_to_dict(value: list) -> dict:
    res = {}
    for i in value:
        tmp = {i.name: i.value, "objective": i.objective}
        res.update(tmp)
    return res


def object_list_to_dict_list(value):
    if value is None:
        return value

    tmp = []
    for i in value:
        tmp.append(i.__dict__)
    return tmp
