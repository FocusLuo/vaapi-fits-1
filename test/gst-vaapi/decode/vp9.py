###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *

#-------------------------------------------------#
#----------------------8BIT-----------------------#
#-------------------------------------------------#

spec_8bit = load_test_spec("vp9", "decode", "8bit")

@slash.requires(have_gst)
@slash.requires(*have_gst_element("vaapi"))
@slash.requires(*have_gst_element("vaapivp9dec"))
@slash.requires(*have_gst_element("checksumsink2"))
@slash.parametrize(("case"), sorted(spec_8bit.keys()))
@platform_tags(VP9_DECODE_8BIT_PLATFORMS)
def test_8bit(case):
  params = spec_8bit[case].copy()

  params.update(mformatu = mapformatu(params["format"]))

  if params["mformatu"] is None:
    slash.skip_test("{format} format not supported".format(**params))

  params["decoded"] = get_media()._test_artifact(
    "{}_{width}x{height}_{format}.yuv".format(case, **params))

  dxmap = {".ivf":"ivfparse", ".webm":"matroskademux"}
  ext = os.path.splitext(params["source"])[1]
  assert ext in dxmap.keys(), "Unrecognized source file extension {}".format(ext)
  params["demux"] = dxmap[ext]

  call(
    "gst-launch-1.0 -vf filesrc location={source}"
    " ! {demux} ! vaapivp9dec"
    " ! videoconvert ! video/x-raw,format={mformatu}"
    " ! checksumsink2 file-checksum=false frame-checksum=false"
    " plane-checksum=false dump-output=true qos=false"
    " dump-location={decoded}".format(**params))

  params.setdefault(
    "metric", dict(type = "ssim", miny = 1.0, minu = 1.0, minv = 1.0))
  check_metric(**params)

#-------------------------------------------------#
#---------------------10BIT-----------------------#
#-------------------------------------------------#

spec_10bit = load_test_spec("vp9", "decode", "10bit")

@slash.requires(have_gst)
@slash.requires(*have_gst_element("vaapi"))
@slash.requires(*have_gst_element("vaapivp9dec"))
@slash.requires(*have_gst_element("checksumsink2"))
@platform_tags(VP9_DECODE_10BIT_PLATFORMS)
@slash.parametrize(("case"), sorted(spec_10bit.keys()))
def test_10bit(case):
  params = spec_10bit[case].copy()

  params.update(mformatu = mapformatu(params["format"]))

  if params["mformatu"] is None:
    slash.skip_test("{format} format not supported".format(**params))

  params["decoded"] = get_media()._test_artifact(
    "{}_{width}x{height}_{format}.yuv".format(case, **params))

  dxmap = {".ivf":"ivfparse", ".webm":"matroskademux"}
  ext = os.path.splitext(params["source"])[1]
  assert ext in dxmap.keys(), "Unrecognized source file extension {}".format(ext)
  params["demux"] = dxmap[ext]

  call(
    "gst-launch-1.0 -vf filesrc location={source}"
    " ! {demux} ! vaapivp9dec"
    " ! videoconvert ! video/x-raw,format={mformatu}"
    " ! checksumsink2 file-checksum=false frame-checksum=false"
    " plane-checksum=false dump-output=true qos=false"
    " dump-location={decoded}".format(**params))

  params.setdefault(
    "metric", dict(type = "ssim", miny = 1.0, minu = 1.0, minv = 1.0))
  check_metric(**params)
