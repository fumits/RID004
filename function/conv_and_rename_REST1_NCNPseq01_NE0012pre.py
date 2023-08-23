#########################################################
# Conversion to NifTi and rename for HCP at KUHP
# Need to set dcm2niix as a path in advance
# ver 1.0 (2022/6/1)
# ver 1.1 (2022/6/2)
# ver 1.2 (2022/6/11)
# ver 1.3 (2022/10/6)
# Written by Yusuke Kyuragi 
# ver 1.3.1 (2023/8/19)
# Modified by Fumitoshi Kodaka
#########################################################

import os, glob, subprocess, shutil, re

def Conv_nii(path):
    sublist = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
    sublist = sorted(sublist)
    # sublist = ["NC0144","NC0145"...]

    for i in range(len(sublist)):
        subname = sublist[i]
        subpath_ = os.path.join(path, subname)

        dirlist_ = []
        for root, subdir, files in os.walk(subpath_): # subpath_: /mnt/.../NC0144/
            for dir in subdir: # subdir: [pre, post, follow]
                dirlist_.append(os.path.join(root, dir))
        dirlist_.sort(key=len) # dirlist_=[NC0144/pre, NC0144/post, NC0144/follow]

        datelist = [p for p in os.listdir(subpath_) if os.path.isdir(os.path.join(subpath_, p))]
        for i in range(len(datelist)):
            if 'pre' in datelist[i] or 'Pre' in datelist[i]:
                datelist[i] = str(1)
            elif 'post' in datelist[i] or 'Post' in datelist[i]:
                datelist[i] = str(2)
            elif 'follow' in datelist[i] or 'Follow' in datelist[i]:
                datelist[i] = str(3)
            else:
                pass
            
        datelist = sorted(datelist) # datelist: [1,2,3]
        t = len(datelist) # t: timpoints. 1=Pre, 2=Pre, Mid, 3=Pre, Mid, Follow

        # convpath = dirlist_[0:t-1]

        for j in range(len(datelist)):
            niipath_ = os.path.join("./img_nii", subname, datelist[j])
            os.makedirs(niipath_, exist_ok=True)

            subprocess.run(f"dcm2niix -o {niipath_} -z y {dirlist_[j]}", shell=True)

            # if datelist[j] in convpath[j]:
            #     subprocess.run(f"dcm2niix -o {niipath_} -z y {convpath[j]}", shell=True)

