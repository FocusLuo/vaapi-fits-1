###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *

spec = load_test_spec("avc", "decode")

@slash.requires(have_ffmpeg)
@slash.requires(have_ffmpeg_qsv_accel)
@slash.requires(have_ffmpeg_h264_qsv_decode)
@slash.requires(using_compatible_driver)
@slash.parametrize(("case"), sorted(spec.keys()))
@platform_tags(AVC_DECODE_PLATFORMS)
def test_default(case):
  params = spec[case].copy()

  params.update(mformat = mapformat(params["format"]))
  if params["mformat"] is None:
    slash.skip_test("{format} format not supported".format(**params))

  params["decoded"] = get_media()._test_artifact(
    "{}_{width}x{height}_{format}.yuv".format(case, **params))

  output = call(
    "ffmpeg -hwaccel qsv -hwaccel_device /dev/dri/renderD128 -v verbose"
    " -c:v h264_qsv -i {source} -vf 'hwdownload,format=nv12'"
    " -pix_fmt {mformat} -f rawvideo -vsync passthrough"
    " -vframes {frames} -y {decoded}".format(**params))

  m = re.search("not supported for hardware decode", output, re.MULTILINE)
  assert m is None, "Failed to use hardware decode"

  m = re.search("Initialize MFX session", output, re.MULTILINE)
  assert m is not None, "It appears that the QSV plugin did not load"

  params.setdefault(
    "metric", dict(type = "ssim", miny = 1.0, minu = 1.0, minv = 1.0))
  check_metric(**params)
