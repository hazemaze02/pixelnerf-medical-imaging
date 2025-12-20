import os
import shutil
import random

SRC_TRAIN = "/DATA/hazellim/final-proj/pixelnerf_data/ucsf/train"
ROOT = "/DATA/hazellim/final-proj/pixelnerf_data/ucsf"

VAL_FRAC = 0.10
TEST_FRAC = 0.10
SEED = 42

# If True: copy instead of move (slower, uses more disk)
COPY_MODE = True

def is_subject_dir(path: str) -> bool:
    return os.path.isdir(path)

def main():
    random.seed(SEED)

    if not os.path.isdir(SRC_TRAIN):
        raise RuntimeError(f"Source train dir not found: {SRC_TRAIN}")

    # subject folders inside train/
    subjects = sorted([
        d for d in os.listdir(SRC_TRAIN)
        if is_subject_dir(os.path.join(SRC_TRAIN, d))
    ])

    if len(subjects) == 0:
        raise RuntimeError(f"No subject folders found in {SRC_TRAIN}")

    random.shuffle(subjects)

    n = len(subjects)
    n_test = int(round(TEST_FRAC * n))
    n_val  = int(round(VAL_FRAC * n))

    test_subjects = subjects[:n_test]
    val_subjects  = subjects[n_test:n_test + n_val]
    train_subjects = subjects[n_test + n_val:]

    # ensure dirs exist
    out_train = os.path.join(ROOT, "train")
    out_val   = os.path.join(ROOT, "val")
    out_test  = os.path.join(ROOT, "test")
    os.makedirs(out_train, exist_ok=True)
    os.makedirs(out_val, exist_ok=True)
    os.makedirs(out_test, exist_ok=True)

    def transfer(subj, dst_root):
        src = os.path.join(SRC_TRAIN, subj)
        dst = os.path.join(dst_root, subj)
        if os.path.exists(dst):
            raise RuntimeError(f"Destination already exists: {dst}")
        if COPY_MODE:
            shutil.copytree(src, dst)
        else:
            shutil.move(src, dst)

    print(f"Found {n} subjects in {SRC_TRAIN}")
    print(f"Split -> train={len(train_subjects)} val={len(val_subjects)} test={len(test_subjects)}")
    print("Mode:", "COPY" if COPY_MODE else "MOVE")

    # Move/copy val + test out of train; leave remaining in train
    for subj in val_subjects:
        transfer(subj, out_val)

    for subj in test_subjects:
        transfer(subj, out_test)

    # If we moved items out, train already contains remaining.
    # If we copied, we should ensure train contains the training subset too.
    if COPY_MODE:
        for subj in train_subjects:
            src = os.path.join(SRC_TRAIN, subj)
            dst = os.path.join(out_train, subj)
            if not os.path.exists(dst):
                shutil.copytree(src, dst)

    print("Done.")
    print("Train:", out_train)
    print("Val:  ", out_val)
    print("Test: ", out_test)

if __name__ == "__main__":
    main()
