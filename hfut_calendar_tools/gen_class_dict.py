from typing import Dict, Any


def gen_class_dict(class_json, **kw):
    """

    :type class_json: dict
    """
    class_dict: Dict[Any, Any] = {}
    for one_of_class in class_json:
        class_dict[one_of_class["id"]] = one_of_class["courseName"]
    return class_dict
