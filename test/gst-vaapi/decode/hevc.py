###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *

spec = load_test_spec("hevc", "decode", "8bit")

@slash.requires(have_gst)
@slash.requires(*have_gst_element("vaapi"))
@slash.requires(*have_gst_element("vaapih265dec"))
@slash.requires(*have_gst_element("checksumsink2"))
@slash.parametrize(("case"), sorted(spec.keys()))
@platform_tags(HEVC_DECODE_8BIT_PLATFORMS)
def test_8bit(case):
  params = spec[case].copy()

  params.update(mformatu = mapformatu(params["format"]))

  if params["mformatu"] is None:
    slash.skip_test("{format} format not supported".format(**params))

  params["decoded"] = get_media()._test_artifact(
    "{}_{width}x{height}_{format}.yuv".format(case, **params))

  call(
    "gst-launch-1.0 -vf filesrc location={source}"
    " ! h265parse ! vaapih265dec"
    " ! videoconvert ! video/x-raw,format={mformatu}"
    " ! checksumsink2 file-checksum=false qos=false"
    " frame-checksum=false plane-checksum=false dump-output=true"
    " dump-location={decoded}".format(**params))

  params.setdefault(
    "metric", dict(type = "ssim", miny = 1.0, minu = 1.0, minv = 1.0))
  check_metric(**params)

#-------------------------------------------------#
#---------------------10BIT-----------------------#
#-------------------------------------------------#

spec10 = load_test_spec("hevc", "decode", "10bit")

@slash.requires(have_gst)
@slash.requires(*have_gst_element("vaapi"))
@slash.requires(*have_gst_element("vaapih265dec"))
@slash.requires(*have_gst_element("checksumsink2"))
@slash.parametrize(("case"), sorted(spec10.keys()))
@platform_tags(HEVC_DECODE_10BIT_PLATFORMS)
def test_10bit(case):
  params = spec10[case].copy()

  params.update(mformatu = mapformatu(params["format"]))

  if params["mformatu"] is None:
    slash.skip_test("{format} format not supported".format(**params))

  params["decoded"] = get_media()._test_artifact(
    "{}_{width}x{height}_{format}.yuv".format(case, **params))

  call(
    "gst-launch-1.0 -vf filesrc location={source}"
    " ! h265parse ! vaapih265dec"
    " ! videoconvert ! video/x-raw,format={mformatu}"
    " ! checksumsink2 file-checksum=false qos=false"
    " frame-checksum=false plane-checksum=false dump-output=true"
    " dump-location={decoded}".format(**params))

  params.setdefault(
    "metric", dict(type = "ssim", miny = 1.0, minu = 1.0, minv = 1.0))
  check_metric(**params)
