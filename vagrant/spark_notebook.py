#!/usr/bin/env python

# https://github.com/felixcheung/vagrant-projects

from os import chdir, getenv, system, umask
from os.path import exists, expanduser
from subprocess import check_output, check_call
from sys import executable


def setenv(var, value, overwrite=True):
    from os import environ
    if overwrite or not var in environ:
        environ[var] = value


#-----------------------
# PySpark
#

umask(0077)  # ensure that always chmod go-wrx
chdir(expanduser("~"))

setenv('PYSPARK_PYTHON', executable, overwrite=False)
setenv('PYSPARK_DRIVER_PYTHON', 'ipython')  # PySpark Driver (ie. IPython)
profile_name = 'pyspark'
setenv('PYSPARK_DRIVER_PYTHON_OPTS', 'notebook --profile=%s' % profile_name)

#-----------------------
# IPython Notebook
#

ipython_notebook_config_template = '''c = get_config()
c.NotebookApp.ip = '{ip}'
c.NotebookApp.port = {port}
c.NotebookApp.open_browser = False
'''

pyspark_setup_template = '''from os import getenv
if not getenv('PYSPARK_SUBMIT_ARGS', None):
    raise ValueError('PYSPARK_SUBMIT_ARGS environment variable is not set')

spark_home = getenv('SPARK_HOME', None)
if not spark_home:
    raise ValueError('SPARK_HOME environment variable is not set')
'''

pyspark_custom_css = '''
.rendered_html img {
    display: inline-block;
}

.rendered_html h1 {
    font-family: "Source Sans Pro",sans-serif;
    font-weight: 200;
    line-height: 36px;
    font-size: 33px
}

.rendered_html h2,h2 .job-name {
    font-family: "Source Sans Pro",sans-serif;
    font-weight: 200;
    line-height: 30px;
    font-size: 27px
}

.rendered_html h3 {
    font-family: "Source Sans Pro",sans-serif;
    font-weight: 200;
    line-height: 24px;
    font-size: 22px
}

.rendered_html h4 {
    font-family: "Source Sans Pro",sans-serif;
    font-weight: 200;
    line-height: 21px;
    font-size: 18px
}

.rendered_html h5 {
    font-family: "Source Sans Pro",sans-serif;
    font-weight: 200;
    line-height: 19px;
    font-size: 16px
}
'''

pyspark_custom_js = ''

matplotlib_inline = '''
c.IPKernelApp.matplotlib = 'inline'
c.InlineBackend.rc = {}
'''

ip = '*'  # Warning: this is potentially insecure
port = 8001

#-----------------------
# Create profile and start
#

try:
    ipython_profile_path         = check_output(['ipython', 'locate']).rstrip('\n') + '/profile_%s' % profile_name
    print ipython_profile_path
    setup_py_path                = ipython_profile_path + '/startup/00-pyspark-setup.py'
    ipython_notebook_config_path = ipython_profile_path + '/ipython_notebook_config.py'
    ipython_kernel_config_path   = ipython_profile_path + '/ipython_kernel_config.py'
    ipython_custom_css_path      = ipython_profile_path + '/static/custom/custom.css'
    ipython_custom_js_path       = ipython_profile_path + '/static/custom/custom.js'

    if not exists(ipython_profile_path):
        print 'Creating IPython Notebook profile\n'
        check_call(['ipython', 'profile', 'create', profile_name])
        print 'Writing custom CSS/JS\n'
        with open(ipython_custom_css_path, 'w') as css_file:
            css_file.write(pyspark_custom_css)
        with open(ipython_custom_js_path, 'w') as js_file:
            js_file.write(pyspark_custom_js)
        print '\n'

    if not exists(setup_py_path):
        print 'Writing PySpark setup\n'
        with open(setup_py_path, 'w') as setup_file:
            setup_file.write(pyspark_setup_template)

    # matplotlib inline
    kernel_config = open(ipython_kernel_config_path).read()
    if "c.IPKernelApp.matplotlib = 'inline'" not in kernel_config:
        print 'Writing IPython kernel config\n'
        new_kernel_config = kernel_config.replace('# c.IPKernelApp.matplotlib = None', matplotlib_inline)
        with open(ipython_kernel_config_path, 'w') as kernel_file:
            kernel_file.write(new_kernel_config)

    if not exists(ipython_notebook_config_path) or 'open_browser = False' not in open(ipython_notebook_config_path).read():
        print 'Writing IPython Notebook config\n'
        with open(ipython_notebook_config_path, 'w') as config_file:
            config_file.write(ipython_notebook_config_template.format(ip=ip, port=port))

    print 'Launching PySpark with IPython Notebook\n'
    cmd = 'pyspark'
    system(cmd)
    exit(0)

except KeyboardInterrupt:
    print 'Aborted\n'
    exit(1)
