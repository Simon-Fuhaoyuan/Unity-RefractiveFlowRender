# Output dir
outDir="Images/"
refDir="Refs/"
maskDir="Masks/"
rgbDir="RGBs/"
flowDir='Flows/'
calibDir=${outDir}"Calibration/"

# Input Dir
dataDir="./data/"
template=${dataDir}"runtime_template.pov"
setting=${dataDir}"setting.pov"

# Render setting
D="Declare="
common="+H512 +W512 -GR -GS -GW +GFerror +GP +FJ -D" # Common POV-RAY render setting
# Please refer to template.pov for definition of the following parameters 
cam_obj_bg_setting="${D}cl_x=${cl_x} ${D}cl_y=${cl_y} ${D}cl_z=${cl_z} ${D}lk_x=${lk_x} ${D}lk_y=${lk_y} ${D}lk_z=${lk_z} ${D}cs_x=${cs_x} ${D}cam_a=${cam_a} ${D}cam_z=${cam_z} ${D}bg_sc=${bg_sc} ${D}bg_pz=${bg_pz} ${D}bg_rx=${bg_rx} ${D}bg_ry=${bg_ry} ${D}bg_rz=${bg_rz} ${D}Dim=${Dim}" 
echo $cam_obj_bg_setting

# Render images and object mask
mkdir -p $outDir
mkdir -p $outDir$refDir
mkdir -p $outDir$maskDir
mkdir -p $outDir$rgbDir
sed -e  's#\${ImageName}#"${COCOImage}"#' ${template} > ${setting}
povray -I$setting $common ${cam_obj_bg_setting} -O${outDir}${refDir}${obj}_ref ${D}Empty=1
povray -I$setting $common ${cam_obj_bg_setting} -O${outDir}${rgbDir}${obj} +A
povray -I$setting $common ${cam_obj_bg_setting} -O${outDir}${maskDir}${obj}_mask +FN -A ${D}mask=1
# python processMask.py --img_dir $outDir # Process Mask

# Use graycode pattern to obtain the ground truth refractive flow field
mkdir -p ${calibDir}${obj}
sed -e  's#\${ImageName}#"./data/graycode_512_512/graycode_"#' ${template} > ${setting}
povray -I$setting $common ${cam_obj_bg_setting} +FN ${D}Calib=1 +KFI1 +KFF20 +KI1 +KF20 -O${calibDir}${obj}/graycode_
python findCorrespondence.py --in_root ${calibDir} --in_dir ${obj} --out_dir ${outDir}${flowDir} 
