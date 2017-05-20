import zipfile, argparse, re, platform, os.path
import struct

EU4BIN_PLAYER_TOKEN = "\x38\x2a"
EU4BIN_ASSIGNMENT_OPERATOR_TOKEN = "\x01\x00"
EU4BIN_STRING_TYPE_TOKEN = "\x0f\x00"

def tag_switch(source_path, target_path, tag):
    if (not zipfile.is_zipfile(source_path)):
        raise ValueError("Not a valid compressed save game file")
    source_zip = zipfile.ZipFile(source_path, 'r')
    metadata = extract_save_metadata(source_zip)
    metadata = tag_replace(metadata, tag)
    if not target_path:
        if platform.system().lower() == "darwin":
            target_path = os.path.join(os.path.expanduser("~/Documents/Paradox Interactive/Europa Universalis IV/save games"), tag.lower()+".eu4")
        else:
            raise ValueError("Need to give a path to save the new save file.")
    save_metadata(metadata, source_zip, target_path)

def save_metadata(metadata, source_zip, target_path):
    target_zip = zipfile.ZipFile(target_path, 'w', compression=zipfile.ZIP_DEFLATED)
    for f in source_zip.namelist():
        if f != "meta":
            target_zip.writestr(f, source_zip.read(f))
    target_zip.writestr("meta", metadata)
    source_zip.close()
    target_zip.close()

def extract_save_metadata(source_zip):
    metadata = source_zip.read("meta")
    if (not metadata):
        raise ValueError("No savegame metadata found")
    return metadata

def tag_replace(metadata, tag):
    if (metadata.startswith("EU4bin")):
        metadata = bytearray(metadata)
        prefix_bytes = EU4BIN_PLAYER_TOKEN+EU4BIN_ASSIGNMENT_OPERATOR_TOKEN+EU4BIN_STRING_TYPE_TOKEN
        prefix_length = len(prefix_bytes)
        pos = metadata.find(prefix_bytes)
        # tag_old_length_bytes = metadata[pos+prefix_length:pos+prefix_length+2]
        tag_length = struct.pack("h", len(tag))
        metadata[pos + prefix_length:pos + prefix_length + 2] = tag_length
        #tag_old = metadata[pos + prefix_length+2:pos + prefix_length + 2+len(tag)]
        metadata[pos + prefix_length + 2 : pos + prefix_length + 2 + len(tag)] = tag
        metadata = str(metadata)
    else:
        pat = re.compile(r'^player="[A-Z]+"', flags=re.MULTILINE)
        m = pat.search(metadata)
        if m:
            return pat.sub('player="%s"' % (tag), metadata)
    return metadata

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='EU4 Ironman Tagswitcher')
    parser.add_argument('tag')
    parser.add_argument('source_path')
    if platform.system().lower() == "darwin":
        parser.add_argument('target_path', nargs='?', default=None)
    else:
        parser.add_argument('target_path')
    args = parser.parse_args()
    tag_switch(args.source_path, args.target_path, args.tag)
    #print args.source_file
    #print args.tag
    #parser.add_argument('-t', action="store_true", default=False)
    #parser.add_argument('-b', action="store", dest="b")
