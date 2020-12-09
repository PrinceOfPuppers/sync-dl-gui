# sync-dl-gui
> An App for downloading and syncing remote playlists to your phone
- [ABOUT](#ABOUT)
- [DEVLOPMENT](#DEVLOPMENT)
- [DEPLOYMENT](#DEPLOYMENT)

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

install android-SDK

install openJDK

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

buildozer android debug 
```
This will build sync_dl_gui however we must manually configure androids manifest xml files located at:
```
32 Bit:
.buildozer/android/platform/build-armeabi-v7a/dists/sync_dl_gui__armeabi-v7a/templates/AndroidManifest.tmpl.xml

64 Bit:
.buildozer/android/platform/build-arm64-v8a/dists/sync_dl_gui__arm64-v8a/templates/AndroidManifest.tmpl.xml
```
In the application element of these files, add:

```
android:requestLegacyExternalStorage="true"
```
This will enable the application to use the old storage api, which will allow sync_dl_gui's
dependancies to access shared files such as music, bypassing the storage scoping rules added to android api 29 while still allowing us to deploy on google play.

Finally run the following command to build, install and run the app
```
buildozer android debug deploy run
```

# DEPLOYMENT

## Build for Deployment
The following will output a deployment build in bin
```
buildozer android release
```

## Jarsigning
Use keytool to create a RSA key of size 2048

install jarsigner 
```
jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore path/to/keystore bin/sync_dl_gui-1.0-armeabi-v7a-release-unsigned.apk chosen-key-alais
```

## Zipalign
install zipalign
```
zipalign -c -v 4 bin/sync_dl_gui-1.0-armeabi-v7a-release-unsigned.apk bin/sync_dl_gui_armeabi_v7a_1.0.apk

```

## Test apk
```
adb install bin/sync_dl_gui_armeabi_v7a_1.0.apk
```

## Repeat for arm64-v8a
Google Play requires both 32 and 64 bit releases

## Google Console
Follow Google Consoles step by step guide for releaseing an the application