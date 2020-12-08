<p align="center">
    <img src="assets/favicon.png" width="300px" alt="Logo" >
    <br />
    <p align="center">
      Voice Enabled Attendance Monotoring System 👨‍🏫
      <br />
      <br />
      Your one stop solution for attendance monitoring and reports.
      <br />
      <br />
      <a href="https://github.com/debdutgoswami/smart-attendance/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
      ·
      <a href="https://github.com/debdutgoswami/smart-attendance/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
    </p>
</p>

---


## Usage (API)

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
    ```

---

## Getting Started

### Installation (Django)

1. Clone the repository

### Installation (Flask)

1. Clone the repository