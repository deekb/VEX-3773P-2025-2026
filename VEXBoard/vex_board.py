class VexBoardWidget:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def update_value(self, new_value):
        self.value = new_value


class VexBoard:
    def __init__(self):
        self.widgets = {}

    def add_widget(self, name, initial_value):
        self.widgets[name] = VexBoardWidget(name, initial_value)

    def update_widget(self, name, new_value):
        if name in self.widgets:
            self.widgets[name].update_value(new_value)
        else:
            print(f"Widget \"{name}\" does not exist.")
