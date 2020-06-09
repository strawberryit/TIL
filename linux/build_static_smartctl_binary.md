## Build static smartctl binary
> smartctl 바이너리가 필요한데 설치를 할 수 없는 환경인 경우, static binary를 빌드하여 사용할 수 있다.

### 준비
- CentOS 6 또는 원하는 버전
  - Docker container에서 동작하는 경우 `sudo`를 제외하고 실행하면 된다.
- smartmontools 소스

#### 비고
smartmontools 6.6부터 C++11 사용으로 C++ 컴파일러 버전을 업데이트해야한다. (여기서는 devtoolset-8 사용)
```
configure: error:
This version of smartmontools does not use C++11 features, but future
versions possibly will.
This script was unable to determine a compiler option to enable C++11.
Use option '--with-cxx11-option=OPTION' to specify the compiler option
(it will be checked, but not used in the actual build).
Use option '--without-cxx11-option' to suppress this error message if the
compiler lacks C++11 support.
In both cases, please send info about compiler and platform to
smartmontools-support@listi.jpberlin.de - Thanks!
```

### 빌드 방법
1. 빌드환경 구성
```
$ sudo yum makecache fast
$ sudo yum install -y centos-release-scl

$ sudo yum makecache fast
$ sudo yum install -y automake glibc-static wget devtoolset-8

$ scl enable devtoolset-8 bash
```

2. 소스 빌드
```
$ wget https://jaist.dl.sourceforge.net/project/smartmontools/smartmontools/7.1/smartmontools-7.1.tar.gz
# 또는 여기에서 소스 파일을 다운받는다.
# https://sourceforge.net/projects/smartmontools/files

$ tar xvzf smartmontools-7.1.tar.gz
$ cd smartmontools-7.1
$ ./autogen.sh
$ ./configure LDFLAGS="-static"
$ make

# 필요하면 디버그 정보 제거로 파일 사이즈를 줄인다.
$ strip smartctl
```

### 참고
https://www.bryceguinta.me/statically-compiling-smartctl.html