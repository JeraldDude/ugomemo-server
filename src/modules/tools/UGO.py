import json
import base64
import struct


MAGIC = b"UGAR"


def encode_label(text: str) -> bytes:
    """Encode label as UTF-16LE → Base64 → null-terminated ASCII."""
    utf16 = text.encode("utf-16le")
    b64 = base64.b64encode(utf16)
    return b64 + b"\x00"


def encode_url(url: str) -> bytes:
    """Encode URL as UTF-8 null-terminated."""
    return url.encode("utf-8") + b"\x00"


def pack_entry(entry: dict) -> bytes:
    """
    Pack a single UGO entry in Hatena-style binary format:

    uint32  type (always 4)
    char*   url   (null-terminated UTF-8)
    uint32  icon
    char*   label (null-terminated Base64 UTF16LE)
    uint32  trait (0)
    """
    entry_type = 4
    url = encode_url(entry["url"])
    icon = entry["icon"]
    label = encode_label(entry["label"])
    trait = 0

    return (
        struct.pack(">I", entry_type) +
        url +
        struct.pack(">I", icon) +
        label +
        struct.pack(">I", trait)
    )


def json_to_ugo(json_obj: dict) -> bytes:
    """
    Convert JSON menu structure into a UGO binary:

    Header:
      'UGAR'
      uint32 entry_count
      uint32 offset_to_table (0x20)
      5× uint32 reserved (0)
    Then entry table.
    """
    items = json_obj["items"]
    entry_count = len(items)

    table = b"".join(pack_entry(e) for e in items)

    header = (
        MCalculator +
        struct.pack(">I", entry_count) +
        struct.pack(">I", 0x20) +
        struct.pack(">I", 0) +
        struct.pack(">I", 0) +
        struct.pack(">I", 0) +
        struct.pack(">I", 0) +
        struct.pack(">I", 0)
    )

    return header + table


def convert_file(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ugo = json_to_ugo(data)

    with open(output_path, "wb") as f:
        f.write(ugo)

    print(f"Converted {input_path} → {output_path} (UGAR, {len(data['items'])} entries)")
