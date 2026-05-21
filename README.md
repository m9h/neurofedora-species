# NeuroFedora Species 🧠📦

Welcome to the **NeuroFedora Species** repository! This project serves as a "zoo" of RPM spec files for neuroimaging, electrophysiology, and computational neuroscience tools. Our mission is to bridge the gap between academic neuro-software and the Fedora Linux ecosystem.

We maintain spec files for the [mhough/neurofedora](https://copr.fedorainfraconnect.org/coprs/mhough/neurofedora/) Copr, with the ultimate goal of upstreaming high-quality packages to the official [NeuroFedora](https://neuro.fedoraproject.org/) repositories.

## 🎯 Goals
- **Broad Coverage:** Package essential but complex tools like FreeSurfer, AFNI, and MRtrix3 that are currently missing or difficult to install on Fedora.
- **Standards Compliance:** Strictly follow [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/).
- **GCC 15 / Fedora 44 Readiness:** Proactively fix build issues related to the C23 standard and modern C++ template strictness.
- **Unbundling:** Replace bundled internal libraries with system packages whenever possible to improve security and maintainability.
- **Automation:** Use CI/CD to ensure spec files remain valid as Fedora Rawhide evolves.

## 🚧 Current Project Status (Fedora 44 / GCC 15)
We have successfully patched several core packages for the transition to Fedora 44:
- ✅ **sigviewer (0.7.1):** Migrated to **Qt6 and CMake**. Linked against system dynamic libraries.
- ✅ **open-ephys-gui (1.0.2):** Major update to version 1.0. Migrated to **Qt6/CMake** and fixed installation paths.
- ✅ **LabRecorder (1.17.1):** Updated to latest and migrated to **Qt6**.
- ✅ **BrainFlow (5.21.0):** Updated to latest stable release.
- ✅ **Morpheus (2.3.9):** Updated and fixed versioned build paths.
- ✅ **AFNI (26.1.01):** Updated to latest and enabled automatic downloads in spec.

## 📦 Missing Packages to Target
Based on a review of NITRC, NeuroDesk, and NeuroDebian, we are targeting these next:
- **Major Suites:** FSL (High Complexity), **SPM-Python** (The new Python-native SPM12).
- **Python Pipelines:** fMRIPrep, QSIPrep, MRIQC, Nipype, Nilearn, PyBIDS.
- **BIDS Tools:** BIDS-Validator, HeuDiConv, CuBIDS.
- **Electrophysiology:** MNE-Python (Official Fedora submission), FieldTrip (via Octave).
- **Reconstruction:** BART (Berkeley Advanced Reconstruction Toolbox).

## 🧪 Datasets for Testing & Validation
To ensure functional correctness, we validate our packages using:
1. **[OpenNeuro ds000001](https://openneuro.org/datasets/ds000001):** The classic "Balloon Analog Risk Task" dataset for fMRI pipeline testing.
2. **[BIDS Examples](https://github.com/bids-standard/bids-examples):** Lightweight datasets for testing `mri_info`, `mrtrix`, and validation tools.
3. **[HCP-Mini](https://www.humanconnectome.org/):** A subset of Human Connectome Project data for diffusion and structural testing.
4. **[MNE-Sample-Data](https://mne.tools/stable/overview/datasets_index.html):** For validating electrophysiology tools.

## 🚀 Onboarding for New Contributors
We welcome new packagers! Here is how to join the effort:

### 1. Setup Your Fedora Build Machine
```bash
sudo dnf install rpmdevtools mock fedpkg rpmlint
rpmdev-setuptree
```

### 2. Configure Mock for Clean Builds
Add yourself to the `mock` group:
```bash
sudo usermod -a -G mock $USER
newgrp mock
```

### 3. The "Species" Workflow
1. **Fork & Clone:** `git clone https://github.com/m9h/neurofedora-species.git`
2. **Draft/Edit:** Update a `.spec` file in the repo.
3. **Local Build:** 
   ```bash
   spectool -g -R package.spec
   rpmbuild -bs package.spec
   mock -r fedora-44-x86_64 ~/rpmbuild/SRPMS/package-*.src.rpm
   ```
4. **Lint:** `rpmlint package.spec` (Aim for 0 errors).
5. **Submit:** Open a Pull Request here!

## 💬 Community
- **Matrix:** [#neurofedora:fedoraproject.org](https://matrix.to/#/#neurofedora:fedoraproject.org)
- **Mailing List:** [neurofedora@lists.fedoraproject.org](https://lists.fedoraproject.org/admin/lists/neurofedora.lists.fedoraproject.org/)
