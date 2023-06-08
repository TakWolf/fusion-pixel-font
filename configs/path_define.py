import os

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

assets_dir = os.path.join(project_root_dir, 'assets')
glyphs_dir = os.path.join(assets_dir, 'glyphs')
fonts_dir = os.path.join(assets_dir, 'fonts')
templates_dir = os.path.join(assets_dir, 'templates')
zip_static_dir = os.path.join(assets_dir, 'zip-static')
www_static_dir = os.path.join(assets_dir, 'www-static')

cache_dir = os.path.join(project_root_dir, 'cache')

build_dir = os.path.join(project_root_dir, 'build')
tmp_dir = os.path.join(build_dir, 'tmp')
glyphs_tmp_dir = os.path.join(tmp_dir, 'glyphs')
dump_dir = os.path.join(build_dir, 'dump')
outputs_dir = os.path.join(build_dir, 'outputs')
releases_dir = os.path.join(build_dir, 'releases')
www_dir = os.path.join(build_dir, 'www')

docs_dir = os.path.join(project_root_dir, 'docs')
