from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..', '..').resolve()

ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')

CONFIGS_DIR = ASSETS_DIR.joinpath('configs')
CONFIGS_FONTS_DIR = CONFIGS_DIR.joinpath('fonts')
CONFIGS_MAPPINGS_DIR = CONFIGS_DIR.joinpath('mappings')
CONFIGS_KERNING_DIR = CONFIGS_DIR.joinpath('kerning')

FONTS_DIR = ASSETS_DIR.joinpath('fonts')
PATCH_GLYPHS_DIR = ASSETS_DIR.joinpath('patch-glyphs')
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
