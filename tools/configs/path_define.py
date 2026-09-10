from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..', '..').resolve()

ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
CONFIGS_DIR = ASSETS_DIR.joinpath('configs')
PATCH_GLYPHS_DIR = ASSETS_DIR.joinpath('patch-glyphs')
FONTS_DIR = ASSETS_DIR.joinpath('fonts')
MAPPINGS_DIR = ASSETS_DIR.joinpath('mappings')
KERNINGS_DIR = ASSETS_DIR.joinpath('kernings')
TEMPLATES_DIR = ASSETS_DIR.joinpath('templates')

CACHE_DIR = PROJECT_ROOT_DIR.joinpath('cache')
DOWNLOADS_DIR = CACHE_DIR.joinpath('downloads')
ARK_PIXEL_GLYPHS_DIR = CACHE_DIR.joinpath('ark-pixel-glyphs')

BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
DUMP_DIR = BUILD_DIR.joinpath('dump')
FALLBACK_GLYPHS_DIR = BUILD_DIR.joinpath('fallback-glyphs')
OUTPUTS_DIR = BUILD_DIR.joinpath('outputs')
RELEASES_DIR = BUILD_DIR.joinpath('releases')

DOCS_DIR = PROJECT_ROOT_DIR.joinpath('docs')
