###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *

spec = load_test_spec("vpp", "deinterlace")

@slash.requires(have_gst)
@slash.requires(*have_gst_element("vaapi"))
@slash.requires(*have_gst_element("vaapipostproc"))
@slash.requires(*have_gst_element("checksumsink2"))
@slash.parametrize(*gen_vpp_deinterlace_parameters(spec, ["bob", "weave", "motion-adaptive", "motion-compensated"]))
@platform_tags(VPP_PLATFORMS)
def test_default(case, method):
  params = spec[case].copy()
  params.update(
    method = map_deinterlace_method(method),
    mformat = mapformat(params["format"]))

  if params["method"] is None:
    slash.skip_test("{} method not supported".format(method))

  params["ofile"] = get_media()._test_artifact(
    "{}_deinterlace_{method}_{format}_{width}x{height}"
    ".yuv".format(case, **params))

  call(
    "gst-launch-1.0 -vf filesrc location={source} num-buffers={frames}"
    " ! rawvideoparse format={mformat} width={width} height={height}"
    " ! vaapipostproc format={mformat} width={width} height={height}"
    " deinterlace-mode=1 deinterlace-method={method} ! checksumsink2"
    " file-checksum=false frame-checksum=false plane-checksum=false"
    " dump-output=true dump-location={ofile}".format(**params))

  psnr = calculate_psnr(
    params["source"], params["ofile"],
    params["width"], params["height"],
    params["frames"], params["format"])

  def compare(k, ref, actual):
    assert ref is not None, "Invalid reference value"
    assert abs(ref[-3] - actual[-3]) < 0.2, "Luma (Y) out of baseline range"
    assert abs(ref[-2] - actual[-2]) < 0.2, "Cb (U) out of baseline range"
    assert abs(ref[-1] - actual[-1]) < 0.2, "Cr (V) out of baseline range"

  get_media().baseline.check_result(
    compare = compare, context = params.get("refctx", []), psnr = psnr)
