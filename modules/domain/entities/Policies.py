from dataclasses import dataclass, field


@dataclass
class Project:
    manage_project: bool = field(default=False)
    delete_project: bool = field(default=False)
    compile_project: bool = field(default=False)


@dataclass
class Pages:
    add_pages: bool = field(default=False)
    edit_pages: bool = field(default=False)
    delete_pages: bool = field(default=False)


@dataclass
class Items:
    add_items: bool = field(default=False)
    edit_items: bool = field(default=False)
    delete_items: bool = field(default=False)


@dataclass
class Media:
    add_image: bool = field(default=False)
    delete_image: bool = field(default=False)

    add_video: bool = field(default=False)
    delete_video: bool = field(default=False)

    add_audio: bool = field(default=False)
    delete_audio: bool = field(default=False)


@dataclass
class Users:
    add_user: bool = field(default=False)
    remove_user: bool = field(default=False)
