import tkinter
import tkinter.ttk
import pathlib


class MoveFileDialog:
    def __init__(self, callback, root, filepath: pathlib.Path):
        self._callback = callback
        self._filepath = filepath
        self._root = tkinter.Toplevel(root)
        self._root.title("Move or rename file")
        self._tree = tkinter.ttk.Treeview(self._root, height=20, selectmode="browse")
        self._tree.column("#0",minwidth=0,width=400)
        ids = list()
        root_elem = filepath.parents[len(filepath.parents)-1]
        ids.append(self._tree.insert("", 0, text=root_elem, values=(root_elem,)))
        for node in filepath.parents.__reversed__():
            node_id = None
            for _id in ids:
                item = self._tree.item(_id, option="values")[0]
                if item == str(node):
                    node_id = _id
                    break
            self._tree.item(node_id, open=True)
            for file in sorted(node.iterdir()):
                if file.is_dir() and file.name[0] != '.':
                    ids.append(self._tree.insert(node_id, "end", text=str(file.name), values=(file,)))
        file_elem = None
        for _id in ids:
            item = self._tree.item(_id, option="values")[0]
            if item == str(filepath.parent):
                file_elem = _id
                break
        for _id in ids:
            childs = self._tree.get_children(_id)
            if len(childs) == 0 and _id != file_elem:
                self._tree.insert(_id, "end", text="Placeholder", values=("None",))
        self._tree.grid(row=0, column=0, columnspan=2)
        tkinter.Label(self._root, text="File name: ").grid(row=1, column=0)
        self._filename_field = tkinter.Entry(self._root, width=40)
        self._filename_field.delete(0, tkinter.END)
        self._filename_field.insert(0, filepath.stem)
        self._filename_field.grid(row=1, column=1)
        self._buttons_frame = tkinter.Frame(self._root)
        self._cancel_button = tkinter.Button(self._buttons_frame, text="Cancel", command=self._root.destroy)
        self._cancel_button.grid(row=0, column=0)
        self._ok_button = tkinter.Button(self._buttons_frame, text="OK", command=self.__ok_btn_handler)
        self._ok_button.grid(row=0, column=1)
        self._buttons_frame.grid(row=2, column=1, sticky="e")
        self._tree.bind("<<TreeviewOpen>>", self.__open_folder)
        self._tree.selection_add(file_elem)
        self._tree.focus(file_elem)

    def __ok_btn_handler(self):
        elem_id_list = self._tree.selection()
        dir = pathlib.Path(self._tree.item(elem_id_list[0], option="value")[0])
        new_filepath = dir.joinpath(self._filename_field.get()+self._filepath.suffix)
        self._callback(new_filepath)

    def __open_folder(self, event):
        elem_id = self._tree.focus()
        childs_list = self._tree.get_children(elem_id)
        if len(childs_list)==1 and self._tree.item(childs_list[0], option="values")[0] == "None":
            self._tree.delete(childs_list)
            elem = pathlib.Path(self._tree.item(elem_id, option="values")[0])
            for file in sorted(elem.iterdir()):
                if file.is_dir() and file.name[0] != '.':
                    file_id = self._tree.insert(elem_id, "end", text=str(file.name), values=(file,))
                    self._tree.insert(file_id, "end", text="Placeholder", values=("None",))