# NeuroFedora Species

Welcome to the NeuroFedora Species repository! This repository serves as the central documentation and staging area for spec files intended for the [NeuroFedora](https://neuro.fedoraproject.org/) project. We maintain spec files for packages built in the `mhough/neurofedora` Copr and aim to ultimately submit them to official Fedora repositories.

## 🎯 Goals
- **Package Essential Software:** Bring critical neuroimaging, electrophysiology, and computational neuroscience tools to Fedora Linux natively.
- **Maintain Quality:** Ensure all spec files strictly adhere to Fedora Packaging Guidelines.
- **Upstream Collaboration:** Work with upstream developers and the Fedora community to resolve bugs and build issues.
- **Copr Staging:** Use `mhough/neurofedora` Copr for continuous integration, testing, and delivery of pre-release or complex packages.
## 📦 Package Status
### ✅ Recently Fixed / Updated
- **BabelBrain:** Unbundled `elastix`. Now uses system `elastix` package and removed 100MB+ of bundled binaries.
- **freesurfer:** Applied GCC 15 / C23 compatibility fixes.
- **mrtrix3:** Applied GCC 15 compatibility fixes.

### 🚧 In Progress (Staging in neurofedora-species)
- **FSLeyes Stack:** Drafted spec files for `fslpy`, `fsleyes-props`, `fsleyes-widgets`, and `fsleyes`.
- **SimNIBS:** Updating to 4.6.0 with CGAL 6 compatibility.

## 📦 Missing Packages to Target
Based on a review of NITRC, Neurodesk, and Neurodebian ecosystems, we have identified the following key packages to package for Fedora:
- **Neuroimaging:** FSL (High Complexity), SPM12 (MATLAB/Octave dependency), MRtrix3 (updates)
- **BIDS / Pipelines:** fMRIPrep, QSIPrep, MRIQC, BIDS Validator, HeuDiConv
...
- **Electrophysiology:** MNE-Python (updates), EEGLAB (via Octave/MATLAB), FieldTrip

## 🛠️ Fedora 44 (GCC 15) Repair Effort
With the transition to Fedora 44 and GCC 15, many packages are experiencing build failures due to stricter C23 standards and C++ template parsing. We are actively working on:
- Applying `-std=gnu17` to legacy C code.
- Adding `-fpermissive` and `-include cstdint` to complex C++ projects (ITK, FreeSurfer).
- Updating packages to the latest upstream versions (e.g., SimNIBS 4.6.0).
- Documenting specific fixes in `STATUS-FC44.md` and `FEDORA-44-REPAIR.md`.

## 🧪 Datasets for Testing
To ensure the packaged software works as expected, we use standard datasets for validation:
1. **[OpenNeuro](https://openneuro.org/):** e.g., `ds000001` for testing fMRI preprocessing pipelines.
2. **[BIDS Examples](https://github.com/bids-standard/bids-examples):** A variety of lightweight Brain Imaging Data Structure datasets for testing compatibility and validation tools.
3. **[NIfTI / DICOM Samples](https://nifti.nimh.nih.gov/nifti-1/data):** For testing basic I/O in viewers like ITK-SNAP or Freeview.
4. **HCP Sample Data:** Minimal Human Connectome Project structural and diffusion data for pipeline testing.

## 🚀 Onboarding for New Packagers
Want to help package neuro-software for Fedora? Here is how to get started:
1. **Learn RPM Basics:** Read the [Fedora RPM Guide](https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/).
2. **Setup Your Environment:** 
   ```bash
   sudo dnf install rpmdevtools mock fedpkg
   rpmdev-setuptree
   ```
3. **Understand NeuroFedora:** Check out the [NeuroFedora documentation](https://neuro.fedoraproject.org/).
4. **Test Locally:** Always use `mock` for clean chroot builds before pushing to Copr:
   ```bash
   mock -r fedora-rawhide-x86_64 path/to/your/package.src.rpm
   ```
5. **Join the Community:** We coordinate on the NeuroFedora Matrix channel and mailing list. Reach out if you need sponsorship or review!
