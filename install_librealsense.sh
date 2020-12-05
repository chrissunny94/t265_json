#sudo sh -c "echo "CONF_SWAPSIZE=2048" >> /etc/dphys-swapfile"
sudo /etc/init.d/dphys-swapfile restart swapon -s
sudo apt update;sudo apt -y upgrade

sudo apt-get install -y libdrm-amdgpu1 libdrm-amdgpu1-dbg libdrm-dev libdrm-exynos1 libdrm-exynos1-dbg libdrm-freedreno1 libdrm-freedreno1-dbg libdrm-nouveau2 libdrm-nouveau2-dbg libdrm-omap1 libdrm-omap1-dbg libdrm-radeon1 libdrm-radeon1-dbg libdrm-tegra0 libdrm-tegra0-dbg libdrm2 libdrm2-dbg
sudo apt-get install -y libglu1-mesa libglu1-mesa-dev glusterfs-common libglu1-mesa libglu1-mesa-dev 

sudo apt-get install -y libglu1-mesa libglu1-mesa-dev mesa-utils mesa-utils-extra xorg-dev libgtk-3-dev libusb-1.0-0-dev

cd ~

git clone https://github.com/IntelRealSense/librealsense
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/ 

sudo udevadm control --reload-rules && udevadm trigger 

 mkdir  build  && cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DFORCE_LIBUVC=true
make -j1
sudo make install
