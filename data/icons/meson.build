application_id = 'io.github.swordpuffin.wardrobe'

scalable_dir = 'hicolor' / 'scalable' / 'apps'
install_data(
  scalable_dir / ('@0@.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)

actions_dir = 'hicolor' / 'scalable' / 'actions'

actions_icons = [
  actions_dir / 'icon-symbolic.svg',
  actions_dir / 'interface-symbolic.svg',
  actions_dir / 'shell-symbolic.svg',
  actions_dir / 'cursor-symbolic.svg',
  actions_dir / 'search-symbolic.svg',
  actions_dir / 'wallpaper-symbolic.svg',
  actions_dir / 'download-symbolic.svg',
  actions_dir / 'delete-symbolic.svg',
  actions_dir / 'left-symbolic.svg',
  actions_dir / 'folder-open-symbolic.svg',
  actions_dir / 'external-link-symbolic.svg',
  actions_dir / 'web-symbolic.svg',
]

install_data(
  actions_icons,
  install_dir: get_option('datadir') / 'icons' / actions_dir
)