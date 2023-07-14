Name: sunshine
Version: 0.20.0
Release: alt1

Summary: Sunshine is a self-hosted game stream host for Moonlight
License: GPL-3.0
Group: Networking/Remote access
Url: https://app.lizardbyte.dev

# Source-url: https://github.com/LizardByte/Sunshine/archive/refs/tags/v%version.tar.gz
Source: %name-%version.tar

Source1: %name-development-%version.tar

# Source2-url: https://github.com/moonlight-stream/moonlight-common-c.git
Source2: moonlight-common-c.tar

# Source3-url: https://github.com/cgutman/enet.git
Source3: enet-v1.3.17.tar

# Source4-url: https://gitlab.com/eidheim/Simple-Web-Server.git
Source4: Simple-Web-Server.tar

Source5: %name.desktop

# Source6-url: https://github.com/miniupnp/miniupnp.git
Source6: miniupnp.tar

# Source7-url: https://github.com/FFmpeg/nv-codec-headers/archive/refs/tags/n11.1.5.2.tar.gz
Source7: nv-codec-headers-n11.1.5.2.tar

# Source8-url: https://github.com/michaeltyson/TPCircularBuffer.git
Source8: TPCircularBuffer.tar

# Source9-url: https://github.com/LizardByte/build-deps/archive/refs/heads/ffmpeg-linux-x86_64.tar.gz
Source9: ffmpeg-linux-x86_64.tar

# Source10-url: https://github.com/sleepybishop/nanors.git
Source10: nanors.tar

# Source11-url: https://github.com/dmikushin/tray.git
Source11: tray.tar

# fix building with CMakeLists.txt with library appindicator3
Patch1: sunshine-0.20.0-alt-fixappindicator.patch

ExclusiveArch: x86_64

BuildRequires(pre): rpm-macros-cmake
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libmfx-devel
BuildRequires: libayatana-appindicator3-devel
BuildRequires: libcap-devel
BuildRequires: libcurl-devel
BuildRequires: libdrm-devel
BuildRequires: libevdev-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libX11-devel
BuildRequires: libxcb-devel
BuildRequires: libXcursor-devel
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXtst-devel
BuildRequires: libGL-devel
BuildRequires: libnuma-devel
BuildRequires: libssl-devel
BuildRequires: libopus-devel
BuildRequires: libpulseaudio-devel
BuildRequires: libcuda
BuildRequires: boost-program_options-devel
BuildRequires: boost-complete
BuildRequires: npm
BuildRequires: bzlib-devel
BuildRequires: libfreetype-devel
BuildRequires: libpcre2-devel
BuildRequires: libbrotli-devel
BuildRequires: libexpat-devel
BuildRequires: libffi-devel
BuildRequires: libmount-devel
BuildRequires: libblkid-devel
BuildRequires: libselinux-devel
BuildRequires: libfribidi-devel
BuildRequires: libthai-devel
BuildRequires: libdatrie-devel
BuildRequires: libXdmcp-devel
BuildRequires: libpixman-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libwayland-cursor-devel
BuildRequires: libwayland-egl-devel
BuildRequires: libepoxy-devel
BuildRequires: at-spi2-atk-devel
BuildRequires: libwaylandpp-devel

%description
Sunshine is a self-hosted game stream host for Moonlight. Offering low latency, cloud gaming server capabilities with support for AMD, Intel, and Nvidia GPUs for hardware encoding. Software encoding is also available. You can connect to Sunshine from any Moonlight client on a variety of devices. A web UI is provided to allow configuration, and client pairing, from your favorite web browser. Pair from the local server or any mobile device.

%prep
%setup -a1 -a2 -a3 -a4 -a6 -a7 -a8 -a9 -a10 -a11
%patch1 -p1

%build
%cmake -W no-dev \
    -D CMAKE_BUILD_TYPE=Release \
    -D SUNSHINE_ENABLE_WAYLAND=1 \
    -D SUNSHINE_ENABLE_X11=1 \
    -D SUNSHINE_ENABLE_DRM=1 \
    -D SUNSHINE_ENABLE_CUDA=1 \
    -D CMAKE_INSTALL_PREFIX=/usr \
    -D SUNSHINE_EXECUTABLE_PATH=%_bindir/sunshine \
    -D SUNSHINE_ASSETS_DIR="share/sunshine"

# cd x86_64-alt-linux
%cmake_build

%install
%cmake_install
mkdir -p  %buildroot/lib/udev/rules.d/
mv -v %buildroot%_libexecdir/udev/rules.d/85-sunshine.rules %buildroot/lib/udev/rules.d/85-sunshine.rules
install -Dm 644  %SOURCE5 -t %buildroot%_desktopdir

%pre
if ! getent group input > /dev/null; then
    echo "Creating group input"
    groupadd -r input
fi
%post
setcap cap_sys_admin+p %_bindir/$(readlink $(which sunshine))

%files
%_bindir/%name
%_bindir/%name-%version
%_libexecdir/systemd/user/sunshine.service
/lib/udev/rules.d/85-sunshine.rules
%_datadir/sunshine/*
%_iconsdir/%name.svg
%_desktopdir/%name.desktop

%changelog
* Tue Jul 11 2023 Ivan Mazhukin <vanomj@altlinux.org> 0.20.0-alt1
- Initial build for Alt Sisyphus
