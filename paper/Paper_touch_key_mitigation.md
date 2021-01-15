# Paper Touch/Key mitigation

### Java code
https://github.com/strawberryit/Android42MockupFramework/blob/db994500d82e84c082248a31e223c5a351f98588/app/src/main/java/android/app/Activity.java#L26-L39

https://github.com/strawberryit/Android42MockupFramework/blob/db994500d82e84c082248a31e223c5a351f98588/app/src/main/java/android/app/Activity.java#L41-L59



### Baksmali
```bash
$ java -jar baksmali-2.4.0.jar x \
    -a 17 \
    -d framework/ \
    -o smali/framework/ \
    framework/framework.odex
```
--di False 옵션을 주면, 코드 비교시에 불필요한 line number를 없앨 수 있다.<br/>
다만, 리패키징할 때는 debug정보가 있는게 좋음

### Smali
```bash
$ java -jar smali-2.4.0.jar a \
    -a 17 \
    -o classes.dex \
    smali/framework
```

### dex -> odex
```bash
$ cp ~~~/framework/framework.jar framework.jar

$ 7z a -tzip framework.jar classes.dex

$ adb push framework.jar /data/local/tmp/
$ adb push dexopt-wrapper /data/local/tmp/
$ adb push busybox-armv7l /data/local/tmp/

$ adb shell

$ cd /data/local/tmp

$ ./dexopt-wrapper framework.jar framework.odex $BOOTCLASSPATH

$ ./busybox dd if=/system/framework/framework.odex \
    of=framework.odex \
    bs=1 count=20 skip=52 seek=52 conv=notrunc
```
필요한 파일 [files](files/)

### framework.odex 교체
```bash
$ su
$ mount -o rw,remount /system
$ cp /system/framework/framework.odex /system/framework/framework.odex.backup

$ stop
$ cat /data/local/tmp/framework.odex > /system/framework/framework.odex
$ start
```


### Mod details
<details>
    <summary>Activity.dispatchTouchEvent() - 원본</summary>

```smali
.method public dispatchTouchEvent(Landroid/view/MotionEvent;)Z
    .registers 3

    invoke-virtual {p1}, Landroid/view/MotionEvent;->getAction()I

    move-result v0

    if-nez v0, :cond_9

    invoke-virtual {p0}, Landroid/app/Activity;->onUserInteraction()V

    :cond_9
    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object v0

    invoke-virtual {v0, p1}, Landroid/view/Window;->superDispatchTouchEvent(Landroid/view/MotionEvent;)Z

    move-result v0

    if-eqz v0, :cond_15

    const/4 v0, 0x1

    :goto_14
    return v0

    :cond_15
    invoke-virtual {p0, p1}, Landroid/app/Activity;->onTouchEvent(Landroid/view/MotionEvent;)Z

    move-result v0

    goto :goto_14
.end method
```
</details>

<details>
    <summary>Activity.dispatchTouchEvent() - 수정</summary>

```smali
.method public dispatchTouchEvent(Landroid/view/MotionEvent;)Z
    .registers 4
    .param p1, "ev"    # Landroid/view/MotionEvent;

    .prologue
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getY()F

    move-result v0

    float-to-int v0, v0

    const/16 v1, 0x38e

    if-ne v0, v1, :cond_b

    const/4 v0, 0x0

    return v0

    :cond_b
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getAction()I

    move-result v0

    if-nez v0, :cond_9

    invoke-virtual {p0}, Landroid/app/Activity;->onUserInteraction()V

    :cond_9
    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object v0

    invoke-virtual {v0, p1}, Landroid/view/Window;->superDispatchTouchEvent(Landroid/view/MotionEvent;)Z

    move-result v0

    if-eqz v0, :cond_15

    const/4 v0, 0x1

    :goto_14
    return v0

    :cond_15
    invoke-virtual {p0, p1}, Landroid/app/Activity;->onTouchEvent(Landroid/view/MotionEvent;)Z

    move-result v0

    goto :goto_14
.end method
```
</details>

<details>
    <summary>Activity.dispatchKeyEvent() - 원본</summary>

```smali
.method public dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    .registers 5

    invoke-virtual {p0}, Landroid/app/Activity;->onUserInteraction()V

    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object v1

    invoke-virtual {v1, p1}, Landroid/view/Window;->superDispatchKeyEvent(Landroid/view/KeyEvent;)Z

    move-result v2

    if-eqz v2, :cond_f

    const/4 v2, 0x1

    :goto_e
    return v2

    :cond_f
    iget-object v0, p0, Landroid/app/Activity;->mDecor:Landroid/view/View;

    if-nez v0, :cond_17

    invoke-virtual {v1}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v0

    :cond_17
    if-eqz v0, :cond_22

    invoke-virtual {v0}, Landroid/view/View;->getKeyDispatcherState()Landroid/view/KeyEvent$DispatcherState;

    move-result-object v2

    :goto_1d
    invoke-virtual {p1, p0, v2, p0}, Landroid/view/KeyEvent;->dispatch(Landroid/view/KeyEvent$Callback;Landroid/view/KeyEvent$DispatcherState;Ljava/lang/Object;)Z

    move-result v2

    goto :goto_e

    :cond_22
    const/4 v2, 0x0

    goto :goto_1d
.end method
```
</details>

<details>
    <summary>Activity.dispatchKeyEvent() - 수정</summary>

```smali
.method public dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    .registers 7
    .param p1, "event"    # Landroid/view/KeyEvent;

    .prologue
    const/4 v2, 0x1

    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I

    move-result v3

    const/16 v4, 0x5c

    if-eq v3, v4, :cond_11

    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I

    move-result v3

    const/16 v4, 0x5d

    if-ne v3, v4, :cond_18

    :cond_11
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getRepeatCount()I

    move-result v3

    if-lez v3, :cond_18

    :cond_17
    :goto_17
    return v2

    :cond_18
    invoke-virtual {p0}, Landroid/app/Activity;->onUserInteraction()V

    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;

    move-result-object v1

    .local v1, "win":Landroid/view/Window;
    invoke-virtual {v1, p1}, Landroid/view/Window;->superDispatchKeyEvent(Landroid/view/KeyEvent;)Z

    move-result v3

    if-nez v3, :cond_17

    iget-object v0, p0, Landroid/app/Activity;->mDecor:Landroid/view/View;

    .local v0, "decor":Landroid/view/View;
    if-nez v0, :cond_2d

    invoke-virtual {v1}, Landroid/view/Window;->getDecorView()Landroid/view/View;

    move-result-object v0

    :cond_2d
    if-eqz v0, :cond_38

    invoke-virtual {v0}, Landroid/view/View;->getKeyDispatcherState()Landroid/view/KeyEvent$DispatcherState;

    move-result-object v2

    :goto_33
    invoke-virtual {p1, p0, v2, p0}, Landroid/view/KeyEvent;->dispatch(Landroid/view/KeyEvent$Callback;Landroid/view/KeyEvent$DispatcherState;Ljava/lang/Object;)Z

    move-result v2

    goto :goto_17

    :cond_38
    const/4 v2, 0x0

    goto :goto_33
.end method
```
</details>
