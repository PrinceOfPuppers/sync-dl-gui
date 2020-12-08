# sync-dl-gui
> An App for downloading and syncing remote playlists to your phone
- [ABOUT](#ABOUT)
- [DEVLOPMENT](#DEVLOPMENT)

# ABOUT
Created to avoid having music deleted but still have the convenience of browsing, adding and reordering new music using remote services such as youtube.

the application does not store any of its metadata in songs, metadata is stored next to them in a .metadata file, the music files are managed through numbering, allowing them to be played alphanumerically using any playback service (such as VLC)



### Smart Sync:
The main feature of sync-dl Adds new music from remote playlist to local playlist, also takes ordering of remote playlist
without deleting songs no longer available in remote playlist.

songs that are no longer available in remote, will remain after the song they are currently after in the local playlist



# DEVLOPMENT

## On Desktop

```
git clone https://github.com/PrinceOfPuppers/sync-dl-gui

cd sync-dl-gui

pip install -r requirements.txt

python3 sync_dl_gui/main.py
```


## On Mobile
install buildozer https://buildozer.readthedocs.io/en/latest/

install adb https://developer.android.com/studio/command-line/adb

Enable developer mode on your smartphone and connect it to your computer via usb, be sure to enable usb debugging.
Test if connection is working using 
```
adb devices
```

Clone the project and setup logging

```
git clone https://github.com/PrinceOfPuppers/sync-dl-gui

cd sync-dl-gui

pip install -r requirements.txt

adb logcat -s "python" > logs/logcat
```

In a seperate terminal run the following to build and push to your smartphone
```
cd PATH_TO_SYNC-DL-GUI

buildozer android debug update deploy run
```
this should build, install and launch sync-dl-gui on your phone, however at times buildozer fails to auto launch
in which case just manually open the newly installed app.