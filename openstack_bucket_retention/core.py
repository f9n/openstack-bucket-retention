import logging
import sys
from datetime import datetime, timedelta

from swiftclient.service import SwiftService, SwiftError

UNITS = dict(s="seconds", m="minutes", h="hours", d="days", w="weeks")

logger = logging.getLogger(__name__)


def convert_to_seconds(s):
    """
    https://stackoverflow.com/questions/3096860/convert-time-string-expressed-as-numbermhdsw-to-seconds-in-python
    """
    count = int(s[:-1])
    unit = UNITS[s[-1]]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days


def filter_object_names_by_seconds(container, seconds):
    """
    https://github.com/openstack/python-swiftclient/blob/master/examples/list.py
    """
    object_names = []
    now = datetime.now()
    old_day = now - timedelta(seconds=seconds)
    old_day_as_isoformat = old_day.isoformat()

    with SwiftService() as swift:
        try:
            list_parts_gen = swift.list(container=container)
            for page in list_parts_gen:
                if not page["success"]:
                    raise page["error"]

                for item in page["listing"]:
                    name = item["name"]
                    last_modified = item["last_modified"]
                    if old_day_as_isoformat > last_modified:
                        object_names.append(name)

        except SwiftError as e:
            logger.error(e.value)
            sys.exit(1)

    return object_names


def delete_objects(container, objects):
    """
    https://github.com/openstack/python-swiftclient/blob/master/examples/delete.py
    """
    _opts = {"object_dd_threads": 20}
    with SwiftService(options=_opts) as swift:
        del_iter = swift.delete(container=container, objects=objects)
        for del_res in del_iter:
            c = del_res.get("container", "")
            o = del_res.get("object", "")
            a = del_res.get("attempts")
            if del_res["success"] and not del_res["action"] == "bulk_delete":
                rd = del_res.get("response_dict")
                if rd is not None:
                    t = dict(rd.get("headers", {}))
                    if t:
                        logger.info(
                            "Successfully deleted {0}/{1} in {2} attempts "
                            "(transaction id: {3})".format(c, o, a, t)
                        )
                    else:
                        logger.info(
                            "Successfully deleted {0}/{1} in {2} "
                            "attempts".format(c, o, a)
                        )


def retention(bucket_name, retention_time):
    retention_seconds = convert_to_seconds(retention_time)
    object_names = filter_object_names_by_seconds(
        container=bucket_name, seconds=retention_seconds
    )
    delete_objects(container=bucket_name, objects=object_names)
