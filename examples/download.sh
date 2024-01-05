#!/bin/bash -ex
# Downloads a subset of "Fetal Brain Atlas (Serag et al.)"

mkdir "$1"
cd "$1"

wget -O template24.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/307/template.nii.gz
wget -O ventricles24.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/331/ventricles.nii.gz
wget -O mask24.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/330/mask.nii.gz

wget -O template34.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/351/template.nii.gz
wget -O ventricles34.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/350/ventricles.nii.gz
wget -O mask34.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/310/mask.nii.gz
