pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'wardrobe'
gnome = import('gnome')

gnome.compile_resources('wardrobe',
  'wardrobe.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'wardrobe.in',
  output: 'wardrobe',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

wardrobe_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'utils.py',
  'styles.css'
]

install_data(wardrobe_sources, install_dir: moduledir)

widget_sources = [
	'widgets/theme_cell.py',
	'widgets/theme_cell_flowbox.py',
	'widgets/install_page.py',
	'widgets/main_page.py',
	'widgets/search_page.py',
	'widgets/theme_page.py',
	'widgets/main_page_banner.py',
	'widgets/item_carousel.py'
]

install_data(widget_sources, install_dir: moduledir)
