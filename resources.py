import os
import json


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def __str__(self):
        return self.title

    def print_entries(self, depth=0):
        print_with_indent(str(self), indent=depth)
        for entry in self.entries:
            entry.print_entries(depth + 1)

    def json(self):
        entry_json = [entry.json() for entry in self.entries]
        data = {
            'title': self.title,
            'entries': entry_json,
        }
        return data

    def save(self, path):
        file_name = os.path.join(path, f'{self.title}.json')
        with open(file_name, 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = f.read()
            value = json.loads(content)
            return cls.from_json(value)

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            entry.add_entry(cls.from_json(sub_entry))
        return entry

class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: [Entry] = []

    def save(self):
        for i, entry in enumerate(self.entries):
            entry.save(self.data_path)

    def load(self):
        for file_name in os.listdir(self.data_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.data_path, file_name)
                entry = Entry.load(file_path)
                self.entries.append(entry)

def print_with_indent(value, indent=0):
    print('\t' * indent + value)