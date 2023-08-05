# Copyright 2021 TUNiB inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools


def igetattr(obj, attr, *args):
    if "[" in attr and "]" in attr:
        attr = "".join("\t".join(attr.split("[")).split("]")).split("\t")
        indexes = "[".join(attr[1:-1]).replace("[", "][")
        indexes = "[" + indexes + "]" if len(indexes) >= 1 else indexes
        return igetattr(obj, attr[0] + indexes)[int(attr[-1])]
    else:
        return getattr(obj, attr, *args)


def isetattr(obj, attr, val):
    if "[" in attr and "]" in attr:
        element = attr.split("[")[0]
        element_obj = getattr(obj, element)
        attr = "".join("\t".join(attr.split("[")).split("]")).split("\t")[1:]

        for i in range(len(attr) - 1):
            element_obj = element_obj[int(attr[i])]

        element_obj[int(attr[-1])] = val
    else:
        setattr(obj, attr, val)


def rgetattr(obj, attr, default=None):
    try:
        left, right = attr.split('.', 1)
    except:
        return igetattr(obj, attr, default)
    return rgetattr(igetattr(obj, left), right, default)


def rsetattr(obj, attr, val):
    try:
        left, right = attr.split('.', 1)
    except:
        return isetattr(obj, attr, val)
    return rsetattr(igetattr(obj, left), right, val)


def rhasattr(obj, attr):
    try:
        left, right = attr.split('.', 1)
    except:
        return hasattr(obj, attr)
    return rhasattr(igetattr(obj, left), right)
