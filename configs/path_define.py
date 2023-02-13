import os

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

assets_dir = os.path.join(project_root_dir, 'assets')
unidata_dir = os.path.join(assets_dir, 'unidata')
fonts_dir = os.path.join(assets_dir, 'fonts')
templates_dir = os.path.join(assets_dir, 'templates')
www_static_dir = os.path.join(assets_dir, 'www-static')

build_dir = os.path.join(project_root_dir, 'build')
dump_dir = os.path.join(build_dir, 'dump')
outputs_dir = os.path.join(build_dir, 'outputs')
releases_dir = os.path.join(build_dir, 'releases')
www_dir = os.path.join(build_dir, 'www')

cache_dir = os.path.join(project_root_dir, 'cache')

docs_dir = os.path.join(project_root_dir, 'docs')
