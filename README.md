# simple-wdl
A simple WDL workflow and Cromwell submission script. 

The workflow simply concatenates two input files and reports the location of the output file.

It is assumed you are running this in a cloud environment and have a Cromwell server set up and listening. It also assumes you are making use of bucket storage. No assumptions about bucket access policies, networking, etc. are made.

The submission script is very bare bones and may not handle all manner of errors, such as if bucket access is denied, etc.

#### To use:

- Upload/copy/etc. two files (any plain text content) in a bucket. 
- Add those paths (full paths, e.g. `s3://<bucket>/<object>`) to the `inputs.json` file.
- Determine the IP address + port of the Cromwell server you are using, including http/https protocol. Call this `<CROMWELL_HOST>`
- Run the script: `python3 cromwell_submit.py <CROMWELL_HOST>`, e.g. `python3 cromwell_submit.py http://10.150.0.2:8000`

The script will submit the job and watch progress until the workflow has completed. If it successfully completes, it will report the location of the output file.