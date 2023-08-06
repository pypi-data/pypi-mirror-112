# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lbcgo', 'lbcgo.examples']

package_data = \
{'': ['*'], 'lbcgo': ['conf/*']}

install_requires = \
['astropy==0', 'ccdproc>=2.2.0,<3.0.0', 'numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'lbcgo',
    'version': '0.1.2',
    'description': "Data reduction for the LBT's Large Binocular Camera",
    'long_description': '# LBCgo: LBC data reduction pipeline\n\nWARNING: This code is currently under continued development. While the basic functionality exists, it should be used with some care and attention.\n\n## Dependencies:\n\nPython dependencies:\n* `astropy`\n* `CCDProc`\n* `numpy`\n\nExternal dependencies:\n* `SExtractor`\n* `SCAMP`\n* `SWarp`\n\nThe external C++ codes `SCAMP`, `SWarp`, and `SExtractor` developed by  Emmanuel Bertin and collaborators are available through http://astromatic.iap.fr. `SCAMP` and `SExtractor` are also available through GitHub: https://github.com/astromatic.\n\n## Running LBCgo:\n\nFor "standard" situations, the `LBCgo` can be run in one step from the python command line. In this case, all of the data in the `raw/` directory are taken on the same night and have appropriate calibrations. In this case, running `LBCgo` from the command line is as simple as:\n```\nipython> from lbcproc import *\nipython> from lbcregister import *\n\nipython> lbcgo()\n```\nBefore doing this, copy the parameter files from `LBCgo/LBCgo/conf/` into the current working directory (an eventual fix won\'t require this step).\n\nAlternatively, it can be useful to process each filter separately or even to avoid doing the astrometric steps until a later time. In this case, one may do:\n```\nipython> lbcgo(filter_names=[\'I-BESSEL\'], do_astrometry=False)\n```\n\nThe astrometric portion of the reduction can be done later using, for example reducing the I-BESSEL data for the target PG1338+101:\n```\nipython> fltr_dirs=glob(\'PG1338+101/I-BESSEL/\')\nipython> go_register(fltr_dirs, do_sextractor=True,\n            do_scamp=True, do_SWarp=True)\n```\n\n#### Missing chips:\n\n`LBCgo` can be used if the images were taken when one of the LBC CCDs was off-line. The approach to doing this is to explicitly specify the chips to include in the data reduction steps:\n```\nipython> lbcgo(lbc_chips=[1,2,4])\n```\nThis is useful, as there were several months in 2011 when LBCCHIP3 was inoperable.\n\n## Some things that might go wrong:\n\nTesting has revealed some occasional issues with the astrometric solution for the individual chips. This can be difficult to diagnose. The registration step using `SWarp` can warn you of some obvious cases, and these can subsequently be removed before rerunning the `SWarp` step by doing, e.g.:\n```\nipython> go_register(fltr_dirs, do_sextractor=False,\n            do_scamp=False, do_SWarp=True)\n```\n\nThere are several issues related to missing or inappropriate files that the current code does not deal with gracefully. The most common is missing flat fields or missing configuration files (found in `LBCgo/LBCgo/conf/`).\n\n\n## Credit:\n\nThis pipeline is built on code initially developed by David Sands, and eventually incorporated into scripts made available by Ben Weiner\n(https://github.com/bjweiner/LBC-reduction).\n\n`LBCgo` was designed to simplify the process of LBC reduction, removing the need for IDL or IRAF in favor of Python. This package continues to require `SCAMP`, `SWarp`, and `SExtractor` provided by Emmanuel Bertin (http://astromatic.iap.fr). It makes extensive use of the `astropy`-affiliated package `CCDProc`.\n\n\n## Known bugs / limitations:\n\n* As of yet no tests are performed to separate LBCB / LBCR images taken with the V-BESSEL filter (which exists in both imagers). Care must be taken to avoid having both in the same directory.\n\n* If flat field images are present, but no image is taken in that flat, an unfortunate behavior results (existing flat fields are divided by the unmatched flats).\n\n* Flat field images taken as "test" images, including only a partial read-out of a single CCD, will cause the code to bail without a helpful error message.\n',
    'author': 'Chris Howk',
    'author_email': 'jhowk@nd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
