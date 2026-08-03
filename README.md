# RentFlow Data Platform

# Daily Practice Checklist


- [ ] Pull latest code
- [ ] Activate virtual environment
- [ ] Run all tests
- [ ] Complete one Azure Board task
- [ ] Implement one feature
- [ ] Write/update Obsidian notes
- [ ] Commit changes
- [ ] Push to GitHub


## 2. Review Azure Board

Open the Sprint Board.

Review:

- Active PBIs
- Active Tasks
- Current AWS milestone

Choose ONE task to complete.

Example:

AWS-010

☐ Supabase Environment Setup
☐ Supabase Extraction Service
☐ Data Export & S3 Integration

Decide which task will be completed today.

---





## Quick Start
Follow these steps every time you start working on the project.

### 1. Open the project
Open Visual Studio Code.
```
File → Open Folder...
C:\Projects\rentflow-data-platform
```

---
### 2. Open a PowerShell terminal

Jump to the right project folder on local:
```powershell
cd C:\Projects\rentflow-data-platform
```

---
### 3. Activate the Python virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

Expected:
```
(.venv)
```
at the beginning of the terminal prompt.

---
### 4. Verify Pytho, AWS CLI, Git branch
```powershell
python --version
aws --version
git status
```

Expected:
```
On branch aws-learning
```

---
### 5. Pull the latest changes

```powershell
git pull origin aws-learning
```

---
### 6. Verify AWS credentials
```powershell
aws sts get-caller-identity
```

You should see your AWS account information.

---
### 7. Verify the Python environment
```powershell
python -m pip list
```

If packages are missing:
```powershell
python -m pip install -r requirements.txt
```

---
### 8. Run the test suite
```powershell
pytest
```

Expected:
```
... passed
```

---
### 9. Start development
Run whichever component you are currently working on.

Examples:
Validate S3 upload

```powershell
python -m aws.s3.scripts.upload_to_s3 agencies
```

Extract RentFlow data
```powershell
python -m aws.s3.scripts.extract_from_supabase rental_units
```

---
## End of day
Before finishing:
```powershell
git status
```

Stage changes
```powershell
git add .
```

Commit
```powershell
git commit -m "Meaningful commit message"
```

Push
```powershell
git push origin aws-learning
```

---
## Project Structure
```
rentflow-data-platform/

aws/
    s3/
        extractors/
        scripts/
        services/
        validation/
        tests/

docs/

README.md

requirements.txt

pytest.ini

.env              (ignored)
.env.example
```

