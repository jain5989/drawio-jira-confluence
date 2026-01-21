# Troubleshooting Guide

Common issues and solutions.

## Backend Issues

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Kill the process or change port in app.py
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall:
pip install -r requirements.txt
```

### CORS Errors

**Error:** Browser console shows CORS errors

**Solution:**
1. Verify backend is running
2. Check `flask-cors` is installed:
```bash
pip install flask-cors
```
3. Restart backend server

## Frontend Issues

### Configuration Not Saving

**Issue:** Settings don't persist after refresh

**Solution:**
- Check browser localStorage is enabled
- Try a different browser
- Check browser console for errors

### Files Won't Upload

**Issue:** Drag & drop doesn't work

**Solution:**
1. Check file type (.drawio, .xml, .mmd, .txt only)
2. Check file size (max 16MB by default)
3. Try clicking instead of dragging
4. Check browser console for errors

## API Issues

### 401 Unauthorized

**Error:** Authentication failed

**Solution:**
1. Verify API token is correct
2. Check email matches Atlassian account
3. Generate new API token if needed
4. Ensure no extra spaces in credentials

### 403 Forbidden

**Error:** Permission denied

**Solution:**
1. Verify you have permissions in project
2. Check project key is correct
3. Verify space key exists
4. Check you can create issues/pages manually

### 404 Not Found

**Error:** Resource not found

**Solution:**
1. Check Jira/Confluence URLs are correct
2. Remove trailing slashes (except for /wiki)
3. Verify project and space exist
4. Test URLs in browser

### 400 Bad Request

**Error:** Invalid request

**Solution:**
1. Check all required fields are filled
2. Verify file format is correct
3. Check configuration JSON is valid
4. Review backend logs for details

## File Processing Issues

### Draw.io Parse Error

**Error:** Invalid draw.io file format

**Solution:**
1. Verify file is valid draw.io XML
2. Try opening in draw.io to check
3. Re-export from draw.io
4. Check file isn't corrupted

### Mermaid Syntax Error

**Error:** Invalid Mermaid syntax

**Solution:**
1. Validate syntax at https://mermaid.live
2. Check for typos in participant names
3. Ensure proper arrow syntax (->>, -->>)
4. Review Mermaid documentation

## Batch Processing Issues

### Some Files Fail

**Issue:** Batch processing completes but some files failed

**Solution:**
1. Check error messages for each file
2. Process failed files individually to see details
3. Verify all files are valid format
4. Check file names don't have special characters

### Progress Bar Stuck

**Issue:** Progress bar doesn't update

**Solution:**
1. Check browser console for errors
2. Refresh page and try again
3. Try smaller batch sizes
4. Check network connection

## Performance Issues

### Slow Processing

**Issue:** Files take long to process

**Solution:**
1. Process fewer files at once
2. Check network connection
3. Verify Atlassian services are responsive
4. Check backend server resources

### Memory Errors

**Error:** Out of memory

**Solution:**
1. Reduce batch size
2. Process files individually
3. Restart backend server
4. Check file sizes

## Getting Help

If your issue isn't listed:

1. Check backend logs:
```bash
# Backend prints detailed errors
python app.py
```

2. Check browser console:
   - F12 to open developer tools
   - Look at Console tab
   - Look at Network tab for API calls

3. Test with sample files:
   - Use files from `examples/` directory
   - If samples work, issue is with your files

4. Verify configuration:
   - Test API token with curl:
```bash
curl -u email@example.com:API_TOKEN \
  https://your-domain.atlassian.net/rest/api/3/myself
```

## Still Need Help?

- Create detailed issue with:
  - Error message
  - Steps to reproduce
  - Browser/Python versions
  - Configuration (without sensitive data!)
  - Backend logs
