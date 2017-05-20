# eu4tagswitch.py


For tagswitching in *locally saved* ironman games in EU4 v1.13.x and EU4 v1.17.1.  This preserves ironman on the modified save even after changing to another country.  Useful to switch to an opposing country and scout out your opposition.

It reportedly preserves the ability to receive achievements as well after tag switching, but I have not tested this in 1.17.1.


####Usage

```python eu4_tagswitch.py tag source_path target_path```

####Example:

```python eu4_tagswitch.py FRA ~/Desktop/ryukyu.eu4 ~/Desktop/ryukyu2.eu4```

where ```tag``` is the [country tag](http://www.eu4wiki.com/Countries) you want to switch to, ```source_path``` is the path to the ironman save file, and ```target_path``` is the path where you want to save the modified save file.  

## Warnings
**DO NOT** use on later versions of this game, > 1.17.1.

For various implementation reasons, do **not** attempt to directly overwrite the old save file with the new save file, by setting ```source_path``` and ```target_path``` to the same path.  Always save to another file, then manually copy the new file over the old.

##Implementation details
The compressed EU4 local ironman save file is an ordinary Zip archive containing a metadata file and the actual save.  The save itself is a binary file, protected by a checksum recorded in the metadata file.  If the save is modified, the checksum no longer matches, and ironman (and ability to earn achievements) is lost.

In v1.13, the game ironically fails to validate the metadata file itself against change.  That is, the checksum in the metadata file does not incorporate the values of the metadata file itself.  Therefore, any value within the metadata file can be extracted from the Zip archive, modified, and recompressed along with the savegame data.  This means the country tag can be changed, and on next load, the game will happily load you as the new chosen country.

Due to the way Python 2.x handles Zip files, compressed files in the archive cannot be changed in-place.  The entire archive has to be extracted, and each file repacked into a new archive.


