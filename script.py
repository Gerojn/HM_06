import sys
from pathlib import Path
import shutil

CATEGORIES = {"Audio": [".mp3", ".wav", ".flac", ".wma"],
              "Docs": [".docx", ".txt", ".pdf"]}


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    normalized_name = normalize(file.name)
    new_path = target_dir.joinpath(normalized_name)
    if not new_path.exists():
        file.replace(new_path)


def unpack_archives(archive_file: Path, root_dir: Path) -> None:
    archive_name = archive_file.stem
    destination_folder = root_dir / "archives" / archive_name

    if not destination_folder.exists():
        destination_folder.mkdir(parents=True)

    shutil.unpack_archive(str(archive_file), str(destination_folder))


cyrillic_to_latin = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
    'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
}


def normalize(input_string):
    result = ''
    for char in input_string:
        if char.lower() in cyrillic_to_latin:
            if char.isupper():
                result += cyrillic_to_latin[char.lower()].upper()
            else:
                result += cyrillic_to_latin[char.lower()]
        elif char.isalnum():
            result += char
        else:
            result += '_'

    return result


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
        elif element.is_dir():
            normalized_name = normalize(element.name)
            new_path = element.parent.joinpath(normalized_name)
            if not new_path.exists():
                element.rename(new_path)


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder dos not exists"

    sort_folder(path)

    return "All Ok"


if __name__ == '__main__':
    main()
