#!/bin/bash
# arguments
Num=1
Prefix=output/

# 1.generate tex files
python main.py --pageNum $Num

# 2.generate pdf files
for ((it=0; it<$Num; it++))
do
    pdflatex -interaction=nonstopmode $Prefix$it.tex
done

mv ./*.pdf output/
rm ./*.aux ./*.log

# 3.convert to image
for ((it=0; it<$Num; it++))
do
    echo $it
    convert -density 400 $Prefix$it.pdf -filter lagrange -distort resize 33% -background white -alpha remove -quality 100 $Prefix$it.jpg
done

# 4.visualize
python scripts/generate_xml.py -I $Prefix --visualize
mv *.xml ./xml
mv *.jpg ./output