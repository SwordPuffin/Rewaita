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
  'interface_to_shell_theme.py'
]

install_data(rewaita_sources, install_dir: moduledir)

template_source = [ 'themes/gnome-shell-template.css' ]

install_data(template_source, install_dir: moduledir)

dark_themes = [
    'themes/dark/catppuccin-frappe.css',
    'themes/dark/catppuccin-mocha.css',
    'themes/dark/dracula.css',
    'themes/dark/everforest.css',
    'themes/dark/gruvbox-medium.css',
    'themes/dark/gruvbox-soft.css',
    'themes/dark/kanagawa.css',
    'themes/dark/material-deepocean.css',
    'themes/dark/material-palenight.css',
    'themes/dark/nightfox.css',
    'themes/dark/nord.css',
    'themes/dark/rose-pine.css',
    'themes/dark/rose-pine-moon.css',
    'themes/dark/solarized.css',
    'themes/dark/tokyonight.css',
    'themes/dark/tokyonight-storm.css'
]

install_data(dark_themes, install_dir: moduledir / 'dark')

light_themes = [
    'themes/light/catppuccin-latte.css',
    'themes/light/dawnfox.css',
    'themes/light/dracula.css',
    'themes/light/everforest.css',
    'themes/light/gruvbox-medium.css',
    'themes/light/gruvbox-soft.css',
    'themes/light/kanagawa.css',
    'themes/light/nord.css',
    'themes/light/rose-pine-dawn.css',
    'themes/light/solarized.css',
    'themes/light/tokyonight.css'
]

install_data(light_themes, install_dir: moduledir / 'light')
