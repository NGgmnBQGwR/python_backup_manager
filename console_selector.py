import tkinter as tk


class SelectableObject(object):
    def __init__(self, data, name, index):
        self.data = data
        self.name = name
        self.index = index
        self.selected = False

    def __str__(self):
        if self.selected:
            mark = '[X]'
        else:
            mark = '[ ]'

        return "{} {:3} - {}".format(mark, self.index, self.name)

    def toggle_selected(self):
        self.selected = not self.selected


class ConsoleSelect(object):
    MAX_ACTIVE_LINES = 30
    HALF_MAX_ACTIVE_LINES = MAX_ACTIVE_LINES // 2

    def __init__(self, selectable_objects, name_key):
        assert type(selectable_objects) is list

        length = len(selectable_objects)
        if length == 0:
            raise ValueError("Cannot start selection with 0 elements.")

        self.selectable_objects = []
        for index, so in enumerate(selectable_objects):
            obj = SelectableObject(data=so, name=getattr(so, name_key), index=index+1)
            self.selectable_objects.append(obj)

        self.selected = None
        self.not_selected = None
        self.element_count = length
        self.index = 0

    def toggle_selection(self, event):
        self.selectable_objects[self.index].toggle_selected()
        self.refresh()

    def selection_select_all(self, event):
        for obj in self.selectable_objects:
            obj.selected = True
        self.refresh()

    def selection_select_none(self, event):
        for obj in self.selectable_objects:
            obj.selected = False
        self.refresh()

    def selection_select_inverse(self, event):
        for obj in self.selectable_objects:
            obj.toggle_selected()
        self.refresh()

    def selection_next(self, event):
        if self.index < self.element_count - 1:
            self.index += 1
        self.refresh()

    def selection_next_page(self, event):
        if self.index < self.element_count - 1:
            self.index += self.HALF_MAX_ACTIVE_LINES
        if self.index >= self.element_count:
            self.index = self.element_count - 1
        self.refresh()

    def selection_previous(self, event):
        if self.index > 0:
            self.index -= 1
        self.refresh()

    def selection_previous_page(self, event):
        if self.index > 0:
            self.index -= self.HALF_MAX_ACTIVE_LINES
        if self.index < 0:
            self.index = 0
        self.refresh()

    def selection_first(self, event):
        self.index = 0
        self.refresh()

    def selection_last(self, event):
        self.index = self.element_count - 1
        self.refresh()

    def selection_stop(self, event, root):
        root.destroy()

    def collect_results(self):
        self.selected = [x.data for x in self.selectable_objects if x.selected]
        self.not_selected = [x.data for x in self.selectable_objects if not x.selected]
        assert len(self.selectable_objects) == len(self.selected) + len(self.not_selected)

    def show_window(self, root):
        if not root.winfo_viewable():
            root.deiconify()

    def select(self):
        self.refresh()

        root = tk.Tk()
        root.bind('<Up>', self.selection_previous)
        root.bind('<Prior>', self.selection_previous_page)
        root.bind('<Home>', self.selection_first)
        root.bind('<Down>', self.selection_next)
        root.bind('<Next>', self.selection_next_page)
        root.bind('<End>', self.selection_last)
        root.bind('<space>', self.toggle_selection)
        root.bind('a', self.selection_select_all)
        root.bind('i', self.selection_select_inverse)
        root.bind('n', self.selection_select_none)
        root.bind('<Return>', lambda x: self.selection_stop(x, root))
        root.bind('<Escape>', lambda x: self.selection_stop(x, root))
        root.bind("<FocusOut>", lambda x: self.show_window(root))
        # don't show the tk window
        root.withdraw()
        root.mainloop()

        self.collect_results()

    def print_row(self, index, obj):
        if index == self.index:
            mark = '> '
        else:
            mark = ''
        print("{}{}".format(mark, obj))

    def refresh(self):
        print('Select:\n')
        printed_skip_mark_at_start = False
        printed_skip_mark_at_end = False
        for index, obj in enumerate(self.selectable_objects):
            if index == 0:
                self.print_row(index, obj)
            elif index == self.element_count - 1:
                self.print_row(index, obj)
            else:
                if self.index - index > self.HALF_MAX_ACTIVE_LINES:
                    if not printed_skip_mark_at_start:
                        printed_skip_mark_at_start = True
                        print('...')
                    continue
                elif index - self.index > self.HALF_MAX_ACTIVE_LINES:
                    if not printed_skip_mark_at_end:
                        printed_skip_mark_at_end = True
                        print('...')
                    continue
                else:
                    self.print_row(index, obj)
        print('\n')

    def get_all(self):
        if not self.selected and not self.not_selected:
            self.select()
        return self.selected, self.not_selected

    def get_selected(self):
        if not self.selected and not self.not_selected:
            self.select()
        return self.selected

    def get_not_selected(self):
        if not self.selected and not self.not_selected:
            self.select()
        return self.not_selected


def test_run():
    lst = [{'id':'START ZERO'}]+[
        {'id': str(x + 1) + 'nth', 'line': 'something'} for x in range(98)
    ]+[{'id': 'END LAST 100'}]
    selected, not_selected = ConsoleSelect(lst, name_key='id').get_all()
    print(selected)
    print(not_selected)

if __name__ == "__main__":
    test_run()
