#!/bin/bash

python3 -m pip install -r requirements.txt

cat > cpass <<EOF
#!/bin/bash
$PWD/main.py \$@
EOF

chmod +x $PWD/cpass

echo "Dependencies installed"
echo "cpass script generated, put it to your PATH dirrectory."
