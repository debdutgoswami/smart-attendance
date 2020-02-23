# Smart Attendance

A web app to facilitate voice controlled attendance system.

## APIs

1. /upload
```
request-type: POST
purpose: uploading the voice from the microphone.
returns: JSON containing list of absents and presents
```

2. /prof
```
request-type: POST
purpose: adding new professor
returns: "OK" on success
```

3. /class
```
request-type: POST
purpose: add new class
returns: Class Unique Identifier (CUI)
```

4. /allclass
```
request-header: POST
purpose: fetching all the classes under a particular professor
returns: JSON containing list CUI along with it's name
```

5. /update
```
request-header: POST
purpose: marking students absent or present
returns: "OK" on success
```

6. /report
```request-header: POST
purpose: fetching students records
returns: individual class data (student records)
```

7. /reqister (upcoming)
```
request-header: POST
purpose: uploading students register via image
returns: "OK" on success