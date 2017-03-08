#!/usr/bin/env bash

add-apt-repository ppa:fkrull/deadsnakes
apt-get update

packages=(
    "build-essential"
    "cmake"
    "gfortran"
    "git"
    "libatlas-base-dev"
    "libavcodec-dev"
    "libavformat-dev"
    "libdc1394-22-dev"
    "libgtk-3-dev"
    "libgtk2.0-dev"
    "libjasper-dev"
    "libjpeg-dev"
    "libjpeg8-dev"
    "libpng-dev"
    "libpng12-dev"
    "libswscale-dev"
    "libswscale-dev libv4l-dev"
    "libtbb-dev"
    "libtbb2"
    "libtiff-dev"
    "libtiff5-dev"
    "libx264-dev"
    "libxvidcore-dev"
    "pkg-config"
    "python-software-properties"
    "python2.7-dev"
    "python3.5-dev"
    "software-properties-common"
    "zsh"
)

for package in "${packages[@]}"
do
    apt-get install -y "$package"
done

cd /home/vagrant
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# install numpy so it works with python2 as well
pip install virtualenv virtualenvwrapper numpy
rm -rf /home/vagrant/get-pip.py /home/vagrant/.cache/pip

echo -e "\n# virtualenv and virtualenvwrapper" >> /home/vagrant/.bashrc
echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

export WORKON_HOME=/home/vagrant/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

sudo chown vagrant -R .virtualenvs

mkvirtualenv cv -p python3.5
workon cv
pip install numpy

git clone https://github.com/Itseez/opencv.git
git clone https://github.com/Itseez/opencv_contrib.git

sudo chown vagrant -R opencv
sudo chown vagrant -R opencv_contrib

cd /home/vagrant/opencv/
git checkout 3.1.0

cd /home/vagrant/opencv_contrib/
git checkout 3.1.0

cd /home/vagrant/opencv/
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=/home/vagrant/opencv_contrib/modules \
      -D PYTHON3_EXECUTABLE=/home/vagrant/.virtualenvs/cv/bin/python3.5 \
      -D BUILD_EXAMPLES=ON ..

make -j4

make install
ldconfig

cd /usr/local/lib/python3.5/site-packages/
mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so

cd /home/vagrant/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so

cd /home/vagrant
rm -rf opencv opencv_contrib

# fix camera hardware warning
ln /dev/null /dev/raw1394
