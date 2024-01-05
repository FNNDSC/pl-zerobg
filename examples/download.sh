#!/bin/bash -ex
# Downloads a subset of "Fetal Brain Atlas (Serag et al.)"

mkdir "$1"
cd "$1"
mkdir age24 age34

wget -O age24/template.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/307/template.nii.gz
wget -O age24/ventricles.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/331/ventricles.nii.gz
wget -O age24/mask.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/330/mask.nii.gz

wget -O age34/template.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/351/template.nii.gz
wget -O age34/ventricles.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/350/ventricles.nii.gz
wget -O age34/mask.nii.gz https://fetalmri-hosting-of-medical-image-analysis-platform-dcb83b.apps.shift.nerc.mghpcc.org/api/v1/files/310/mask.nii.gz
