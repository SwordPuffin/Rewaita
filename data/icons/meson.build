application_id = 'io.github.swordpuffin.rewaita'

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
  actions_dir / 'reload-symbolic.svg',
  actions_dir / 'hammer-symbolic.svg',
  actions_dir / 'brush-symbolic.svg'
]

install_data(
  actions_icons,
  install_dir: get_option('datadir') / 'icons' / actions_dir
)
