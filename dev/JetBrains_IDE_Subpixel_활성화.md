## JetBrains IDE(2020.1.3+)에서 사라진 IDE Subpixel Antialiasing 활성화하기

### 문제
JetBrains의 IDE(IDEA, PyCharm, ...)가 2020.1.2 -> 2020.1.3+ 버전으로 업데이트 되면서 성능상의 문제인지 `Antialiasing > IDE` 옵션에서 Subpixel이 사라졌습니다.
(Grayscale, No antialiasing 만 선택할 수 있음)

Grayscale로 사용해 봤는데, 글자가 덜 이쁘게 나오는것 같아 다시 Subpixel 방식으로 돌아가기로 했습니다.

### 해결
프로젝트 선택 화면에서 `Configure -> Edit Custom VM Options...` 로 들어가서 아래 옵션을 추가합니다.
```
-Denable.macos.ide.subpixelAA=true
``` 
Save 후 다시 시작하면 IDE Antialising 옵션에서 Subpixel을 선택할 수 있습니다.

~~기본값을 바꾸면 되지 왜 굳이 숨겨서 귀찮게 만들어~~

### 출처
- https://youtrack.jetbrains.com/issue/IDEA-242765
- https://youtrack.jetbrains.com/issue/IDEA-238301#focus=streamItem-27-4167876.0-0