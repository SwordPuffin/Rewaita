pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'rewaita'
gnome = import('gnome')

gnome.compile_resources('rewaita',
  'rewaita.gresource.xml',
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
  input: 'rewaita.in',
  output: 'rewaita',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

rewaita_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'utils.py',
  'custom_theme.py'
]

install_data(rewaita_sources, install_dir: moduledir)

template_source = [ 'themes/gnome-shell-template.css', 'themes/default-light.css', 'themes/default-dark.css', 'themes/custom-template.css' ]

install_data(template_source, install_dir: moduledir)

install_subdir(
  'themes/window-controls',
  install_dir: moduledir
)

install_subdir(
  'themes/dark',
  install_dir: moduledir
)

install_subdir(
  'themes/light',
  install_dir: moduledir
)
