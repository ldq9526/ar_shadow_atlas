if [ $# -lt 2 ]; then
	echo "${#} parameters."
	echo "Usage: bash demo.sh <image_filename> <board_ip>"
	echo "<image_filename>: image file in data/noshadow/ and data/mask"
	echo "<board_ip>: ip address of Atlas 200 DK, default 192.168.1.2 for USB"
	exit
fi

echo "Give one of the windows focus and press any key to continue."
python3 display.py ${1}
if [ $? -ne 0 ]; then
	echo "[ERROR] No files."
	exit
fi

mkdir temp
mkdir temp/noshadow temp/mask
cp data/noshadow/${1} temp/noshadow/demo.jpg
cp data/mask/${1} temp/mask/demo.jpg

# default password is Mind@123
echo "Copy files to HwHiAiUser@${2}."
scp -r temp/* HwHiAiUser@${2}:~/ARShadowDemo/data/
if [ $? -ne 0 ]; then
	echo "[ERROR] Fail to copy files."
	rm -rf temp
	exit
fi
rm -rf temp

echo "Login HwHiAiUser@${2}."
ssh -t HwHiAiUser@${2} "cd /home/HwHiAiUser/ARShadowDemo; python demo.py; exit"
result_ssh=$?
if [ ${result_ssh} -ne 0 ]; then
	echo "ssh return ${result_ssh}"	
	echo "[ERROR] Fail to login Atlas 200."
	exit
fi

# copy result output folder from Atlas 200 DK
echo "Get results from HwHiAiUser@${2}."
scp -r HwHiAiUser@${2}:~/ARShadowDemo/output ./
echo "Give one of the windows focus and press any key to exit."
python3 display.py ${1} -o True
