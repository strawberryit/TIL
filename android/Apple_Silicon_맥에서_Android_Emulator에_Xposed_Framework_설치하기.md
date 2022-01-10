# Apple Silicon 맥에서 Android Emulator에 Xposed Framework 설치하기

## XPosed Framework?
> Xposed is a framework for modules that can change the behavior of the system and apps without touching any APKs.

https://www.xda-developers.com/xposed-framework-hub/

Xposed는 Android APK 파일을 직접 수정하지 않고도, 시스템/사용자 App의 동작을 변경할 수 있는 framework이다. Android의 시스템 프로세스인 zygote를 injection하여 사용자 모듈이 동작할 수 있도록 해준다.

여기에서는 `Magisk + riru + LSPosed` 조합으로 emulator에 XPosed Framework를 설치한다.


> :warning: **경고**
>
> 기기 루팅 및 Xposed framework는 보안에 매우 취약할 수 있으므로, 개발/테스트 용도로만 사용한다.


## 작업 순서
1. 아래 저장소를 clone한다.<br/>
https://github.com/shakalaca/MagiskOnEmulator.git

2. 저장소 디렉토리의 busybox를 arm64용으로 바꾸어준다.
> (저장소에 포함된 busybox는 `x86_64`, `aarch32`용이라서 M1 Android emulator에서 제대로 동작하지 않음)

아래 파일을 다운로드 받아서 이름을 busybox로 변경하여 위 폴더에 복사한다.<br/>
busybox (arm64): https://github.com/Magisk-Modules-Repo/busybox-ndk/blob/master/busybox-arm64-selinux?raw=true

3. AVD Manager에서 Create Virtual Device로 AVD를 생성한다.
   - `Choose a device definition`: PlayStore가 **포함되지 않은** 기기를 선택
   - `Select a system image`: R (API Level 30, Android 11, arm64-v8a)

4. 위에서 선택한 버전의 system image가 위치한 ramdisk.img 파일을 MagiskOnEmulator 디렉토리에 복사한다.
> - 일반적으로 Android SDK는 `~/Library/Android/sdk`에 설치된다.
> - `android-30`: API Level 30
> - `google_apis`: PlayStore가 **포함되지 않은** 버전
```bash
~/MagiskOnEmulator $ cp ~/Library/Android/sdk/system-images/android-30/google_apis/arm64-v8a/ramdisk.img .
```

5. MagiskOnEmulator 디렉토리에서 patch.sh를 실행하면 `ramdisk.img` 파일이 패치된다.
> :warning: 주의:
>
> arm64 버전의 magisk.zip파일을 별도로 준비해야 하는데, `canary` 옵션을 주면 개발버전의 최신 magisk가 자동으로 설치된다.
```
$ bash patch.sh canary
```

6. 패치된 ramdisk.img를 AVD 경로에 복사해넣는다.
```bash
$ cp ramdisk.img ~/.android/avd/<AVD 이름>.avd/
```

7. Emulator를 종료한 후 다시 실행할 때 **Cold Boot Now** 옵션으로 재실행한다.

8. Emulator에서 Chrome을 실행한 후 아래 두 파일을 다운로드 받는다.
   - https://github.com/RikkaApps/Riru/releases 에서 riru-v*******-release.zip
   - https://github.com/LSPosed/LSPosed/releases 에서 LSPosed-v******-riru-release.zip

9. Emulator에서 Magisk를 실행하고 Modules 탭에서 위 두 파일을 설치한다.
   - Install from storage -> riru-v*******-release.zip -> Reboot
   - 재부팅 후
   - Install from storage -> LSPosed-v******-riru-release.zip -> Reboot

10. 설치된 LSPosed 실행하면 초록색 Activated가 활성화되어있다.

## 참고
- https://github.com/shakalaca/MagiskOnEmulator
- https://github.com/RikkaApps/Riru
- https://github.com/LSPosed/LSPosed
- https://forum.xda-developers.com/t/lsposed-xposed-framework-8-0-12-0-simple-magisk-module-edxposed-alternative.4228973/
