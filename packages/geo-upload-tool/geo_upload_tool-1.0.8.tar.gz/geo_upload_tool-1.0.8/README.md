# gut - gEO upload tool

Last updated: 2020-01-07

GEO is amazing. Uploading data to GEO is not. I wrote this tool to ease the
pain of preparing all of the files and metadata associated with uploading a
dataset of high throughput sequencing data to GEO. The tool makes the process
much less manual, tedious, and error prone, as it requires well structured
tabular input that can be checked automatically for common problems.

## Installation & Prerequisites

Install using pip or your favorite python package installation mechanism:

```
pip install geo-upload-tool
```

gut uses [STAR](https://github.com/alexdobin/STAR) aligner to prepare the
metadata file for upload. Ensure they are available on your system before using
gut.

## Basic Usage

The entire process is driven from two CSV files: *sample_info* and *file_info*.
Described below:

### Sample Info

This information makes up the SAMPLES section. The CSV should have exactly one
row per sample, and all of the following required columns:

  - **Sample name**: unique name for this sample
  - **source name**: sample source, e.g. brain
  - **organism**: name of the organism, e.g. human
  - **molecule**: one of a set of controlled vocabulary, listed below
  - **description** (optional): description of the sample, if desired

You may include as many more columns in the file as you like, and they will
all be added as **characteristic: tag** columns under the SAMPLES section.

NB: The **Sample name** column is used to cross reference with the file info,
which is discussed next.

### File Info

This information is used to derive the RAW FILES, PROCESSED DATA FILES, and
PAIRED-END EXPERIMENTS sections, as well as the **processed data file** and
**raw file** columns of the SAMPLES section. gut infers whether a file is
raw or processed based on the **rectype** column (see below). The CSV should
have at least one raw and at least one processed file per sample in the
sample info file (GEO requires this).

The raw files are always fastq files, and there should be one row
*per fastq* file per sample, e.g.:

```
Sample name,rectype,file type,instrument model,path,ref_fa,end
A1,PE fastq,fastq,Illumina HiSeq 2000,A1_R1.fastq.gz,hg38.fa,1
A1,PE fastq,fastq,Illumina HiSeq 2000,A1_R2.fastq.gz,hg38.fa,2
A2,SE fastq,fastq,Illumina HiSeq 2000,A2_R1.fastq.gz,hg38.fa,1
```

The processed files may be any other type of file, and there must be at
least one processed file for *each sample* in the sample info file, e.g.
continuing from above example:

```
A1,wig,na,na,A1.wig.gz,na,na
A1,csv,na,ns,raw_counts.csv,na,na
A2,wig,na,na,A2.wig.gz,na,na
A2,csv,na,ns,raw_counts.csv,na,na
```

Note the same file *raw_counts.csv* is provided for both samples, since
the raw counts matrix often contains processed data for all samples.
The CSV file must have all of the following columns with column names
in the first row:

  - **Sample name**: unique name for this sample, corresponds to sample info
  - **rectype**:
      - for RAW files: either "PE fastq" or "SE fastq"
      - for PROCESSSED files: anything appropriate for the file (e.g. csv,
        txt, wig, etc)
  - **file type**: 
      - for RAW files: one of a controlled vocabulary, listed below
      - for PROCESSED files: value ignored
  - **instrument model**:
      - for RAW files: one of a controlled vocabulary, listed below required
      - for PROCESSED files: value ignored
  - **path**: the relative or absolute path to the file on your local system
  - **ref_fa**: (optional)
      - for RAW files only: a fasta reference sequence that can be used to
        compute average insert size and standard deviation for paired-end datasets
  - **end**: required only for rectype == "PE fastq": either 1 or 2 indicating
    the end of the fastq file

Any additional fields in the file info file are quite friendly ignored.

### Validate

With the above CSVs prepared, you can validate them, to make sure everything
lines up as expected:

```
gut validate -o my_geo_submission sample_info.csv file_info.csv
```

The `-o` argument is the name of the directory that will be created to stage
the files (GEO requires the directory be named the same as your email). The
validation logic checks to make sure everything lines up between your samples
and files, e.g. make sure all samples are in both files, each sample has both
raw and processed files, etc.


### Build

Once you have fixed all the problems and validation is successful, you can
build the staged directory:

```
gut build -o my_geo_submission sample_info.csv file_info.csv
```

This will do the following:

  1. Symlink (or copy with `--copy`) all of the raw and processed files into
     the staging directory
  2. Compute md5 checksum on all files
  3. Identify read length and single- or paired-endedness for any fastq files
  4. Calculate the average insert size and standard deviation for paired-end
  fastq files, using STAR and `--ref-fa=FA` or **ref_fa** file_info columns
  to specify the reference sequence.
  5. Construct a metadata file with SAMPLES, PROCESSED DATA FILES, RAW FILES,
  and PAIRED-END EXPERIMENTS sections filled out appropriately, saved as an
  excel file in the staging directory

If all went well, the file *metadata_TOFILL.xlsx* should exist inside the
staging directory. As the *TOFILL* part suggests, you need to fill it out
some more, as the other sections (e.g. SERIES) are not yet complete, unless
you provided the other sections with the `--addnl` CLI flag (see below). I
suggest you create a copy named *metadata_complete.xlsx* or something in the
staging directory and fill that out. Be on the lookout for errors and blank
fields; I surely didn't think to check for every possible mistake.

If you wish to automate the whole honking process, you may also provide a
CSV file with the SERIES, PROTOCOLS, and DATA PROCESSING PIPELINE sections
filled out. The file should contain ONLY these sections, with fields taken
from the v2.1 template. There is an example file in the root of this repo
you may use as a starting point. Once the file is completed, you may provide
it to gut with the `--addnl` CLI option. The resulting `metadata_TOFILL.xlsx`
will have these fields incorporated, and if you were thorough, you might
not need to edit it at all. As per below, the metadata files created by gut
do not upload by default, so you will still have to copy or rename the
metadata file (e.g. to `metadata.xlsx`) for gut to know to upload it.

### Upload

Once you have filled in the missing metadata and put the new file into the
staging directory, you are ready to upload. You will have to initiate the
upload process from the GEO website and receive an upload directory, e.g.
`uploads/your@email.edu_mXoLeWqE`. An FTP client is built into python and
gut uses this to upload just the staged files:

```
gut upload my_geo_submission geousername geopassword uploads/your@email.edu_mXoLeWqE
```

You can get the geousername and geopassword from the GEO website upon
initiating an upload. Your submission should be done in a matter of hours to
days, depending on how big your data are. Then the iteration begins.

NB: gut will upload *everything* in the staging directory *except*:

  - files with **TOFILL** in the name
  - the .cache directory, which contains a bunch of stuff gut made for
  processing the files

You can put other things in there you want to upload if you so desire.

Sometimes upload can fail part way through, especially when uploading many
large files. To avoid unnecessary re-uploads, the upload routine checks
for the presence of each file on the server before uploading, and if the
remote and local file sizes are the same, upload is skipped. You can turn 
this behavior off and force upload every time by supplying `--no-cache` to the
upload command.

## Detailed Documentation

TODO

## Controlled Field Values

### molecule

If `seq_template_v2.1.xls` is to be believed, **molecule** must be precisely
one of:

  - total RNA
  - polyA RNA
  - cytoplasmic RNA
  - nuclear RNA
  - genomic DNA
  - protein
  - other

### rectype

These values are gut-specific, and used to help figure out what to do with
the files. The files that end up in the RAW FILES section are:

  - PE fastq
  - SE fastq

Anything else ends up in the PROCESSED DATA FILES section (e.g. csv, txt,
peak, wig, bed, gff, etc).

### file type

These are the accepted filetype values:

  - fastq
  - Illumina_native_qseq
  - Illumina_native
  - SOLiD_native_csfasta
  - SOLiD_native_qual
  - sff
  - 454_native_seq
  - 454_native_qual
  - Helicos_native
  - srf
  - PacBio_HDF5

### instrument model

According to `seq_template_v2.1.xls`, **instrument model** must be one of:

  - Illumina Genome Analyzer
  - Illumina Genome Analyzer II
  - Illumina Genome Analyzer IIx
  - Illumina HiSeq 2000
  - Illumina HiSeq 1000
  - Illumina MiSeq
  - Illumina NextSeq
  - 
  - AB SOLiD System
  - AB SOLiD System 2.0
  - AB SOLiD System 3.0
  - AB SOLiD 4 System
  - AB SOLiD 4hq System
  - AB SOLiD PI System
  - AB 5500xl Genetic Analyzer
  - AB 5500 Genetic Analyzer
  - 
  - 454 GS
  - 454 GS 20
  - 454 GS FLX
  - 454 GS Junior
  - 454 GS FLX Titanium
  - 
  - Helicos HeliScope
  - PacBio RS
  - PacBio RS II
  - Complete Genomics
  - Ion Torrent PGM
