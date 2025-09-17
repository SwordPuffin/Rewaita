import gi
from gi.repository import Gtk, Adw

extras_info = {
    "Default": "default",
    "Colored": "colored",
    "MacOS style": "macos"
}

class ButtonBox(Gtk.Button):
    def __init__(self, control, current_config, window, flowbox):
        super().__init__(hexpand=True)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for pack_side in [Gtk.PackType.END, Gtk.PackType.START]:
            window_controls = Gtk.WindowControls(side=pack_side, halign=Gtk.Align.CENTER)
            window_controls.add_css_class(extras_info[control])
            window_controls_frame = Gtk.Frame(child=window_controls, margin_bottom=12, margin_top=12, halign=Gtk.Align.CENTER)
            window_controls_frame.add_css_class("card")
            box.append(window_controls_frame)
        title = Gtk.Label(label=_(control), margin_bottom=12)
        box.append(title)
        self.connect("clicked", window.on_window_control_clicked, extras_info[control], window, flowbox)
        self.set_child(box)
        if(extras_info[control] == current_config):
            self.add_css_class("suggested-action")

class WindowControlBox(Gtk.Box):
    def __init__(self, window, current_config):
        super().__init__(hexpand=True, orientation=Gtk.Orientation.VERTICAL)
        self.append(Adw.Clamp(maximum_size=1200, child=Gtk.Separator(margin_start=20, margin_end=20, margin_top=25)))
        title = Gtk.Label(label=_("Window Controls"), margin_bottom=12, margin_top=15)
        title.add_css_class("title-2")
        self.append(title)
        flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
        for control in extras_info.keys():
            flowbox.insert(ButtonBox(control, current_config, window, flowbox), -1)
        self.append(Adw.Clamp(child=flowbox, maximum_size=1200))

