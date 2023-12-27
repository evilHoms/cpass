#!/bin/bash

# python3 -m pip install -r requirements.txt
if [ $1 ]; then HASH_KEY="-K$1"; fi
if [ $2 ]; then KEY="-k$2"; fi

cat > cpass <<EOF
#!/bin/bash
$PWD/main.py \$@ $HASH_KEY $KEY
EOF

chmod +x $PWD/cpass

echo "Dependencies installed"
echo "cpass script generated, put it to your PATH dirrectory."
