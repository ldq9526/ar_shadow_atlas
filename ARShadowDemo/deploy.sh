if [ ${#} -lt 1 ]; then
	echo "${#} parameters."
	echo "Usage: bash deploy.sh <board_ip>"
	echo "<board_ip>: ip address of Atlas 200, default 192.168.1.2 for USB"
	exit
fi

DEMO_DIR="ARShadowDemo"

echo "Deploying on HwHiAiUser@${1}..."
ssh -t HwHiAiUser@${1} "if [ ! -d ${DEMO_DIR} ]; then mkdir ${DEMO_DIR}; fi; cd ${DEMO_DIR}; mkdir models data; mkdir data/noshadow data/mask; exit"
result_ssh=$?
if [ ${result_ssh} -ne 0 ]; then
	echo "ssh return ${result_ssh}"	
	echo "[ERROR] Fail to deploy on Atlas 200 DK."
	exit
fi

echo "Copying files to HwHiAiUser@${1}..."
scp demo.py HwHiAiUser@${1}:~/${DEMO_DIR}/
scp model.om HwHiAiUser@${1}:~/${DEMO_DIR}/models/
result_scp=$?
if [ ${result_scp} -ne 0 ]; then
	echo "scp return ${result_scp}"	
	echo "[ERROR] Fail to copy files to Atlas 200 DK."
	exit
fi

echo "Finish deploying."
