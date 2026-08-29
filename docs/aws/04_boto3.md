## Reusable uploader

The uploader accepts a table name through the command line rather than
hard-coding one dataset.

**Example**:
python upload_to_s3.py rental_units

Benefits:

- One implementation supports multiple source tables.
- Invalid table names are rejected.
- Each table has an independent S3 prefix.
- The script is easier to automate later with Lambda or orchestration.

**Check the following commits to see the evolution of the upload_to_s3.py loading script:**
- "Generalize S3 snapshot uploader for multiple tables"
- "Add timestamped S3 snapshot uploads"
- "Add AWS S3 learning project scaffold"


