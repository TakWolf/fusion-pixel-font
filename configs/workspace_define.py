import os

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

assets_dir = os.path.join(project_root_dir, 'assets')
fonts_dir = os.path.join(assets_dir, 'fonts')
design_dir = os.path.join(assets_dir, 'design')
www_static_dir = os.path.join(assets_dir, 'www-static')

dump_outputs_dir = os.path.join(project_root_dir, 'dump_outputs')

outputs_dir = os.path.join(project_root_dir, 'outputs')

releases_dir = os.path.join(project_root_dir, 'releases')

docs_dir = os.path.join(project_root_dir, 'docs')

www_dir = os.path.join(project_root_dir, 'www')
