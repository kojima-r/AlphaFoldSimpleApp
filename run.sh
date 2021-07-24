path=$1
uid=$2

cd /data1/AlphaFold/alphafold

base=/data1/AlphaFold/api/static
echo $uid > ${base}/log/${uid}.txt
python docker/run_docker.py \
	--fasta_paths=${path} \
	--max_template_date=2020-05-14 \
	--preset=casp14 \
	--gpu_devices "2,3" >>  ${base}/log/${uid}.txt

