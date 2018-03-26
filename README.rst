CFM-ID for Galaxy
=================
|Build Status (Travis)| |Bioconda|

Galaxy tool wrapper for CFM-ID.

Website: http://cfmid.wishartlab.com/

Source code: https://sourceforge.net/p/cfm-id/wiki/Home/


Galaxy
------
`Galaxy <https://galaxyproject.org>`_ is an open, web-based platform for data intensive biomedical research. Whether on the free public server or your own instance, you can perform, reproduce, and share complete analyses. 


TODO
------
- Requirements and add CFM-ID to Bioconda (Initial recipe created)
- Different data types for input
- Replace python file with `configfile option <https://docs.galaxyproject.org/en/latest/dev/schema.html#tool-configfiles-configfile>`_
- Use either InChI or SMILES (currently InChI)
- Add model files using the "tool-data" folder
- Annotation with different adduct types
- Run in parallel
- Note (testing): This tool requires the exportation of a system variable (LD_LIBRARY_PATH), we are currently adding CFM-ID to Biconda, but if you like to test the tool locally, you need to run the installation from `install.txt <https://github.com/computational-metabolomics/cfmid-galaxy/install.txt>`_ and correctly indicate them in the "command" section in the Galaxy tool XML file.
- Note: CFM-ID tool depends on a model. Trained models and invormation are available at https://sourceforge.net/p/cfm-id/code/HEAD/tree/supplementary_material/trained_models/esi_msms_models/. 


Developers & Contributors
-------------------------
 - Jordi Capellades (j.capellades.to@gmail.com) - Universitat Rovira i Virgili (Tarragona, Spain)
 - Ralf J. M. Weber (r.j.weber@bham.ac.uk) - `University of Birmingham (UK) <http://www.birmingham.ac.uk/index.aspx>`_


Changes
-------


License
-------
Released under the GNU General Public License v3.0 (see LICENSE file)


.. |Build Status (Travis)| image:: https://img.shields.io/travis/computational-metabolomics/cfmid-galaxy.svg?style=flat&maxAge=3600&label=Travis-CI
   :target: https://travis-ci.org/computational-metabolomics/cfmid-galaxy

.. |Bioconda| image:: https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat&maxAge=3600
   :target: http://bioconda.github.io/recipes/cfmid/README.html
