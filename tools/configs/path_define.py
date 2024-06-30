from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..', '..').resolve()

assets_dir = project_root_dir.joinpath('assets')
patch_glyphs_dir = assets_dir.joinpath('patch-glyphs')
fonts_dir = assets_dir.joinpath('fonts')
templates_dir = assets_dir.joinpath('templates')
www_static_dir = assets_dir.joinpath('www-static')

build_dir = project_root_dir.joinpath('build')
cache_dir = build_dir.joinpath('cache')
ark_pixel_glyphs_dir = build_dir.joinpath('ark-pixel-glyphs')
dump_dir = build_dir.joinpath('dump')
fallback_glyphs_dir = build_dir.joinpath('fallback-glyphs')
outputs_dir = build_dir.joinpath('outputs')
releases_dir = build_dir.joinpath('releases')
www_dir = build_dir.joinpath('www')

docs_dir = project_root_dir.joinpath('docs')
