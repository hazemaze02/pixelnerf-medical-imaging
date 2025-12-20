import os, shutil

SRC_SYNTH = "/DATA/hazellim/final-proj/synth_ucsf_mip"           # where the per-subject npys live
DST_ROOT  = "/DATA/hazellim/final-proj/pixelnerf_data/ucsf"       # has train/val/test

SPLITS = ["train", "val", "test"]
NEED = ["poses_c2w.npy", "images_gray.npy", "meta.json"]

for split in SPLITS:
    split_dir = os.path.join(DST_ROOT, split)
    if not os.path.isdir(split_dir):
        continue
    for subj in os.listdir(split_dir):
        sdir = os.path.join(split_dir, subj)
        if not os.path.isdir(sdir):
            continue
        for fn in NEED:
            dst = os.path.join(sdir, fn)
            if os.path.exists(dst):
                continue
            src = os.path.join(SRC_SYNTH, subj, fn)
            if os.path.exists(src):
                shutil.copy2(src, dst)
            else:
                print(f"[MISSING IN SYNTH ROOT] {subj}/{fn} (expected {src})")

print("Done.")