def Rename():
    path = "./img_nii" 
    sublist = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
    sublist = sorted(sublist)
    # sublist: [NC0144,NC0134..]

    for i in range(len(sublist)):
        subname = sublist[i]
        subpath_ = os.path.join(path, subname)
        # subname: NC0144
        # subpath_: ./img_nii/NC0144

        datelist = [p for p in os.listdir(subpath_) if os.path.isdir(os.path.join(subpath_, p))]
        datelist = sorted(datelist) # datelist = [1,2,3], 1=pre, 2=post, 3=follow
        # datelist: [1,3]
        # datelist: [1,3] <- sorted
        
        datelist_int = [int(i) for i in datelist]

        for j in datelist_int:
            flist = [f for f in glob.glob(os.path.join(subpath_, str(datelist_int), "*")) \
                if re.search('.*(.nii.gz$|.bval$|.bvec$)', f)]
            # flist: [*.nii.gz, *.bval, *bvec]
            timepoint = ["Pre", "Post", "Follow"]
            subname_HCP = "sub-" + subname[2:]

            r_niipath_ = os.path.join("./rename_img_nii", timepoint[j-1], "Images", subname_HCP, "unprocessed/3T")
            T1dir_path = os.path.join(r_niipath_, "T1w_MPR1")
            T2dir_path = os.path.join(r_niipath_, "T2w_SPC1")
            Diffdir_path = os.path.join(r_niipath_, "Diffusion")
            REST_APdir_path = os.path.join(r_niipath_, "rfMRI_REST_AP")
            REST_PAdir_path = os.path.join(r_niipath_, "rfMRI_REST_PA")

            dirlist = [T1dir_path, T2dir_path, Diffdir_path, REST_APdir_path, REST_PAdir_path]
            for _ in range(len(dirlist)):
                os.makedirs(dirlist[_], exist_ok=True)

            # ファイル名
            ## sMRI
            T1_fname = f"{subname_HCP}_3T_T1w_MPR1.nii.gz"
            T2_fname = f"{subname_HCP}_3T_T2w_SPC1.nii.gz"

            ## SE field map
            SEFmap_AP_fname = f"{subname_HCP}_3T_SpinEchoFieldMap_AP.nii.gz"
            SEFmap_PA_fname = f"{subname_HCP}_3T_SpinEchoFieldMap_PA.nii.gz"

            ## diffusion 軸数=bvecファイルの行方向のデータ数
            Diff_AP_fname = f"{subname_HCP}_3T_DWI_dir68_AP.nii.gz"
            Diff_AP_SBRef_fname = f"{subname_HCP}_3T_DWI_dir68_AP_SBRef.nii.gz"
            Diff_AP_bval_fname = f"{subname_HCP}_3T_DWI_dir68_AP.bval"
            Diff_AP_bvec_fname = f"{subname_HCP}_3T_DWI_dir68_AP.bvec"          

            Diff_PA_fname = f"{subname_HCP}_3T_DWI_dir69_PA.nii.gz"
            Diff_PA_SBRef_fname = f"{subname_HCP}_3T_DWI_dir69_PA_SBRef.nii.gz"
            Diff_PA_bval_fname = f"{subname_HCP}_3T_DWI_dir69_PA.bval"
            Diff_PA_bvec_fname = f"{subname_HCP}_3T_DWI_dir69_PA.bvec"

            ## rs-fMRI
            ### AP
            REST_AP_fname = f"{subname_HCP}_3T_rfMRI_REST_AP.nii.gz"
            REST_AP_SBRef_fname = f"{subname_HCP}_3T_rfMRI_REST_AP_SBRef.nii.gz"
            ### PA
            REST_PA_fname = f"{subname_HCP}_3T_rfMRI_REST_PA.nii.gz"
            REST_PA_SBRef_fname = f"{subname_HCP}_3T_rfMRI_REST_PA_SBRef.nii.gz"

            ## melanin
            Melanin_fname = f"{subname_HCP}_3T_T1w_NeuroMEL.nii.gz"


            # 各モダリティの相対パス
            ## sMRI
            T1_fpath = os.path.join(T1dir_path, T1_fname)
            T2_fpath = os.path.join(T2dir_path, T2_fname)

            ## diffusion
            Diff_AP_fpath = os.path.join(Diffdir_path, Diff_AP_fname)
            Diff_AP_SBRef_fpath = os.path.join(Diffdir_path, Diff_AP_SBRef_fname)
            Diff_AP_bval_fpath = os.path.join(Diffdir_path, Diff_AP_bval_fname)
            Diff_AP_bvec_fpath = os.path.join(Diffdir_path, Diff_AP_bvec_fname)
            Diff_PA_fpath = os.path.join(Diffdir_path, Diff_PA_fname)
            Diff_PA_SBRef_fpath = os.path.join(Diffdir_path, Diff_PA_SBRef_fname)
            Diff_PA_bval_fpath = os.path.join(Diffdir_path, Diff_PA_bval_fname)
            Diff_PA_bvec_fpath = os.path.join(Diffdir_path, Diff_PA_bvec_fname)

            ## rs-fMRI
            REST_AP_fpath = os.path.join(REST_APdir_path, REST_AP_fname)
            REST_AP_SBRef_fpath = os.path.join(REST_APdir_path, REST_AP_SBRef_fname)
            REST_PA_fpath = os.path.join(REST_PAdir_path, REST_PA_fname)
            REST_PA_SBRef_fpath = os.path.join(REST_PAdir_path, REST_PA_SBRef_fname)

            ## SE field map
            SEFmap_AP_forT1_fpath = os.path.join(T1dir_path, SEFmap_AP_fname)
            SEFmap_PA_forT1_fpath = os.path.join(T1dir_path, SEFmap_PA_fname)
            SEFmap_AP_forRESTAP_fpath = os.path.join(REST_APdir_path, SEFmap_AP_fname)
            SEFmap_PA_forRESTAP_fpath = os.path.join(REST_APdir_path, SEFmap_PA_fname)
            SEFmap_AP_forRESTPA_fpath = os.path.join(REST_PAdir_path, SEFmap_AP_fname)
            SEFmap_PA_forRESTPA_fpath = os.path.join(REST_PAdir_path, SEFmap_PA_fname)

            ## Neuromelanin
            Melanin_fpath = os.path.join(T1dir_path, SEFmap_AP_fname)

            for fname in flist:
                if 'T1_MPR' in fname:
                    shutil.copy2(fname, T1_fpath)
                elif 'T2_SPC' in fname:
                    shutil.copy2(fname, T2_fpath)
                elif 'DWI_AP' in fname and '17.nii.gz' in fname:
                    shutil.copy2(fname, Diff_AP_SBRef_fpath)
                elif 'DWI_AP' in fname and '18.nii.gz' in fname:
                    shutil.copy2(fname, Diff_AP_fpath)
                elif '18.bval' in fname:
                    shutil.copy2(fname, Diff_AP_bval_fpath)
                elif '18.bvec' in fname:
                    shutil.copy2(fname, Diff_AP_bvec_fpath)
                elif 'DWI_PA' in fname and '22.nii.gz' in fname:
                    shutil.copy2(fname, Diff_PA_SBRef_fpath)
                elif 'DWI_PA' in fname and '23.nii.gz' in fname:
                    shutil.copy2(fname, Diff_PA_fpath)
                elif '23.bval' in fname:
                    shutil.copy2(fname, Diff_PA_bval_fpath)
                elif '23.bvec' in fname:
                    shutil.copy2(fname, Diff_PA_bvec_fpath)
                elif 'REST1_AP' in fname and '9.nii.gz' in fname:
                    shutil.copy2(fname, REST_AP_SBRef_fpath)
                elif 'REST1_AP' in fname and '10.nii.gz' in fname:
                    shutil.copy2(fname, REST_AP_fpath)    
                elif 'REST1_PA' in fname and '12.nii.gz' in fname:
                    shutil.copy2(fname, REST_PA_SBRef_fpath)
                elif 'REST1_PA' in fname and '13.nii.gz' in fname:
                    shutil.copy2(fname, REST_PA_fpath)
                elif 'SEField1_AP_20200929101420_8' in fname:
                    shutil.copy2(fname, SEFmap_AP_forT1_fpath)
                    shutil.copy2(fname, SEFmap_AP_forRESTAP_fpath)
                    shutil.copy2(fname, SEFmap_AP_forRESTPA_fpath)
                elif 'SEField1_PA' in fname:
                    shutil.copy2(fname, SEFmap_PA_forT1_fpath)
                    shutil.copy2(fname, SEFmap_PA_forRESTAP_fpath)
                    shutil.copy2(fname, SEFmap_PA_forRESTPA_fpath)
                else:
                    pass

if __name__ == "__main__":
    cwd = os.getcwd()
    Conv_nii(cwd)
    Rename()
